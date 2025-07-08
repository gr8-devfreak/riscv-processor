
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module decode_load_inst(
    input logic [31:7] instruction_code,
    output logic [4:0] rs1,
    output logic [4:0] rd,
    output logic [11:0] imm,
    output logic [2:0] load_control
);

// Edit the code here begin ---------------------------------------------------
    logic [2:0]funct3;
    
    assign rs1 =instruction_code[19:15];
    assign rd = instruction_code[11:7];
    assign imm = instruction_code[31:20];
    assign funct3= instruction_code[14:12];

    always_comb begin
        case(funct3) 
        3'h0:load_control=`LB;
        3'h1:load_control=`LH;
        3'h2:load_control=`LW;
        3'h4:load_control=`LBU;
        3'h5:load_control=`LHU ;
        default:load_control=`LD_NOP;
        endcase
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/decode_load_inst.vcd");
        $dumpvars(0, decode_load_inst);
    end
`endif

endmodule
