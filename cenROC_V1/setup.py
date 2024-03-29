import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "cenroc",
    version = "0.0.4",
    author = "Yury Moskaltsov,Miguel Pereira",
    author_email = "yury.moskaltsov@plaindata.ai",
    description = "Calculation of censored ROC curve",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # url = "package URL",
    # project_urls = {
    #     "Bug Tracker": "package issues URL",
    # },
    install_requires=['numpy', 'pandas', 'matplotlib', 'scipy','statsmodels'],
    keywords=['python', 'cenROC', 'survival'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)




