SHELL = /bin/sh
PREFIX = $(PWD)/gamer_install
FETK_INCLUDE = $(PREFIX)/include
FETK_LIBRARY = $(PREFIX)/lib
PYTHON = /opt/local/bin/python3.4
LDFLAGS = -L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib
# DYLD_LIBRARY_PATH = $(PREFIX)/lib:$DYLD_LIBRARY_PATH
# PYTHONPATH = $(PREFIX)/lib/python3.4/site-packages:$PYTHONPATH

.PHONY: all
all: maloc gamer gamer_swig gamer_tools upy

.PHONY: maloc
maloc:
	@ cd maloc ; ./configure --prefix=$(PREFIX) ; $(MAKE) ; $(MAKE) install

.PHONY: gamer
gamer: maloc
	@ cd gamer ; ./configure --prefix=$(PREFIX) ; $(MAKE) ; $(MAKE) install

.PHONY: gamer_swig
gamer_swig: gamer
	@ cd gamer/swig ; ./configure --prefix=$(PREFIX) LDFLAGS="-L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib" ; $(MAKE) ; $(MAKE) install

.PHONY: gamer_tools
gamer_tools: gamer
	@ cd gamer/tools/ImproveSurfMesh ; ./configure --prefix=$(PREFIX) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/MolecularMesh ; ./configure --prefix=$(PREFIX) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/GenerateMesh ; ./configure --prefix=$(PREFIX) ; $(MAKE) ; $(MAKE) install

.PHONY: upy
upy:
	@ cd upy ; $(PYTHON) setup.py install --prefix=$(PREFIX)

clean:
	@ cd maloc; $(MAKE) clean
	@ cd gamer; $(MAKE) clean
	@ cd gamer/swig; $(MAKE) clean
	@ cd gamer/tools/ImproveSurfMesh; $(MAKE) clean
	@ cd gamer/tools/MolecularMesh; $(MAKE) clean
	@ cd gamer/tools/GenerateMesh; $(MAKE) clean
	@ cd upy; rm -rf build

distclean: clean
	rm -rf gamer_install
