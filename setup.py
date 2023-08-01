from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.8'
DESCRIPTION = 'Blob mapping utility for easy translation between azure urls and local paths'
LONG_DESCRIPTION = 'Blob mapping utility for easy translation between azure urls and local paths'

# Setting up
setup(
    name="blob_mounting_helper_utility",
    version=VERSION,
    author="Ivica Matic",
    author_email="<ivica.matic@spatialdays.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['azure-storage-blob==12.17.0'],
    keywords=['python', 'azure', 'blob', 'mount'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)