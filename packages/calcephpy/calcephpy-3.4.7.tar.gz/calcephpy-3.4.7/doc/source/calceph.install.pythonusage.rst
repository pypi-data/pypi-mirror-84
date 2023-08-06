Installation
************

The following section describes the installation of the **Python** interface of the library.
If you want to install the interface for another programming language, you have to follow the instructions of the manual of that language.  

Instructions
============

The python interface of the library should be installed using the  package management system **pip** on all operating systems : Windows and Unix-like system (Linux, Mac OS X, BSD, Cygwin, ...).

A python interpreter, compliant at least with with the Python 2.6 or Python 3.0  specifications, and the package Cython, setuptools and numpy are required to install the python interface of the library.

Depending on your python installation, the command **pip** may be replaced by **pip3**. If you use the distribution *anaconda*, you should use the pip command of that distribution.

The steps are :

.. highlight::  bash

- Install the requirements

    ::
    
        pip install Cython setuptools numpy


- Install the library

    ::

        pip install calcephpy
 
 .. highlight::  none
