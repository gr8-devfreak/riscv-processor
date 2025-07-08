import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.coroutine
async def reset_dut(dut):
    """ Reset the DUT """
    dut.i_rst.value = 0
    for _ in range(2):
        await RisingEdge(dut.i_clk)
    dut.i_rst.value = 1
    await RisingEdge(dut.i_clk)

def load_hex(dut):
    hex_file_path = f"./firmware/build/firmware_wish_riscv_full.hex"
    with open(hex_file_path, 'r') as f:
        hex_file = f.read().splitlines()
    for ii in range(512):           # pram
        dut.inst_mem.memory_reg[ii].value = int(hex_file[ii], 16)
    for ii in range(512,1024):      # dram
        dut.inst_mem.memory_reg[ii].value = 0
    cocotb.log.info("loaded hexfile into Memory")
