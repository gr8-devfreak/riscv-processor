
module ifu(
    input logic i_clk,
    input logic i_rst,
    input logic stall_pc,
    input logic pc_update_control,
    input logic [31:0] pc_update_val,
    output logic [31:0] pc,
    output logic [31:0] prev_pc
);

// Edit the code here begin ---------------------------------------------------

    always @(posedge i_clk or negedge i_rst) begin
        if(~i_rst) begin
            pc<=0;
            prev_pc<=0;
        end
        else begin
            prev_pc<=pc; //corrected
            if(stall_pc==0 && pc_update_control==0 ) begin
                pc<=pc+4;
            end
            if(stall_pc==0 && pc_update_control==1 ) begin
               pc<=pc_update_val;
            end
        end
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/ifu.vcd");
        $dumpvars(0, ifu);
    end
`endif

endmodule
