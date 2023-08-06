import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="layersdk", # Replace with your own username
    version="0.0.1",
    author="Layer Co",
    author_email="python-sdk@layer.co",
    description="The Layer SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://layer.co",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
