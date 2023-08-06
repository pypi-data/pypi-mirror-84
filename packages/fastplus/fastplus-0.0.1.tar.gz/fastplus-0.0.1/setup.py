import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastplus",
    version="0.0.1",
    install_requires=[
        'Click',
    ],
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        fastplus=fastplus.cli:fastplus
    ''',
    author="Will Johns",
    author_email="will@wcj.dev",
    description="An opinionated expansion of FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MetaBytez/fastplus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
