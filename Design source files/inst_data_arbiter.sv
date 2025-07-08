
module inst_data_arbiter(
    input logic [31:0] inst_addr,
    input logic stall_pc,
    input logic [31:0] mem_addr,
    input logic mem_rw_mode,
    input logic [31:0] mem_write_data,
    input logic [3:0] mem_byte_en,
    input logic ignore_curr_inst,
    input logic [31:0] from_mem_data,
    output logic [31:0] instruction_code,
    output logic [31:0] mem_read_data,
    output logic [31:0] to_mem_addr,
    output logic to_mem_rw_mode,
    output logic [31:0] to_mem_write_data,
    output logic [3:0] to_mem_byte_en
);

// Edit the code here begin ---------------------------------------------------

    assign instruction_code = ignore_curr_inst?0:from_mem_data;
    assign mem_read_data=ignore_curr_inst?from_mem_data:0;
    assign to_mem_rw_mode=stall_pc? mem_rw_mode:1;
    assign to_mem_addr=stall_pc? mem_addr:inst_addr;
    assign to_mem_write_data=stall_pc? mem_write_data :0;
    assign to_mem_byte_en=stall_pc? mem_byte_en :0;

// Edit the code here end -----------------------------------------------------

endmodule
