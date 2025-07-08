
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module jump(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] pc,  //fed prev_pc by ifu(from top-level module)
    input logic [31:0] imm,
    input logic [31:0] rs1_val,
    input logic [1:0] jump_control,
    output logic rd_write_control,
    output logic [31:0] rd_write_val,
    output logic pc_update_control,
    output logic [31:0] pc_update_val,
    output logic ignore_curr_inst
);

// Edit the code here begin ---------------------------------------------------

    always @(posedge i_clk or negedge i_rst) begin
        if(~i_rst) ignore_curr_inst<=0;
        else ignore_curr_inst<=pc_update_control;
    end

    always_comb begin
        case(jump_control)
            `JAL:begin
                pc_update_control=1;
                pc_update_val=pc+imm;
                rd_write_control=1;
                rd_write_val=pc+4;
            end 
            `JALR:begin
                pc_update_control=1;
                pc_update_val=rs1_val+imm;
                rd_write_control=1;
                rd_write_val=pc+4;
            end
            `JMP_NOP:begin 
                pc_update_control=0;
                pc_update_val=0;
                rd_write_control=0;
                rd_write_val=0;
            end
            endcase
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/jump.vcd");
        $dumpvars(0, jump);
    end
`endif

endmodule
