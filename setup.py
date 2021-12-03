# coding:utf8
"""
@author Nemo
@time 2021/12/03 11:01
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nemo_python_db",
    version="1.0.0",

    author="Nemo",
    author_email="nemo@link-nemo.com",

    description="简单的数据操作库",
    long_description=long_description,

    keywords='python tool database',
    long_description_content_type="text/markdown",

    url="https://github.com/geeeeeeeeeeeeeeeek/nemo_python_db",
    license="MIT Licence",

    platforms='Mac Linux',

    packages=setuptools.find_packages(),
    include_package_data=True,

    programming_language="python3",
)
