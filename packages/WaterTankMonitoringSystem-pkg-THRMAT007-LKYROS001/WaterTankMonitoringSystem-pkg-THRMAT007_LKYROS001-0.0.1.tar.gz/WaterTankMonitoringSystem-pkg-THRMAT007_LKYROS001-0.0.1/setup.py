import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WaterTankMonitoringSystem-pkg-THRMAT007_LKYROS001", # Replace with your own username
    version="0.0.1",
    author="THRMAT007",
    author_email="THRMAT007&@myuct.ac.za",
    description="Design project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/THRMAT007/EEE3097SProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)