import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyinsight-depositor-firestore",
    version="0.0.1",
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