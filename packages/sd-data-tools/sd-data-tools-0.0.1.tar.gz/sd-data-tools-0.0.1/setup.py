import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name="sd-data-tools",
  version="0.0.1",
  author="Siddhant A. Deshmukh",
  author_email="siddhant593@gmail.com",
  description="A collection of useful plotting, analysis and manipulation scripts for data science.",
  long_description=long_description,
  url="https://github.com/SiddhantDeshmukh/usefulScripts",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.6"
)
