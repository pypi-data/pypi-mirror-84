import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name='random_root_locus_generator',    # This is the name of your PyPI-package.
    version='1.0.6',
    url='https://github.com/ryanGT/random_root_locus_generator',
    author='Ryan Krauss',
    author_email='ryanwkrauss@gmail.com',
    description="package for generating random root locus problems intelligently",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
