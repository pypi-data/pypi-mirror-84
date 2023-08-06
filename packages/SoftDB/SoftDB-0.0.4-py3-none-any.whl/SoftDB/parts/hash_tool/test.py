
# ハッシュ関数関連ツール [hash_tool]
# 【動作確認 / 使用例】

import sys
from sout import sout
from relpath import add_import_path
add_import_path("../")
# xxh64 [hash_tool]
from hash_tool import xxh64

# xxh64 [hash_tool]
hash_value = xxh64(b"hoge")
assert hash_value == 5662325944257968344

print("--- TEST ALL CLEAR ---")
