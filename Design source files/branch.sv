
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module branch(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] pc,
    input logic [31:0] imm,
    input logic [31:0] rs1_val,
    input logic [31:0] rs2_val,
    input logic [2:0] branch_control,
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
        case(branch_control)
            `BEQ:begin
                if(rs1_val==rs2_val) begin
                    pc_update_control=1;
                    pc_update_val=pc+imm;
                end
                else begin
                    pc_update_control=0;
                    pc_update_val=0;  
                end
            end 
            `BNE:begin
                if(rs1_val!=rs2_val) begin
                    pc_update_control=1;
                    pc_update_val=pc+imm;
                end
                else begin
                    pc_update_control=0;
                    pc_update_val=0;  
                end
            end
            `BLT:begin                     //use $signed()
                if($signed(rs1_val)<$signed(rs2_val)) begin
                    pc_update_control=1;
                    pc_update_val=pc+imm;
                end
                else begin
                    pc_update_control=0;
                    pc_update_val=0;  
                end
            end
            `BGE:begin                     //use $signed()
                if($signed(rs1_val) >= $signed(rs2_val)) begin
                    pc_update_control=1;
                    pc_update_val=pc+imm;
                end
                else begin
                    pc_update_control=0;
                    pc_update_val=0;  
                end

            end
            `BLTU:begin
                if(rs1_val<rs2_val) begin
                    pc_update_control=1;
                    pc_update_val=pc+imm;
                end
                else begin
                    pc_update_control=0;
                    pc_update_val=0;  
                end

            end
            `BGEU:begin
                if(rs1_val>=rs2_val) begin
                    pc_update_control=1;
                    pc_update_val=pc+imm;
                end
                else begin
                    pc_update_control=0;
                    pc_update_val=0;  
                end

            end
            `BR_NOP: begin
                pc_update_control=0;
                pc_update_val=0; 
            end
            endcase
    end
    
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/branch.vcd");
        $dumpvars(0, branch);
    end
`endif

endmodule
