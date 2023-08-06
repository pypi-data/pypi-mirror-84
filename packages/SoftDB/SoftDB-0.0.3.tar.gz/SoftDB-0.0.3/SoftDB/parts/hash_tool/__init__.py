
# ハッシュ関数関連ツール [hash_tool]

import sys
from sout import sout
import xxhash

# SHA-256ハッシュ [hash_tool]
def sha_256_hash(arg_str):
	raise Exception("mijisso!")
	return hash_value

# xxh64 [hash_tool]
def xxh64(arg_bin):
	x64 = xxhash.xxh64()
	x64.update(arg_bin)
	hash_value = x64.intdigest()
	return hash_value
