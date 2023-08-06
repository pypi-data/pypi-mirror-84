import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Some information about this package
    name = "GoodCalculator",
    version = "0.0.2",
    author = "Joey",
    author_email = "test@gmail.com",
    description = "A calculator",
    long_description = long_description, # use README.md or README.rst file
    long_description_content_type = "text/markdown",
    url = "https://github.com/pypa/sampleproject",
    
    # Tell distutils where are the packages (find __init__.py file)
    # packages=setuptools.find_packages(),
    # or use:
    packages = [
        "GoodCalculator"
    ],
    # Where to find packages
    package_dir = [],
    
    # Standard desciptions for this package to let community members to find projects based on their desired criteria. 
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # Python requirements
    python_requires = '>=3.6',

    # Entry point to use command line
    # you can decide your dir (GoodCalculator_cli) whatever you want
    # <command in console> = <module name>.<some kind of script>:<function>
    entry_points={
        "console_scripts": [
            "cal = GoodCalculator.GoodCalculator_cli:run_cli"
        ]
    }
)