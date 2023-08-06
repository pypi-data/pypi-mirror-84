
# SoftDBのSQL層 [sql_layer]
# 【動作確認 / 使用例】

import sys
from sout import sout
from relpath import add_import_path
add_import_path("../")
from sql_layer import SQLLayer

# SoftDBのSQL層 [sql_layer]
sl = SQLLayer("./database.sdb")

# 準備 (key == 2がある場合は削除)
if sl.has_key(key = 2) is True: sl.delete(key = 2)

### 正常系 ###

# データ新規作成
sl.create(key = 2, value = b"hoge")
# データ取得
value = sl.read(key = 2)
assert value == b"hoge"
# keyの存在確認
assert sl.has_key(key = 2) is True
assert sl.has_key(key = 0) is False
# データ更新
sl.update(key = 2, value = b"fuga")
assert sl.read(key = 2) == b"fuga"
# データ削除
sl.delete(key = 2)
assert sl.has_key(key = 2) is False

### 異常系 ###

# すでにあるkeyをcreate
sl.create(key = 2, value = b"hoge")
error = "NO ERROR"
try:
	sl.create(key = 2, value = b"hoge")
except Exception as e:
	error = e
assert str(error).split(":")[0] == "UNIQUE constraint failed"
# 存在しないkeyをread
error = "NO ERROR"
try:
	sl.read(key = 23)
except Exception as e:
	error = e
assert str(error).split("(")[0] == "[SQLLayer error] KeyError"
# 存在しないkeyをupdate
sl.update(key = 23, value = b"hoge")	# エラーは起こらないが何も実行されない
# 存在しないkeyをdelete
sl.delete(key = 23)	# エラーは起こらないが何も実行されない

print("--- TEST ALL CLEAR ---")
