
import sys
# SoftDBのpython層 [python_layer]
from .parts.python_layer import Hash

# ダミー実装: python_layerそのまま
SoftDB = Hash

# モジュールをそのままcallできるようにする工夫
class mod_call:
    def __init__(self):
    	self.SoftDB = SoftDB
    def __call__(self, *args, **kwargs):
        return SoftDB(*args, **kwargs)

sys.modules[__name__] = mod_call()
