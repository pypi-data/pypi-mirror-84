from setuptools import setup

with open("./README.md") as readme:
    desc = readme.read()

setup(
    name="sshdjup",
    version="0.5",
    long_description=desc,
    long_description_content_type="text/markdown",
    packages=["sshdjup"],
    author_email="yariksvitlitskiy81@gmail.com",
    zip_safe=False
)
