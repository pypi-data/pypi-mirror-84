
import sys
from sout import sout
from setuptools import setup, find_packages
import pypandoc

def ls_finder(arg_ls):
	ret_ls = []
	for temp_dir in arg_ls:
		for e in find_packages(temp_dir): ret_ls.append(e)
	return ret_ls

with open("./README.md", encoding="utf-8") as f:
	long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, "rst", format="markdown_github")

setup(
	name = "SoftDB",
	version = "0.0.3",
	description = "DB that can be manipulated as if they were objects in memory",
	author = "le latelle",
	author_email = "g.tiger.ml@gmail.com",
	url = "https://github.co.jp/",
	packages = ["SoftDB", "SoftDB.parts.hash_tool", "SoftDB.parts.python_layer", "SoftDB.parts.sql_layer"],
	install_requires = ["relpath", "sout", "tqdm", "xxhash"],
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license = "MIT",
	classifiers = [
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Libraries",
		"License :: OSI Approved :: MIT License"
	]
)
