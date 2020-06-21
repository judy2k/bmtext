from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

PILLOW_DEPS = [
    "pillow ~= 7.1",
]

DEV_DEPS =  [
    "black",
    "pytest",
    "twine",
    "wheel",
] + PILLOW_DEPS

setup(
    name="bmtext",
    description="Render text from BMFont bitmap fonts.",
    author="Mark Smith",
    author_email="judy@judy.co.uk",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    version="0.0.2",

    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "attrs~=19.3",
    ],
    extras_require={
        "dev": DEV_DEPS,
        "pillow": PILLOW_DEPS,
    },
)