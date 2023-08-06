import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="botprint",
	version="1.0.1",
	author="Whitekeks",
	author_email="JanNiklasb1998@gmail.com",
	description="A small Package for printing in Discord",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/Whitekeks/botprint.git",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
)