README
===================

This is the README file for the Python module ``hiegeo``, described in
the manuscript *A new perspective to model subsurface stratigraphy in
alluvial hydrogeological basins, introducing geological hierarchy and
relative chronology* by C.Zuffetti, A.Comunian, R.Bersezio and
P.Renard, Computers and Geosciences, DOI: `10.1016/j.cageo.2020.104506 <https://doi.org/10.1016/j.cageo.2020.104506>`_.

Hereinafter we report a brief "quick start guide".  For additional
information about how to install and run the provided Python scripts,
please check out the full documentation from `this link
<https://hiegeo.readthedocs.io/en/latest/index.html>`_ can be also
downloaded as PDF, EPUB and also as a local HTML archive `here
<https://readthedocs.org/projects/hiegeo/downloads/>`_.


Installation
=========================

``hiegeo`` is available at the `Python Package Index repository
<https://pypi.org/project/hiegeo/>`_. Therefore, in can be easily
installed (together with its dependencies) with the command::

    pip install hiegeo

Alternatively, if you prefer to download the sources from
`https://bitbucket.org/alecomunian/hiegeo
<https://bitbucket.org/alecomunian/hiegeo>`_ in "edit mode" you can:

1) Clone or download this repository on your hard drive.
2) If required, unpack it and ``cd hiegeo``.
3) Inside the project directory, from the command line::

     pip install -e .

4) To check if it worked, open a Python terminal and try::

     import hiegeo

Examples
==============================

To test the package, move to the folder ``examples`` and there, from
the command line, run one of the two provided demonstration scripts.
For example::

  ./hiegeo_test-simple.py

and hit <Enter>.
On Linux you will probably need to give execution rights to the file, like this::

  chmod +x hiegeo_test-simple.py

    

