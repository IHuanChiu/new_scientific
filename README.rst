=====================================
The Analyzer Framework
=====================================

.. contents:: Table of contents

Introduction
============

This is the analysis framework for new scientific work. 
YOU need to use >python3.9
pip install root_numpy
pip install scipy
pip install numpy

imageAna
==================

Main workspace for dsd analysis including 2D and 3D images.

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

ANLNext
==================
The ANL tool for DSD made by Takahashi-ken. Check `here <https://github.com/odakahirokazu/ANLNext>`_ 

CdTe123
====================================

This is CdTe123 data recored at J-PARC.

DSDAnalysisTools
==========================================

The main analysis framework for uploading to git.

GeAnalysis
================================

This tools is using to transfer pha file to root file. And the ``macro`` in the framework is used to make spectrum.

TRIM_simulation
============================

To compare the simulation result from Geant4, the TRIM is used.
