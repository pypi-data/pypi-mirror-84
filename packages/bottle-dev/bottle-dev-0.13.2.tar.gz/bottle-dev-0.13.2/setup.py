#!/usr/bin/env python3 -B -u
import sys
from setuptools import setup
import bottle
setup(name="bottle-dev",
	version=bottle.__version__,
	description="Fast and simple WSGI-framework for small web-applications.",
	long_description=bottle.__doc__,
	long_description_content_type="text/markdown",
	url="http://bottlepy.org",
	py_modules=["bottle"],
	scripts=["bottle.py"],
	license="MIT",
	platforms="any",
	classifiers=["Development Status :: 4 - Beta",
	 "Operating System :: OS Independent",
	 "Intended Audience :: Developers",
	 "License :: OSI Approved :: MIT License",
	 "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
	 "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
	 "Topic :: Internet :: WWW/HTTP :: WSGI",
	 "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
	 "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
	 "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
	 "Topic :: Software Development :: Libraries :: Application Frameworks",
	 "Programming Language :: Python :: 3"],
)
