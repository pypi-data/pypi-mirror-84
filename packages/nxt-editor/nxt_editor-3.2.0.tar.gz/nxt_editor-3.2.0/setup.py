import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nxt_editor",
    version="3.2.0",
    author="the nxt contributors",
    author_email="author@example.com",
    description="The nxt editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SunriseProductions/nxt",
    packages=setuptools.find_packages(),
    python_requires='>=2.7, <3'
)