
# SoftDB [SoftDB]
# 【動作確認 / 使用例】

import sys
from relpath import add_import_path
add_import_path("../")
# SoftDB [SoftDB]
import SoftDB

# SoftDB [SoftDB]
sdb = SoftDB("test_DB.sdb")

sdb["hoge"] = ["fuga", 23]

# key存在確認
assert ("hoge" in sdb) is True
assert ("moge" in sdb) is False

# データ読み出し
assert sdb["hoge"] == ["fuga", 23]

print("--- TEST ALL CLEAR ---")
