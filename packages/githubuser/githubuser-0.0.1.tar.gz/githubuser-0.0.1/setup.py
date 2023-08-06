from setuptools import setup,find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Find Github user basic details'
LONG_DESCRIPTION = "This package can be used to extract a Github user's basic details like name,no of repos etc."

# Setting up
setup(
    name="githubuser",
    version=VERSION,
    author="Pranav V P",
    author_email="<pranavvp07@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'Github', 'githubuser'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)