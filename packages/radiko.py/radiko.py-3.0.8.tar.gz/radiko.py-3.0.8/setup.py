import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="radiko.py",
    version="3.0.8",
    author="akatonbo1011",
    author_email="akatonbobook@gmail.com",
    description="radiko rapper",
    install_requires=["requests", "m3u8"],
    tests_require=["requests", "m3u8"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Radiko, radiko, radiko.py, Radiko.py",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: BSD License',
    ]
)