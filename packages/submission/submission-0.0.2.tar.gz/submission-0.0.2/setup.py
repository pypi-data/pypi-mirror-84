from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
      name='submission',
      version='0.0.2',
      long_description=long_description,
      long_description_context_type="text/markdown",
      description='Takes algorithm, train, test, X variables, Y variables, column names required for submission and name of submission file as input and produces an output csv for submitting in the competition.',
      py_modules=["submission"],
      package_dir={'':'package'},
      )
