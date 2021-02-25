.. TARCH documentation master file, created by
   sphinx-quickstart on Thu May  7 08:05:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TARCH's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

TARCH
============
What is TARCH?
++++++++++++++++++++++++++++++++

.. image:: images/purpose.svg
   :alt: Purpose of TARCH

TARCH is a framework written in Python 3.8 for turning lots of messy real-world data into clean, documented and usable data for analysis. Special attention is paid to repeatability, self documentation and ease of use.

Why should I use TARCH?
++++++++++++++++++++++++++++++++
.. image:: images/badExample.svg
   :alt: TARCH is powered by modules

When working on a long project with lot's of people coming and going, it is very easy to end up with a mess of scripts in a folder that need to be run in an arcane order that no one *truely* understands. On top of organizational concerns, documentation and understanding of raw data/processed data can be a monumetal task on it's own. And we haven't even mentioned the trials and tribulations of standardizing workflows! Worry not, TARCH is here to help.

.. image:: images/modules.svg
   :alt: TARCH is powered by modules

The goal of TARCH is to keep the simplicity and immediate ease-of-use of the "folder of scripts" method while providing structure and standardization to make scientists life easier when it's time to replicate, check or verify their work. Additionally, TARCH is designed for an ever changing lab - startup is quick and easy so summer interns/research assistants can get working without a steep learning curve.

.. image:: images/dataUtils.svg
   :alt: TARCH provides utilities, logging and structure to modules

TARCH provides three sets of built in features - Logging, Validation and Utilities. Logging is straight forward - it provides a common interface to modules so that (a) you save time by not reimplementing it and (b) files written by different people output logs that are cohesive. Utilities provides >60 functions for common data manipulation tasks (especially those related to cleaning poorly formatted data). Validation [WIP] reads a schema file and is used by main to validate the output of modules to ensure data is formatted correctly and consistently.


Structure of TARCH
+++++++++++++++++++++++++++++++

.. image:: images/detailed-composition.svg
   :alt: Structure of TARCH

The individual components of TARCH are described below. Sphinx is used to autogenerate documentation from inline docustrings. 

DataUtils
============
.. automodule:: dataUtils
   :members:

Dev
===========
.. autoclass:: testModuleNoData.TestClass
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
