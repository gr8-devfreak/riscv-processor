
module mem(
    input logic i_clk,
    input logic i_rst,
    input logic [9:0] in_mem_addr,
    input logic in_mem_re_web,
    input logic [31:0] in_mem_write_data,
    input logic [3:0] in_mem_byte_en,
    output logic [31:0] out_mem_data
);

logic [31:0] memory_reg [0:1023];
logic [31:0] write_data_muxed;

// Edit the code here begin ---------------------------------------------------

    assign out_mem_data = write_data_muxed ;
    //use no-blocking for sequential logic
    always@(posedge i_clk or negedge i_rst ) begin
        if(in_mem_re_web) begin
            write_data_muxed <=i_rst? memory_reg[in_mem_addr]:0;
        end
        else begin
            if(in_mem_byte_en[0]==1'b1) begin
                memory_reg[in_mem_addr][7:0]<= in_mem_write_data[7:0];
            end 
            if(in_mem_byte_en[1]==1'b1) begin
                memory_reg[in_mem_addr][15:8]<= in_mem_write_data[15:8];
            end
            if(in_mem_byte_en[2]==1'b1) begin
                memory_reg[in_mem_addr][23:16]<= in_mem_write_data[23:16];
            end
            if(in_mem_byte_en[3]==1'b1) begin
                memory_reg[in_mem_addr][31:24]<= in_mem_write_data[31:24];
            end  
        end
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/
// string filename;
`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        // filename = $sformatf("./sim_build/mem_%d.vcd", `TESTCASE);
        // $dumpfile(filename);
        $dumpfile("./sim_build/mem.vcd");
        $dumpvars(0, mem);
    end
`endif

endmodule
