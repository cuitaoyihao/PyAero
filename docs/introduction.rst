Introduction
============

`PyAero <index.html>`_ is an open-source airfoil contour analysis and CFD meshing tool. The main intention of writing the software was to make an easy to use tool for 2D airfoil meshing and subsequent CFD analysis.

`PyAero <index.html>`_, at least at the moment, does not do the CFD calculation itself. At a later stage it might be possible that `PyAero <index.html>`_ will be interfaced (i.e. export meshes in the respective format(s)) with existing open source CFD methods (e.g. `SU2 <http://su2.stanford.edu>`_).

As an initial step towards aerodynamic calculations, a panel method from `AeroPython <http://nbviewer.ipython.org/github/barbagroup/AeroPython/blob/master/lessons/11_Lesson11_vortexSourcePanelMethod.ipynb>`_ (©2014 Lorena A. Barba, Olivier Mesnard) has been implemented. There are minor changes done to the code which are dedicated purely to interface AeroPython with `PyAero <index.html>`_.

In the course of the development it turned out, that airfoil contours (at least legacy airfoils) are often described through a limited number of points (approx. 60 points). When meshing such contours, if not interpolated by splines, the resulting mesh and numerical solutions based on it would end up with artefacts. These would deteriorate the quality of the analysis results.

Therefore, in addition to the mesh generation module, some additional features have been implemented. These features are intended to be able to analyze and improve the airfoil contour. The improvement process is supported by point insertion and spline interpolation techniques. First and second derivatives of the contour allow for control of the contour as well as curvature smoothness.

To reflect *real* shapes, an option for creating a trailing edge and blendig it to the contour is implemented.
