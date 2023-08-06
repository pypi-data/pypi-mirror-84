import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="gdplot",
    version="0.0.1",
    author="Suman Kumar",
    author_email="sumankumar0091@gmail.com",
    description="Plot Chart from your Google Sheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sumankumar0091/greendeck_plot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = ['Chart', 'gsheet', 'plot'],

    install_requires=[
        'pandas',
        'matplotlib',
        'gsheets'
    ]
)