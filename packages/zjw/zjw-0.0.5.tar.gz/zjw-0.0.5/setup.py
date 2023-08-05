import setuptools

with open("README.md", "r", encoding="utf-8") as fg:
    long_description = fg.read()


setuptools.setup(
    name="zjw",
    version = "0.0.5",
    author = "zjw",
    author_email="2415528035@qq.com",
    description="a package for extend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],

)