from setuptools import setup, find_packages

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