
# SoftDBのSQL層 [sql_layer]

import sys
import sqlite3
from sout import sout

# SoftDBのSQL層 [sql_layer]
class SQLLayer:
	# 初期化処理
	def __init__(self, db_filename):
		self.sq3 = sqlite3.connect(db_filename)
		self.cur = self.sq3.cursor()
		# テーブル作成
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS main_table
			(raw_key int NOT NULL PRIMARY KEY,
			raw_value BLOB);
		""")
	# データ新規作成
	def create(self, key, value):
		self.cur.execute("INSERT INTO main_table VALUES (?, ?);", (key, value))
		self.sq3.commit()
	# データ取得
	def read(self, key):
		self.cur.execute("SELECT * FROM main_table WHERE raw_key = ?;", (key,))
		fetch_result = self.cur.fetchall()
		if len(fetch_result) == 0: raise Exception("[SQLLayer error] KeyError(key = %s)"%str(key))
		return fetch_result[0][1]
	# keyの存在確認
	def has_key(self, key):
		self.cur.execute("SELECT 1 FROM main_table WHERE raw_key = ?;", (key,))
		fetch_result = self.cur.fetchall()
		return (len(fetch_result) > 0)
	# データ更新
	def update(self, key, value):
		self.cur.execute("UPDATE main_table SET raw_value = ? WHERE raw_key = ?;", (value, key))
		self.sq3.commit()
	# データ削除
	def delete(self, key):
		self.cur.execute("DELETE FROM main_table WHERE raw_key = ?;", (key,))
		self.sq3.commit()
