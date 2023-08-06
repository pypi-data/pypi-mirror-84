import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emre", # Project name
    version="1.0.14",
    author="Peter Van Horne",
    author_email="petervh@cisco.com",
    description="Embedded Machine Reasoning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires= ['ncclient==0.6.9', 'clipspy==0.3.3', 'xmltodict', 'pexpect', 'regex'],
    py_modules=['emreclass', 'genie_parsers', 'runemre'],
    entry_points={
        'console_scripts': [
            # Run tests, suites, and profiles from the console
            'runemre = runemre:main'
        ],
    },
)
