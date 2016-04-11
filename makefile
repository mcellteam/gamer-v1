SHELL = /bin/sh
BUILD_DIR = $(PWD)/gamer_build_static
export FETK_INCLUDE = $(BUILD_DIR)/include
export FETK_LIBRARY = $(BUILD_DIR)/lib
export PYTHON = /usr/bin/python3.4
#export PYTHON = /opt/local/bin/python3.4
LDFLAGS = \"\"
#LDFLAGS = \"-L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib\"
INSTALL_DIR = ~/.config/blender/2.76
#INSTALL_DIR = ~/Library/Application\ Support/Blender/2.75

export LD_LIBRARY_PATH=$(BUILD_DIR)/lib:$LD_LIBRARY_PATH
#export DYLD_LIBRARY_PATH=$(BUILD_DIR)/lib:$DYLD_LIBRARY_PATH
PYTHONPATH = $(BUILD_DIR)/lib/python3.4/site-packages:$PYTHONPATH

all: maloc gamer gamer_swig gamer_tools

.PHONY: maloc gamer gamer_swig upy

maloc:
	@ cd maloc ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer: maloc
	@ cd gamer ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer_swig: gamer
#	@ cd gamer/swig ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/swig ; ./configure --enable-static --prefix=$(BUILD_DIR) LDFLAGS=$(LDFLAGS) ; $(MAKE) ; $(MAKE) install

gamer_tools: gamer
	@ cd gamer/tools/ImproveSurfMesh ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/MolecularMesh ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/GenerateMesh ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install


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

distclean: clean
	rm -rf $(BUILD_DIR)
