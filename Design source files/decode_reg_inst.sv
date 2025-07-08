
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif
//purely combinational ,possible that instruction at input is not R-type
module decode_reg_inst(
    input logic [31:7] instruction_code,
    output logic [4:0] rs1,
    output logic [4:0] rs2,
    output logic [4:0] rd,
    output logic [4:0] alu_control
);

// Edit the code here begin ---------------------------------------------------
    logic [2:0]funct3;
    logic [6:0]funct7;

    assign rs1 = instruction_code[19:15];
    assign rs2 = instruction_code[24:20];
    assign rd = instruction_code[11:7];
    assign funct3=instruction_code[14:12];
    assign funct7=instruction_code[31:25];
 
    always_comb begin
        case(funct3) 
        3'h0:begin
            if(funct7==7'h00) alu_control= `ADD ;
            else if(funct7==7'h20)alu_control= `SUB ;
            else alu_control= `ALU_NOP ;
        end
        3'h1:begin
            if(funct7==7'h00) alu_control= `SLL ;
            else alu_control= `ALU_NOP ;
        end  
        3'h2:begin
            if(funct7==7'h00) alu_control= `SLT ;
            else alu_control= `ALU_NOP ;
        end  
        3'h3:begin
            if(funct7==7'h00) alu_control= `SLTU ;
            else alu_control= `ALU_NOP ;
        end 
        3'h4:begin
            if(funct7==7'h00) alu_control= `XOR;
            else alu_control= `ALU_NOP ;
        end  
        3'h5:begin
            if(funct7==7'h00) alu_control= `SRL ;
            else if(funct7==7'h20)alu_control= `SRA ;
            else alu_control= `ALU_NOP ;
        end 
        3'h6:begin
            if(funct7==7'h00) alu_control= `OR ;
            else alu_control= `ALU_NOP ;
        end  
        3'h7:begin
            if(funct7==7'h00) alu_control= `AND ;
            else alu_control= `ALU_NOP ;
        end  
        endcase
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/decode_reg_inst.vcd");
        $dumpvars(0, decode_reg_inst);
    end
`endif

endmodule
