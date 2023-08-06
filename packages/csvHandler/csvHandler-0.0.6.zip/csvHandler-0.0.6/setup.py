from setuptools import find_packages, setup

setup(
    name='csvHandler',
    packages=find_packages(),
    version='0.0.6',
    description='csv in memory paginator',
    author='own-backup',
    license='MIT',
    install_requires=['pandas']
)