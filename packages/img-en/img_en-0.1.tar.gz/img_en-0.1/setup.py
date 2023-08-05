import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(
    name = "img_en",
    version = "0.1",
    description = "It takes img and int zoom level and output zoomed image.",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://www.youtube.com/channel/UC_7_s7TPjHp2WgCJAbyKLOg",
    author = "Sarthak Karki",
    author_email = "srthk7338@gmail.com",
    license = "MIT",
    keywords = "zoom",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"],
    packages = ["img_en"],
    include_package_data = True,

    install_requires = ["opencv-python==4.4.0.44","numpy==1.19.3"],


)