#!/bin/sh
# -----------------------------------------------------------------------------
#
# Copyright (c) 2009 - 2012 Chris Martin, Kasia Boronska, Jenny Young,
# Peter Jimack, Mike Pilling
#
# Copyright (c) 2017 Sam Cox, Roberto Sommariva
#
# This file is part of the AtChem2 software package.
#
# This file is covered by the MIT license which can be found in the file
# LICENSE.md at the top level of the AtChem2 distribution.
#
# -----------------------------------------------------------------------------

# Makefile for AtChem2

# choose fortran compiler
# 1. "gnu" for gfortran
# 2. "intel" for ifort
FORTC = "gnu"

# set paths to the dependencies
# N.B.: use the full path, not the relative path
CVODELIB     = ${HOME}/atchem-lib/cvode/lib
OPENLIBMDIR  = ${HOME}/atchem-lib/openlibm-0.4.1
FRUITDIR     = ${HOME}/atchem-lib/fruit_3.4.3


# default location of the chemical mechanism shared library (mechanism.so)
# use the second argument of the build script to override $SHAREDLIBDIR
SHAREDLIBDIR = model/configuration

# ================================================================== #
# DO NOT MODIFY BELOW THIS LINE
# ================================================================== #

.SUFFIXES:
.SUFFIXES: .f90 .o
.PHONY: all test

# detect operating system
OS := $(shell uname -s)

# if on Travis
ifeq ($(TRAVIS),true)
ifeq ($(TRAVIS_OS_NAME),linux)
# if linux, pass gfortran
FORT_COMP    = gfortran
FORT_LIB     = ""
else
# if macOS, pass homebrew gfortran
FORT_COMP    = /usr/local/Cellar/gcc@4.9/4.9.4_2/bin/gfortran-4.9
FORT_LIB     = /usr/local/Cellar/gcc@4.9/4.9.4_2/lib/gcc/4.9
endif
# if not on Travis, set the fortran compiler
else
ifeq ($(FORTC),"gnu")
FORT_COMP    = gfortran
FORT_LIB     = ""
endif
ifeq ($(FORTC),"intel")
FORT_COMP    = ifort
FORT_LIB     = ""
endif
endif

# set compilation flags for each compiler
ifeq ($(FORT_COMP),gfortran)
FFLAGS       =  -fprofile-arcs -ftest-coverage -ffree-form -fimplicit-none -Wall -Wpedantic -fcheck=all -fPIC
FSHAREDFLAGS =  -ffree-line-length-none -ffree-form -fimplicit-none -Wall -Wpedantic -Wno-unused-dummy-argument -fcheck=all -fPIC -shared
LIBDIR       =  /usr/lib/:$(CVODELIB)
endif
ifeq ($(FORT_COMP),ifort)
FFLAGS       = -free -warn
FSHAREDFLAGS =
LIBDIR       =
endif

# set rpath flag
ifeq ($(OS),Linux)
RPATH_OPTION = -R
else
RPATH_OPTION = -rpath
endif

# set other compiler flags
LDFLAGS = -L$(CVODELIB) -L$(OPENLIBMDIR) -Wl,$(RPATH_OPTION),$(LIBDIR):$(OPENLIBMDIR) -lopenlibm -lsundials_fcvode -lsundials_cvode -lsundials_fnvecserial -lsundials_nvecserial -ldl

# object files and source files directories
OBJ = obj
SRC = src

# executable
AOUT = atchem2

# source files
UNITTEST_SRCS = $(SRC)/dataStructures.f90 $(SRC)/argparse.f90 $(SRC)/interpolationFunctions.f90 $(SRC)/configFunctions.f90 $(SRC)/inputFunctions.f90 $(SRC)/outputFunctions.f90 $(SRC)/atmosphereFunctions.f90 $(SRC)/solarFunctions.f90 $(SRC)/constraintFunctions.f90 $(SRC)/solverFunctions.f90 $(SRC)/parameterModules.f90
SRCS = $(UNITTEST_SRCS) $(SRC)/atchem2.f90

# prerequisite is $(SRCS), so this will be rebuilt everytime any source file in $(SRCS) changes
$(AOUT): $(SRCS)
	$(FORT_COMP) -o $(AOUT) -J$(OBJ) -I$(OBJ) $(SRCS) $(FFLAGS) $(LDFLAGS)

# setup FRUIT
UNITTESTDIR = travis/unit_tests
fruit_code = $(FRUITDIR)/src/fruit.f90
unittest_code = $(UNITTEST_SRCS) $(shell ls travis/unit_tests/*_test.f90 )
unittest_code_gen = $(UNITTESTDIR)/fruit_basket_gen.f90 $(UNITTESTDIR)/fruit_driver_gen.f90
all_unittest_code = $(fruit_code) $(unittest_code) $(unittest_code_gen)
fruit_driver = $(UNITTESTDIR)/fruit_driver.exe

# copy fruit_generator.rb to the unit tests directory and replace the path of FRUIT with $(FRUITDIR)
$(UNITTESTDIR)/fruit_basket_gen.f90 : $(unittest_code)
	@cp travis/fruit_generator.rb $(UNITTESTDIR)
	@cd $(UNITTESTDIR); sed -i "18s,.*,load \"$(FRUITDIR)/rake_base.rb\"," fruit_generator.rb; ruby fruit_generator.rb

# build fruit_driver.exe from the individual unit tests
$(fruit_driver) : $(all_unittest_code)
	$(FORT_COMP) -o $(fruit_driver) -J$(OBJ) -I$(OBJ) $(all_unittest_code) $(FFLAGS) $(LDFLAGS)

# search travis/tests/ for all subdirectories, which should reflect the full list of tests
TESTS := $(shell ls -d travis/tests/*/ | sed 's,travis/tests/,,g' | sed 's,/,,g')

# ================================================================== #
# Makefile rules

all: $(AOUT)

indenttest:
	@./travis/run_indent_test.sh

styletest:
	@./travis/run_style_test.sh

unittests: $(fruit_driver)
	@export DYLD_LIBRARY_PATH=$(FORT_LIB):$(CVODELIB):$(OPENLIBMDIR) ; $(fruit_driver)

tests:
	@echo "Make: Running the following tests:" $(TESTS)
	@./travis/run_tests.sh "$(TESTS)" "$(FORT_LIB):$(CVODELIB):$(OPENLIBMDIR)"

alltests: indenttest styletest unittests tests

sharedlib:
	$(FORT_COMP) -c $(SHAREDLIBDIR)/mechanism.f90 $(FSHAREDFLAGS) -o $(SHAREDLIBDIR)/mechanism.o -J$(OBJ)
	$(FORT_COMP) -shared -o $(SHAREDLIBDIR)/mechanism.so $(SHAREDLIBDIR)/mechanism.o

clean:
	rm -f *.o
	rm -f *.gcda *.gcno *.xml
	rm -f $(AOUT)
	rm -f $(OBJ)/*.mod
	rm -f travis/tests/*/*.out travis/tests/*/*.output travis/tests/*/reactionRates/*[0-9]
	rm -f $(UNITTESTDIR)/fruit_basket_gen.f90 $(UNITTESTDIR)/fruit_driver_gen.f90 $(fruit_driver)
	rm -f model/configuration/mechanism.{f90,o,prod,reac,ro2,so,species}

# dependencies:
atchem2.o : atchem2.f90 inputFunctions.o configFunctions.o dataStructures.o
argparse.o : argparse.f90 dataStructures.o
constraintFunctions.o : constraintFunctions.f90 dataStructures.o
atmosphereFunctions.o : atmosphereFunctions.f90
dataStructures.o : dataStructures.f90
inputFunctions.o : inputFunctions.f90 configFunctions.o dataStructures.o
interpolationFunctions.o : interpolationFunctions.f90 dataStructures.o
configFunctions.o : configFunctions.f90
outputFunctions.o : outputFunctions.f90 dataStructures.o
parameterModules.o : parameterModules.f90 dataStructures.o
solverFunctions.o : solverFunctions.f90 dataStructures.o
