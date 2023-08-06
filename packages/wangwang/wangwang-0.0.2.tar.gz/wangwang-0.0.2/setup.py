# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="UTF_8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wangwang",
    version="0.0.2",
    author="ZERONE",
    author_email="zerone40@163.com",
    description="钉钉群消息推送",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
