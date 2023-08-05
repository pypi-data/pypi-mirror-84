from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='matrix_path',
    version='1.1.1',
    description='Navigating and Visualizing paths in a 2D Matrix.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rushmash91/matrix_path",
    author="Arush Sharma",
    author_email="arushsharma91@gmail.com",
    py_modules=["matrix"],
    package_dir={"": "src"},
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[],
)