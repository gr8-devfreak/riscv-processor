
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module decode_imm_inst(
    input logic [31:7] instruction_code,
    output logic [4:0] rs1,
    output logic [4:0] rd,
    output logic [11:0] imm,
    output logic [4:0] alu_control
);

// Edit the code here begin ---------------------------------------------------
    logic [2:0]funct3;
    logic [6:0]funct7;

    assign rs1 = instruction_code[19:15];
    assign rd = instruction_code[11:7];
    assign imm = instruction_code[31:20];
    assign funct3=instruction_code[14:12];
    assign funct7 = instruction_code[31:25];                          //imm[11:5]
    always_comb begin
        case(funct3) 
        3'h0:begin
            alu_control= `ADDI ;
        end
        3'h1:begin
            if(funct7==7'h00) alu_control= `SLLI ;
            else alu_control= `ALU_NOP ;
        end  
        3'h2:begin
            alu_control= `SLTI ;
        end  
        3'h3:begin
            alu_control= `SLTIU ;
        end 
        3'h4:begin
            alu_control= `XORI ;
        end  
        3'h5:begin
            if(funct7==7'h00) alu_control= `SRLI ;
            else if (funct7==7'h20) alu_control= `SRAI ;
            else alu_control= `ALU_NOP ;
        end 
        3'h6:begin
            alu_control= `ORI ;
        end  
        3'h7:begin
            alu_control= `ANDI ;
        end  
        endcase
    end
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/decode_imm_inst.vcd");
        $dumpvars(0, decode_imm_inst);
    end
`endif

endmodule
