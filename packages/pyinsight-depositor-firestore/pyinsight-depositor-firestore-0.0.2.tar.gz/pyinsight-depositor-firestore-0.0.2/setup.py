import codecs
import os.path
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split('"')[1]
    else:
        raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name="pyinsight-depositor-firestore",
    version=get_version("pyinsight_depositor_firestore/__init__.py"),
    author="Soral",
    author_email="soral@x-i-a.com",
    description="Insight Depositor Module Firestore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/X-I-A/pyinsight-depositor-firestore",
    packages=['pyinsight_depositor_firestore'],
    install_requires=[
        'pyinsight',
        'google-auth',
        'google-cloud-firestore',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)