#!/bin/sh

export PREFIX=$PWD/gamer_build
export FETK_INCLUDE=$PREFIX/include
export FETK_LIBRARY=$PREFIX/lib
export PYTHON=/opt/local/bin/python3.4
export DYLD_LIBRARY_PATH=$PREFIX/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=$PREFIX/lib/python3.4/site-packages:$PYTHONPATH

(cd maloc ; ./configure --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer ; ./configure --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer/swig ; ./configure --prefix=$PREFIX LDFLAGS="-L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib" ; make clean ; make ; make install)
(cd gamer/tools/ImproveSurfMesh ; ./configure --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer/tools/MolecularMesh ; ./configure --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer/tools/GenerateMesh ; ./configure --prefix=$PREFIX ; make clean ; make ; make install)
(cd upy ; $PYTHON setup.py install --prefix=$PREFIX)

