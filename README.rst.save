=====================================
The DC760 Analyzer Framework
=====================================

.. contents:: Table of contents

Introduction
============

This is the analysis framework for data of the drift-chamber detector. 
With the framework provided, the several root files and figures can be produced for checking recored data. 
Currently the framework provide:

tou can execute in the run folder and the output will be placed in same folder.
The source codes are put in the macro and binary2root folders.

 * ``run`` folder : to execute and the output will be placed in this folder (default). 
 * ``macro`` and ``binary2root`` folders : the source codes.

How to get started
==================

Simply to make sure your workspace::

  mkdir MyDC760Analysis
  cd MyDC760Analysis 
  git clone https://gitlab.com/mulexsea/dc760-analyzer.git

Once the clone is finished, the framework can be compile with following command::

  cd macro 
  make
  cd ../binary2root 
  make

configuration
-------------

After the compilation, the four options are available in the ``run`` folder. 

===========  ===========================================================================
Run Option   Description
===========  ===========================================================================
binary2root  to transfer the dc760 data to root file
run_check    to check the adc, tdc, hit position and drift time of recored data
run          reconstructe trajectory of the input particle by ROOT TMinuit
monitor.sh   monitor operation during data taking (normally, it is not need in analysis step)
===========  ===========================================================================

Running the binary data to root file
====================================

Switch to the ``run`` folder and call the ``binary2root`` e.g.::

  cd MyDC760Analysis/run
  ./binary2root <path/to/data>/<name of dc760 data> <name of output root file> <number of samples; default is 31> 

where the path of input data and name of output root file are need for ``binary2root``. 
The number of sample is used for window size during data taking.
The default input path is ``run/data`` and the default window size is 31.
The output root file will be placed in the folder named ``run/root``.

Running figure maker to check recored data
==========================================

In the same ``run`` folder and call the ``run_check`` e.g.::

  ./run_check <path of input root file> <name of output file> <number of figures> <plotting level>

where the path/name of input file is the root file we got in `Running the binary data to root file`_.
The output file is used to save hit position and figures. (default path for output file is ``run/output``)
Considering the long rinning time problem, we need to specify the number of figures we want to check.
For instance, the package only make adc and tdc plots for last two event once we set the ``number of figures`` is 2.
The plotting level is a switch to decide to draw large number of drift time plots or not. (2 is yes; 1 is no; other value is not available yet)

Running trajectory recontruction
================================

The analysis code ``tran.C`` provides trajectory recontruction of input beam and hit map of DC760.
You can call the ``run`` command to run this analysis code e.g.::
 
 ./run <path of input root file>

The output file will be placed in ``run/output`` and named as ``drift_plot.root``. 
The ntuple stores several variables such as drift_time, drift_radius (means drift distance), hit position and DCA in the ``Eventtree``.

You can deal with the ntuple for the further analysis (for instance, XT-curve).
The "plot" in tran class is a function to make simple hit map.
This script still need to be optimized.

Running monitor
============================

Normally, it is not available in your workspace. It only can run during data taking period.::

 source monitor.sh
  
This script will run `Running the binary data to root file`_ and `Running figure maker to check recored data`_ every 1 minutes (default),
and then copy the all output file to the site of hori computer.
The all figures made for new recored data can be checked in the here:

* `DC760 monitor <http://prism.phys.sci.osaka-u.ac.jp/~t-hori/>`_
