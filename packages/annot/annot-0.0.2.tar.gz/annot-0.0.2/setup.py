import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="annot",
    version="0.0.2",
    author="Mike Claffey",
    author_email="mikeclaffey@yahoo.com",
    description="Annotate data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mclaffey/annot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    # Datatables
    package_data={'annot': ['DataTables/*']},

    # executable
    entry_points={
        'console_scripts': [
            'annot = annot.__main__:main',
        ],
    }

)
