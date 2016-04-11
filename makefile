SHELL = /bin/sh
BUILD_DIR = $(PWD)/gamer_build_static
export FETK_INCLUDE = $(BUILD_DIR)/include
export FETK_LIBRARY = $(BUILD_DIR)/lib
#export PYTHON = /usr/bin/python3.4
export PYTHON = /opt/local/bin/python3.4
LDFLAGS = \"-L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib\"
#LDFLAGS = \"\"
#INSTALL_DIR = ~/Library/Application\ Support/Blender/2.75
INSTALL_DIR = ~/.config/blender/2.76

DYLD_LIBRARY_PATH = $(BUILD_DIR)/lib:$DYLD_LIBRARY_PATH
PYTHONPATH = $(BUILD_DIR)/lib/python3.4/site-packages:$PYTHONPATH

all: maloc gamer gamer_swig gamer_tools upy

.PHONY: maloc gamer upy

maloc:
	@ cd maloc ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer:
	@ cd gamer ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer_swig:
#	@ cd gamer/swig ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/swig ; $(MAKE) clean ; ./configure --prefix=$(BUILD_DIR) LDFLAGS=$(LDFLAGS) ; $(MAKE) ; $(MAKE) install

gamer_tools:
	@ cd gamer/tools/ImproveSurfMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/MolecularMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/GenerateMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

upy:
	@ cd upy ; $(PYTHON) setup.py install --prefix=$(BUILD_DIR)

install:
	@ mkdir -p $(INSTALL_DIR)
	@ cp ./gamer/tools/blender/mesh_gamer_addon.py $(INSTALL_DIR)/scripts/addons/
	@ cp -r ./gamer_addon $(INSTALL_DIR)/scripts/addons/
	@ cp -r $(BUILD_DIR)/lib/python3.4/site-packages/gamer $(INSTALL_DIR)/scripts/modules/
#	@ cp -r $(BUILD_DIR)/lib/python3.4/site-packages/upy $(INSTALL_DIR)/scripts/modules/

clean:
	@ cd maloc; $(MAKE) clean
	@ cd gamer; $(MAKE) clean
	@ cd gamer/swig; $(MAKE) clean
	@ cd gamer/tools/ImproveSurfMesh; $(MAKE) clean
	@ cd gamer/tools/MolecularMesh; $(MAKE) clean
	@ cd gamer/tools/GenerateMesh; $(MAKE) clean
	@ cd upy; rm -rf build

distclean: clean
	rm -rf $(BUILD_DIR)
