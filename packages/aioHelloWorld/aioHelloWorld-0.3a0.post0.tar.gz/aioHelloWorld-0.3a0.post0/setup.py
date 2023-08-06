from setuptools import setup


with open("README.md", "r") as read:
      readme = read.read()

setup(name="aioHelloWorld",
      version="0.3a.post0",
      description="This is a asynchronous package for printing hello world",
      long_description=readme,
      long_description_content_type = "text/markdown",
      project_urls={"Issue tracker": "https://github.com/Exainz/aioHelloWorld/issues"},
      author="Exainz",
      packages=["aioHelloWorld"],
      install_requires=[])
