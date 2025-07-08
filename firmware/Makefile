#Makefile
SIM = icarus
TOPLEVEL_LANG = verilog

VER_DIR = ../ver

ifeq ($(MAKECMDGOALS), )
ifndef tname
$(error $$tname must be defined. Use `make tname=<testcase_name>`)
endif
endif

ifeq ($(tname),instr)
	MODULE = test_instr
else
	MODULE = test_$(tname)
endif

VERILOG_SOURCES = $(VER_DIR)/processor.sv
COMPILE_ARGS += -I $(VER_DIR)
TOPLEVEL = processor

all: clean

include $(shell cocotb-config --makefiles)/Makefile.sim


