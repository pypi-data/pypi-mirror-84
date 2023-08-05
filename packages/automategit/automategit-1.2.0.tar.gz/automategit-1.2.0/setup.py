from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()

setup(
    name='automategit',
    version= '1.2.0',
    description='Github automation using python',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Anukrati Rawal',
    author_email='anukratirawal1.4@gmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["automategit"],
    install_requires=[ "PyGithub==1.53","requests==2.24.0",],
    dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'])