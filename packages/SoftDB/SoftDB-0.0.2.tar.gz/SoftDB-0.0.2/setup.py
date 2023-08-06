
import sys
from sout import sout
from setuptools import setup, find_packages
import pypandoc

with open("./README.md", encoding="utf-8") as f:
	long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, "rst", format="markdown_github")

setup(
	name = "SoftDB",
	version = "0.0.2",
	description = "DB that can be manipulated as if they were objects in memory",
	author = "le latelle",
	author_email = "g.tiger.ml@gmail.com",
	url = "https://github.co.jp/",
	packages = ["SoftDB"],
	install_requires = ["relpath", "sout", "tqdm"],
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license = "MIT",
	classifiers = [
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Libraries",
		"License :: OSI Approved :: MIT License"
	]
)
