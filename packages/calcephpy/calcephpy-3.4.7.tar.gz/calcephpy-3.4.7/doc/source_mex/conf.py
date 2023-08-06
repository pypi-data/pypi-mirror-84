
import sys
import os

exec(open(os.path.abspath("../source/confcommon.py")).read())

primary_domain = 'mat'

# General information about the project.
project = u'CALCEPH  - Octave/Matlab language'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['condsingle', 'condsingle/calceph.single.rst', 'calceph.install.pythonusage.rst', 'calceph.install.cusage.rst' ]


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'calceph.tex', u'CALCEPH - Octave/Matlab language',
     u'M. Gastineau, J. Laskar, A. Fienga, H. Manche', 'manual'),
]

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'calceph', u'CALCEPH - Octave/Matlab language',
     author, 'calceph', 'CALCEPH - Octave/Matlab language.',
     'Miscellaneous'),
]


def setup(app):
    app.add_config_value('calcephapi', 'Mex', 'env')


rst_epilog = """
.. |API| replace:: Octave/Matlab
.. |supportedspk| replace:: 1, 2, 3, 5, 8, 9, 12, 13, 17, 18, 20, 21, 102, 103 and 120
.. |LIBRARYNAME| replace:: CALCEPH Library
.. |LIBRARYSHORTNAME| replace:: CALCEPH
.. |EMAIL| replace:: inpop.imcce@obspm.fr
.. |eph| replace:: *self*
.. |ephemerisdescriptoreph| replace:: the ephemeris descriptor 
.. |menu_calceph_open| replace:: CalcephBin.open
.. |calceph_open| replace:: :mat:meth:`CalcephBin.open()`
.. |menu_calceph_open_array| replace:: CalcephBin.open
.. |calceph_open_array| replace:: :mat:meth:`CalcephBin.open()`
.. |menu_calceph_close| replace:: CalcephBin.close
.. |calceph_close| replace:: :mat:meth:`CalcephBin.close()`
.. |menu_calceph_prefetch| replace:: CalcephBin.prefetch
.. |calceph_prefetch| replace:: :mat:meth:`CalcephBin.prefetch()`
.. |menu_calceph_isthreadsafe| replace:: CalcephBin.isthreadsafe
.. |calceph_isthreadsafe| replace:: :mat:meth:`CalcephBin.isthreadsafe()`
.. |menu_calceph_compute| replace:: CalcephBin.compute
.. |calceph_compute| replace:: :mat:meth:`CalcephBin.compute()`
.. |menu_calceph_compute_unit| replace:: CalcephBin.compute_unit
.. |calceph_compute_unit| replace:: :mat:meth:`CalcephBin.compute_unit()`
.. |menu_calceph_getconstant| replace:: CalcephBin.getconstant
.. |calceph_getconstant| replace:: :mat:meth:`CalcephBin.getconstant()`
.. |menu_calceph_getconstantsd| replace:: CalcephBin.getconstantsd
.. |calceph_getconstantsd| replace:: :mat:meth:`CalcephBin.getconstantsd()`
.. |menu_calceph_getconstantvd| replace:: CalcephBin.getconstantvd
.. |calceph_getconstantvd| replace:: :mat:meth:`CalcephBin.getconstantvd()`
.. |menu_calceph_getconstantss| replace:: CalcephBin.getconstantss
.. |calceph_getconstantss| replace:: :mat:meth:`CalcephBin.getconstantss()`
.. |menu_calceph_getconstantvs| replace:: CalcephBin.getconstantvs
.. |calceph_getconstantvs| replace:: :mat:meth:`CalcephBin.getconstantvs()`
.. |menu_calceph_getconstantcount| replace:: CalcephBin.getconstantcount
.. |calceph_getconstantcount| replace:: :mat:meth:`CalcephBin.getconstantcount()`
.. |menu_calceph_getconstantindex| replace:: CalcephBin.getconstantindex
.. |calceph_getconstantindex| replace:: :mat:meth:`CalcephBin.getconstantindex()`
.. |menu_calceph_gettimescale| replace:: CalcephBin.gettimescale
.. |calceph_gettimescale| replace:: :mat:meth:`CalcephBin.gettimescale()`
.. |menu_calceph_gettimespan| replace:: CalcephBin.gettimespan
.. |calceph_gettimespan| replace:: :mat:meth:`CalcephBin.gettimespan()`
.. |menu_calceph_getfileversion| replace:: CalcephBin.getfileversion
.. |calceph_getfileversion| replace:: :mat:meth:`CalcephBin.getfileversion()`
.. |menu_calceph_getpositionrecordcount| replace:: CalcephBin.getpositionrecordcount
.. |calceph_getpositionrecordcount| replace:: :mat:meth:`CalcephBin.getpositionrecordcount()`
.. |menu_calceph_getpositionrecordindex| replace:: CalcephBin.getpositionrecordindex
.. |calceph_getpositionrecordindex| replace:: :mat:meth:`CalcephBin.getpositionrecordindex()`
.. |menu_calceph_getorientrecordcount| replace:: CalcephBin.getorientrecordcount
.. |calceph_getorientrecordcount| replace:: :mat:meth:`CalcephBin.getorientrecordcount()`
.. |menu_calceph_getorientrecordindex| replace:: CalcephBin.getorientrecordindex
.. |calceph_getorientrecordindex| replace:: :mat:meth:`CalcephBin.getorientrecordindex()`
.. |menu_calceph_orient_unit| replace:: CalcephBin.orient_unit
.. |calceph_orient_unit| replace:: :mat:meth:`CalcephBin.orient_unit()`
.. |menu_calceph_rotangmom_unit| replace:: CalcephBin.rotangmom_unit
.. |calceph_rotangmom_unit| replace:: :mat:meth:`CalcephBin.rotangmom_unit()`
.. |menu_calceph_compute_order| replace:: CalcephBin.compute_order
.. |calceph_compute_order| replace:: :mat:meth:`CalcephBin.compute_order()`
.. |menu_calceph_orient_order| replace:: CalcephBin.orient_order
.. |calceph_orient_order| replace:: :mat:meth:`CalcephBin.orient_order()`
.. |menu_calceph_rotangmom_order| replace:: CalcephBin.rotangmom_order
.. |calceph_rotangmom_order| replace:: :mat:meth:`CalcephBin.rotangmom_order()`
.. |menu_calceph_sopen| replace:: CalcephBin.sopen
.. |calceph_sopen| replace:: :mat:meth:`CalcephBin.sopen()`
.. |menu_calceph_sclose| replace:: CalcephBin.sclose
.. |calceph_sclose| replace:: :mat:meth:`CalcephBin.sclose()`
.. |menu_calceph_scompute| replace:: CalcephBin.scompute
.. |calceph_scompute| replace:: :mat:meth:`CalcephBin.scompute()`
.. |menu_calceph_sgetconstant| replace:: CalcephBin.sgetconstant
.. |calceph_sgetconstant| replace:: :mat:meth:`CalcephBin.sgetconstant()`
.. |menu_calceph_sgetconstantcount| replace:: CalcephBin.sgetconstantcount
.. |calceph_sgetconstantcount| replace:: :mat:meth:`CalcephBin.sgetconstantcount()`
.. |menu_calceph_sgetconstantindex| replace:: CalcephBin.sgetconstantindex
.. |calceph_sgetconstantindex| replace:: :mat:meth:`CalcephBin.sgetconstantindex()`
.. |menu_calceph_seterrorhandler| replace:: calceph_seterrorhandler
.. |calceph_seterrorhandler| replace:: :mat:meth:`calceph_seterrorhandler()`
.. |menu_calceph_getversion_str| replace:: calceph_getversion_str
.. |menu_Headers_and_Libraries| replace:: Package
.. |CALCEPH_UNIT_AU| replace:: :mat:attr:`UNIT_AU`
.. |CALCEPH_UNIT_KM| replace:: :mat:attr:`UNIT_KM`
.. |CALCEPH_UNIT_DAY| replace:: :mat:attr:`UNIT_DAY`
.. |CALCEPH_UNIT_SEC| replace:: :mat:attr:`UNIT_SEC`
.. |CALCEPH_UNIT_RAD| replace:: :mat:attr:`UNIT_RAD`
.. |CALCEPH_OUTPUT_EULERANGLES| replace:: :mat:attr:`OUTPUT_EULERANGLES`
.. |CALCEPH_OUTPUT_NUTATIONANGLES| replace:: :mat:attr:`OUTPUT_NUTATIONANGLES`
.. |CALCEPH_USE_NAIFID| replace:: :mat:attr:`USE_NAIFID`
.. |retfuncfails0| replace:: returns 0 or an exception if an error occurs, otherwise a non-zero value.
.. |funcfails0| replace::  On exit, it returns 0 or an exception if an error occurs, otherwise the return value is a non-zero value.
.. |retfuncfailsNULL| replace:: raises an exception if an error occurs, otherwise a valid object.
.. |funcfailsNULL| replace:: On exit, it raises an exception if an error occurs, otherwise the return value is a valid value.
.. |retfuncfailsnbval| replace:: returns 0 or an exception if an error occurs, otherwise the number of values associated to the constant.
.. |retfuncnotfound0| replace::  returns 0 if the file version was not found, otherwise non-zero value.
.. |funcnotfound0| replace::  On exit, it returns 0 if the file version was not found, otherwise non-zero value.
"""
