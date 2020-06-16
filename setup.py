import versioneer
from setuptools import setup, find_packages


setup(
    name='tornado-restful',
    packages=find_packages(exclude=['tests']),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='library for easy restful APIs in tornado',
    install_requires=['tornado'],
    extras_require={
        'test': ['pytest',
                 'pytest-spec']
    },
    author='Richard Postelnik',
    author_email='richard.postelnik@gmail.com',
    url='https://github.com/postelrich/tornado-restful',
    zip_safe=False
)