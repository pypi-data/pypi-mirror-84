import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KevinSR",
    version="0.0.7",
    author="Kevin Zhang",
    author_email="zhangkuanmayo@gmail.com",
    description="This is a test package for data preprocessing of medical imaging masks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/KevinSR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
