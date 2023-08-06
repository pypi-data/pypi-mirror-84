from setuptools import setup, find_packages

setup(
    name="clangast",
    version="0.2.1",
    descriptiom="Find and indexing algorithms for AST based on clang",
    url="https://github.com/DmitIW/clang_ast_wrapper",
    author="Dmitri Ivakhnenko",
    author_email="dmit.ivh@gmail.com",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=["clang>=11.0"]
)
