from setuptools import setup

setup(
    author="Boyuan Liu",
    author_email="boyuanliu6@yahoo.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
    description="A CLI for saving notes, both locally and online",
    license="MIT",
    install_requires=[],
    name="notesaver",
    packages=["notesaver"],
    python_requires=">= 3.6",
    entry_points={
        "console_scripts": ["notesaver=NoteSaver.__main__:main"]
    },
    url="https://github.com/boyuan12/NoteSaver",
    version="0.0.1",
)