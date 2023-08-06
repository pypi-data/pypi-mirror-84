from setuptools import find_packages, setup

setup(
    name="pystac-io",
    version="0.1.0",
    description="Python library providing additional IO implementations for PySTAC",
    author="Azavea",
    author_email="info@azavea.com",
    url="https://github.com/azavea/pystac-io",
    license="Apache Software License 2.0",
    packages=find_packages(),
    install_requires=["pystac>=0.5.2"],
    extras_require={"https": ["requests>=2.24.0"], "s3": ["boto3>=1.16.6"]},
    keywords=["pystac", "pystac_io", "pystac-io", "s3", "catalog", "STAC"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
