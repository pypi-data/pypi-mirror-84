from setuptools import setup, find_packages

setup(
    name="waveprocess",
    version="0.0.1",
    license="MIT Licence",

    url="https://github.com/ailabnjtech/wavepro/tree/master",
    author="zhang_1998",
    author_email="727261446@qq.com",

    packages=find_packages(),
    install_requires=["torch","numpy"],
    include_package_data=True,
    platforms="any",
)