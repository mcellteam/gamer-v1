SHELL := /bin/sh
BUILD_DIR := $(PWD)/gamer_build_static
export FETK_INCLUDE := $(BUILD_DIR)/include
export FETK_LIBRARY := $(BUILD_DIR)/lib

# On a Linux platform, uncomment these lines and adjust as needed:
export PYTHON := /opt/python3.4/bin/python3.4
export LD_LIBRARY_PATH := $(BUILD_DIR)/lib:$(LD_LIBRARY_PATH)
LDFLAGS := "-L/opt/python3.4/lib/"
INSTALL_DIR := ~/.config/blender/2.77

# On a MacOSX platform, uncomment these lines and adjust as needed:
#export PYTHON := /opt/local/bin/python3.4
#export DYLD_LIBRARY_PATH := $(BUILD_DIR)/lib:$(DYLD_LIBRARY_PATH)
#LDFLAGS := -L/opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib
#INSTALL_DIR := ~/Library/Application\ Support/Blender/2.77

export PYTHONPATH := $(BUILD_DIR)/lib/python3.4/site-packages:$(PYTHONPATH)


all: maloc gamer gamer_swig gamer_tools

.PHONY: maloc gamer gamer_swig upy

maloc:
	@ cd maloc ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer: maloc
	@ cd gamer ; ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer_swig: gamer
	echo "LDFLAGS is set to:  " $(LDFLAGS)
	echo "LD_LIBRARY_PATH is set to:  " $(LD_LIBRARY_PATH)
	@ cd gamer/swig ; ./configure --enable-static --prefix=$(BUILD_DIR) LDFLAGS=$(LDFLAGS) ; $(MAKE) ; $(MAKE) install

gamer_tools: gamer
	@ cd gamer/tools/ImproveSurfMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/MolecularMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/GenerateMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install


install:
	@ mkdir -p $(INSTALL_DIR)/scripts/addons
	@ mkdir -p $(INSTALL_DIR)/scripts/modules
	@ cp -r ./gamer_addon $(INSTALL_DIR)/scripts/addons/
	@ cp -r $(BUILD_DIR)/lib/python3.4/site-packages/gamer $(INSTALL_DIR)/scripts/modules/

clean:
	@ cd maloc; $(MAKE) -k clean
	@ cd gamer; $(MAKE) -k clean
	@ cd gamer/swig; $(MAKE) -k clean
	@ cd gamer/tools/ImproveSurfMesh; $(MAKE) -k clean
	@ cd gamer/tools/MolecularMesh; $(MAKE) -k clean
	@ cd gamer/tools/GenerateMesh; $(MAKE) -k clean

distclean:
	rm -rf $(BUILD_DIR)
	@ $(MAKE) -k clean
