
module regfile(
    input logic i_clk,
    input logic i_rst,
    input logic [4:0] rs1,
    input logic [4:0] rs2,
    input logic [4:0] rd,
    input logic rd_write_control,
    input logic [31:0] rd_write_val,
    output logic [31:0] rs1_val,
    output logic [31:0] rs2_val
);

logic [31:0] regs [0:31];

assign rs1_val= regs[rs1];
assign rs2_val=regs[rs2];
// Edit the code here begin ---------------------------------------------------
always@(posedge i_clk or negedge i_rst) begin
    // reset entire register bank
    if(~i_rst) begin
        for(int i=0;i<32;i++) begin
            regs[i]<=0;
        end
    end
    else begin
        //r0 can not be written to,since hardwired to 0
        if(rd_write_control && rd!=0)begin 
            regs[rd]<=rd_write_val;
        end
    end

end
// Edit the code here end -----------------------------------------------------


/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/regfile.vcd");
        $dumpvars(0, regfile);
    end
`endif

endmodule
