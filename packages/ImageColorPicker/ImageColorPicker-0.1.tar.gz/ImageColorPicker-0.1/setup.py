import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ImageColorPicker',
    version='0.1',
    author='Mark Tamarov',
    author_email="marktamarov2001@gmail.com",
    description="Simple class for finding dominant colors from image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mar4elkin/ImageColorPicker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)