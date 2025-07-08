#Makefile
USER_DIR := /home/wishuser/wish25-course/3_riscv/sim/firmware
TEST_DIR = $(USER_DIR)/examples
BUILD_DIR = $(USER_DIR)/build
core = wish_riscv
SECTIONS := $(USER_DIR)/linker/sections.lds

INC_COMMON := ""

ifeq ($(MAKECMDGOALS), )
ifndef tname
$(error $$tname must be defined. Use `make tname=<testcase_name>`)
endif
endif

C_TEST		:= $(tname)
C_CORE		:= $(core)

DIR_USER	:= $(addsuffix /c_src, $(USER_DIR))
INC_USER	+= $(USER_DIR)/include

CFLAGS		:= \
		-march=rv32im_zicsr \
		-mabi=ilp32 \
		-Os \
		-ffunction-sections \
		-fdata-sections \
		$(addprefix -I, $(INC_USER))

LFLAGS		:= \
		-nostdlib \
		-lgcc \
		-Wl,-Bstatic,--gc-sections,-T,$(SECTIONS),-Map,$(BUILD_DIR)/firmware_$(C_CORE).map,--strip-debug

# TODO: Check on ubuntu machine
OS_VER := $(shell grep "^ID=" /etc/os-release | awk -F'["=]' '{print $$3}')

ifeq ($(OS_VER), rhel)
	RV_PREFIX	?= /data/CATALOG_DIG_PG1_OA_DS/sync/python_env/hscpy/extra/riscv/bin/riscv64-unknown-elf-
else
	RV_PREFIX	?= riscv32-unknown-elf-
endif

CC			:= $(RV_PREFIX)gcc
OBJDUMP		:= $(RV_PREFIX)objdump
OBJCOPY		:= $(RV_PREFIX)objcopy
SIZE		:= $(RV_PREFIX)size

SRC_USER	= $(wildcard $(addsuffix /*.c, $(DIR_USER)))
ASM_USER	= $(wildcard $(addsuffix /*.S, $(DIR_USER)))
OBJ_USER_C = $(addprefix $(BUILD_DIR)/, $(addsuffix .o, $(basename $(notdir $(SRC_USER))))) 
OBJ_USER_S = $(addprefix $(BUILD_DIR)/, $(addsuffix .o, $(basename $(notdir $(ASM_USER))))) 


ALL_OBJ = \
		$(OBJ_USER_C) \
		$(OBJ_USER_S) \
		$(addprefix $(BUILD_DIR)/, $(C_TEST).o)

.PRECIOUS: $(BUILD_DIR)/firmware_$(C_CORE).elf $(BUILD_DIR)/firmware_$(C_CORE).bin $(ALL_OBJ)

all: clean $(BUILD_DIR) $(addprefix $(BUILD_DIR)/, firmware_$(C_CORE).hex firmware_$(C_CORE).asm)

.PHONY: all $(C_TEST).o

$(BUILD_DIR)/%.asm: $(BUILD_DIR)/%.elf
	@echo " -- Dumping $*.elf to $*.asm"
	@$(OBJDUMP) -D $< > $@

$(BUILD_DIR)/%.hex: $(BUILD_DIR)/%.bin
	@echo " -- Converting $*.bin to $*.hex"
	@python $(USER_DIR)/scripts/makehex.py $< 1 2048 full

$(BUILD_DIR)/%.bin: $(BUILD_DIR)/%.elf
	@echo " -- Converting $*.elf to $*.bin"
	@$(OBJCOPY) -O binary $< $@

$(BUILD_DIR)/%.elf: $(ALL_OBJ) $(SECTIONS)
	@echo " -- Generating $*.elf and firmware_$(C_CORE).map"
	@$(CC) $(CFLAGS) $(LFLAGS) -o $@ $(ALL_OBJ)
	@$(SIZE) $@

$(BUILD_DIR)/%.o: $(DIR_USER)/%.S
	@echo " -- Compiling $*.S to $*.o"
	@$(CC) -c $(CFLAGS) -o $@ $<

$(BUILD_DIR)/%.o: $(TEST_DIR)/%.c
	@echo " -- Compiling $*.c to $*.o"
	@$(CC) -c $(CFLAGS) -o $@ $<


$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

clean:
	@rm -rf $(BUILD_DIR)
