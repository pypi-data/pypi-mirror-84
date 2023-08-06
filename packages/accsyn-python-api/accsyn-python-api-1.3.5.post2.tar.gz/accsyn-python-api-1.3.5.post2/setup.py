import setuptools

with open("README.md", "r") as fh:

	long_description = fh.read()

setuptools.setup(

	 name='accsyn-python-api',  

	 version='1.3.5-2',

	 packages=['accsyn_api'],

	 author="Henrik Norin",

	 author_email="henrik.norin@accsyn.com",

	 description="A Python API for controlling Accsyn fast data delivery software",

	 long_description=long_description,

	 long_description_content_type="text/markdown",

	 url="https://github.com/accsyn/accsyn-python-api.git",

	 classifiers=[

		 "Programming Language :: Python :: 2",

		 "License :: OSI Approved :: MIT License",

		 "Operating System :: OS Independent",

	 ],

 )
