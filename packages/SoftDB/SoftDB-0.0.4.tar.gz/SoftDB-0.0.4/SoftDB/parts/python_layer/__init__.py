
# SoftDBのpython層 [python_layer]

import sys
import math
import pickle
from tqdm import tqdm
from sout import sout
from relpath import add_import_path
add_import_path("../")
from sql_layer import SQLLayer
# xxh64 [hash_tool]
from hash_tool import xxh64

# SoftDBのpython層 [python_layer]
class Hash:
	# 初期化処理
	def __init__(self, db_filename, load_factor = 0.75):
		# SoftDBのSQL層 [sql_layer]
		self.sql_layer = SQLLayer(db_filename)
		self.load_factor = load_factor
		self.min_bucket_size = 6
		self.during_bucket_change = False
		# DBの初期化
		if self.sql_layer.has_key(0) is False:
			# DB上のbucket_offsetとbucket_sizeの初期化
			self.sql_layer.create(0, pickle.dumps(2))	# bucket_offset
			self.sql_layer.create(1, pickle.dumps(0))	# bucket_size
		self.bucket_offset = pickle.loads(self.sql_layer.read(0))
		self.bucket_size = pickle.loads(self.sql_layer.read(1))	# ハッシュテーブルの領域サイズ
		self.data_n = len([k for k in self])
		# 必要ならば初期領域を再確保
		self.__change_bucket_size()
	# データ書き込み
	def __setitem__(self, key, value):
		# keyを見つける (内部関数)
		found_flag, addr, _ = self.__find_key(key)
		# 格納する値の作成
		bin_value = pickle.dumps((key, value))
		# 格納
		self.sql_layer.update(addr, bin_value)
		# データ数記録のインクリメント
		if found_flag is False: self.data_n += 1
		# 必要ならば領域を再確保
		self.__change_bucket_size()
		# # [debug] メモリ内容表示
		# self.memory_debug()
	# key存在確認
	def __contains__(self, key):
		# keyを見つける (内部関数)
		found_flag, addr, value = self.__find_key(key)
		return found_flag
	# データ読み出し
	def __getitem__(self, key):
		# keyを見つける (内部関数)
		found_flag, addr, value = self.__find_key(key)
		# 見つからない場合
		if found_flag is False: raise Exception("[__getitem__() error] KeyError: %s"%str(key))
		# 値を返す
		return value
	# 全データを走査
	def __iter__(self):
		for idx in range(self.bucket_size):
			addr = self.bucket_offset + idx
			bin_value = self.sql_layer.read(key = addr)
			if len(bin_value) == 0: continue
			key, _ = pickle.loads(bin_value)
			yield key
	# データ数を返す
	def __len__(self):
		return self.data_n
	# keyを見つける (内部関数)
	def __find_key(self, key):
		# keyの型のチェック
		if type(key) != type(""): raise Exception("[__setitem__() error] The type of the key must be a string.")
		# keyのハッシュ値を計算
		hash_value = xxh64(key.encode())	# xxh64 [hash_tool]
		# 仮のアドレス値
		rel_addr_0 = hash_value % self.bucket_size
		# 開番地法で格納アドレスを決定
		for i in range(self.bucket_size):
			# アドレス値をシフトしていく
			rel_addr = (rel_addr_0 + i) % self.bucket_size
			addr = self.bucket_offset + rel_addr
			# その番地を読んでみる
			bin_value = self.sql_layer.read(addr)
			# 空き地だった場合
			if len(bin_value) == 0:
				return False, addr, None
			# オブジェクトを解凍
			temp_key, value = pickle.loads(bin_value)
			if temp_key == key:
				return True, addr, value
		# 開番地が見つからなかった場合
		raise Exception("[Hash internal error] The area should be expanded before it is all filled up.")
	# 適正な領域の広さを計算
	def __calc_proper_bucket_size(self):
		raw_plf = self.data_n / self.load_factor
		if raw_plf < self.min_bucket_size: raw_plf = self.min_bucket_size
		# 2のべき乗に揃える
		pow2 = math.ceil(math.log(raw_plf, 2))
		proper_bucket_size = int(math.pow(2, pow2))
		return proper_bucket_size
	# 必要ならば領域を再確保
	def __change_bucket_size(self):
		# 領域サイズ変更中の判定
		if self.during_bucket_change is True: return None
		# 領域サイズ変更要否の判断
		proper_bucket_size = self.__calc_proper_bucket_size()	# 適正な領域の広さを計算
		if self.bucket_size == proper_bucket_size: return None
		# 領域サイズ変更中
		self.during_bucket_change = True
		# 領域サイズ変更前のbucketの情報を退避
		prev_offset = self.bucket_offset
		prev_size = self.bucket_size
		# offset, bucket_size値を新しい値に更新
		self.bucket_offset = prev_offset + prev_size
		self.bucket_size = proper_bucket_size
		# 新しい領域範囲をsql_layer上に物理的に確保
		for idx in range(self.bucket_size):
			addr = self.bucket_offset + idx
			self.sql_layer.create(key = addr, value = b"")	# データ新規作成
		# 古い領域のデータをすべて走査して、新しい領域に保存
		self.data_n = 0
		for idx in range(prev_size):
			addr = prev_offset + idx
			bin_value = self.sql_layer.read(key = addr)
			# 空き地だった場合は飛ばす
			if len(bin_value) == 0: continue
			key, value = pickle.loads(bin_value)
			self[key] = value	# 新しい領域にセット
		# DB上のoffset, bucket_size値を更新する
		self.sql_layer.update(0, pickle.dumps(self.bucket_offset))
		self.sql_layer.update(1, pickle.dumps(self.bucket_size))
		# 古いアドレス範囲をすべて削除 (sql_layerにおける「削除」)
		for idx in range(prev_size):
			addr = prev_offset + idx
			self.sql_layer.delete(key = addr)
		self.during_bucket_change = False
	# [debug] メモリ内容表示
	def memory_debug(self):
		for idx in range(self.bucket_size):
			addr = self.bucket_offset + idx
			bin_value = self.sql_layer.read(key = addr)
			if len(bin_value) == 0:
				show_s = "(empty)"
			else:
				key, value = pickle.loads(bin_value)
				show_s = "key: %s, value: %s"%(str(key), str(value))
			print("[%d] %s"%(addr, show_s))
		print("-------")
