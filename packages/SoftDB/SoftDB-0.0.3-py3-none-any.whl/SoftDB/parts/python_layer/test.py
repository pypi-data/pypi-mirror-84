
# SoftDBのpython層 [python_layer]
# 【動作確認 / 使用例】

import sys
from sout import sout
from tqdm import tqdm
from relpath import add_import_path
add_import_path("../")
from python_layer import Hash

# 辞書 [python_layer]
h_obj = Hash("./database.sdb")

# データ追記
h_obj["hoge"] = ["fuga", 55]

# key存在確認
assert ("hoge" in h_obj) is True
assert ("moge" in h_obj) is False

# データ読み出し
assert h_obj["hoge"] == ["fuga", 55]

# 領域拡大のテスト
for i in tqdm(range(50)):
	h_obj[str(i)] = i
for i in range(50): assert h_obj[str(i)] == i

# 2重追記テスト
h_obj["hoge"] = "fugaku"
assert h_obj["hoge"] == "fugaku"

### 異常系

# keyが文字列ではない
try:
	h_obj[2.3] = "hoge"
except Exception as e:
	assert str(e) == "[__setitem__() error] The type of the key must be a string."

# 非存在key読み出し
try:
	h_obj["homa"]
except Exception as e:
	assert str(e) == "[__getitem__() error] KeyError: homa"

print("--- TEST ALL CLEAR ---")
