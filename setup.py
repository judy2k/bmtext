from setuptools import setup, find_packages

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
        "dev": [
            "black",
            "pytest",
            "twine",
            "wheel",
        ]
    },
    
)