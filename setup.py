from setuptools import setup, find_packages

setup(
    name='AC3D',
    version='0.0.1',
    packages=find_packages(),
    package_data={'AC3D': ['data/Acetylation.txt']},
    include_package_data=True,
    install_requires=[]
)