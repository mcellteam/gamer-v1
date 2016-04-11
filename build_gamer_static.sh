#!/bin/sh

export PREFIX=$PWD/gamer_build_static
export FETK_INCLUDE=$PREFIX/include
export FETK_LIBRARY=$PREFIX/lib
export PYTHON=/usr/bin/python3.4
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH
#export DYLD_LIBRARY_PATH=$PREFIX/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=$PREFIX/lib/python3.4/site-packages:$PYTHONPATH

(cd maloc ; ./configure --enable-static --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer ; ./configure --enable-static --prefix=$PREFIX ; make clean ; make ; make install)
#(cd gamer/swig ; ./configure --enable-static --prefix=$PREFIX LDFLAGS="-L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib" ; make clean ; make ; make install)
(cd gamer/swig ; ./configure --enable-static --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer/tools/ImproveSurfMesh ; ./configure --enable-static --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer/tools/MolecularMesh ; ./configure --enable-static --prefix=$PREFIX ; make clean ; make ; make install)
(cd gamer/tools/GenerateMesh ; ./configure --enable-static --prefix=$PREFIX ; make clean ; make ; make install)
# (cd upy ; $PYTHON setup.py install --prefix=$PREFIX)

