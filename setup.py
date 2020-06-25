import versioneer
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='tornado-restful',
    packages=find_packages(exclude=['tests']),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='library for easy restful APIs in tornado',
    long_description=long_description,
    install_requires=['tornado'],
    author='Richard Postelnik',
    author_email='richard.postelnik@gmail.com',
    url='https://github.com/postelrich/tornado-restful',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: New BSD",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)