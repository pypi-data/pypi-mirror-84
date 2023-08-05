from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
setup(
    name="sfjwt",
    version="1.0.1",
    description="A small repo to provide functions to authenticate against SalesForce.",
    long_description=(here / 'ReadMe.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url="https://github.com/Rehket/SalesForceJWT-Server-Auth",
    author="Adam A",
    author_email="aalbright425@gmail.com",
    license="MIT",
    packages=["sfjwt"],
    zip_safe=True,
    install_requires=["requests", "PyJWT"],
    extras_require={  # Optional
        "dev": ["responses", "pytest", "coverage", "pip-tools"],
    },
)
