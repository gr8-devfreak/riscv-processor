
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module store(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] rs1_val,
    input logic [31:0] rs2_val,
    input logic [31:0] imm,
    input logic [2:0] store_control,
    output logic stall_pc,
    output logic ignore_curr_inst,
    output logic mem_rw_mode,
    output logic [31:0] mem_addr,
    output logic [31:0] mem_write_data,
    output logic [3:0] mem_byte_en
);

// Edit the code here begin ---------------------------------------------------

    // assign stall_pc = 'b0;
    // assign ignore_curr_inst = 'b0;
    // assign mem_rw_mode = 'b0;
    // assign mem_addr = 'b0;
    // assign mem_write_data = 'b0;
    // assign mem_byte_en = 'b0;

    logic [1:0]addr_offset;

    typedef enum  {S1,S2} state;   
    state PS,NS;
    always@(*) begin           //Next state Decoder
           case(PS) 
           S1:begin
           if(store_control!=`STR_NOP) begin
            stall_pc=1;
            mem_rw_mode=0;
            mem_addr=rs1_val+imm;
            addr_offset=mem_addr;
            case(store_control) 
            `SB:begin
                mem_byte_en= 1<<addr_offset;
                case(addr_offset) 
                2'b00:mem_write_data=rs2_val[7:0];
                2'b01:mem_write_data={16'b0,rs2_val[7:0],8'b0};
                2'b10:mem_write_data={8'b0,rs2_val[7:0],16'b0};
                2'b11:mem_write_data={rs2_val[7:0],24'b0};
                endcase
            end
            `SH:begin
                mem_byte_en= (addr_offset[1]==1) ? 4'b1100 : 4'b0011 ;
                mem_write_data=(addr_offset[1]==1) ?{rs2_val[15:0],16'b0} :rs2_val[15:0];
            end
            `SW:begin
                mem_byte_en=4'b1111 ;
                mem_write_data=rs2_val;
            end
            endcase
            NS=S2;
           end
           else begin
            mem_rw_mode=1;
            stall_pc=0;
            mem_addr=0;
            addr_offset=mem_addr;
            mem_write_data=0;
            mem_byte_en=0;
           end
           end
           S2:begin
            mem_rw_mode=1;
            stall_pc=0;
            mem_addr=0;
            addr_offset=mem_addr;
            mem_write_data=0;
            mem_byte_en=0;
            NS=S1;
           end
           endcase       
    end

    always@(posedge i_clk or negedge i_rst) begin  //state register
        if(~i_rst) PS<=S1;
        else PS<=NS;
    end

    always@(posedge i_clk or negedge i_rst) begin  
        if(~i_rst)begin
            ignore_curr_inst<=0; 
        end
        else begin 
            ignore_curr_inst<=stall_pc;
        end
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/store.vcd");
        $dumpvars(0, store);
    end
`endif

endmodule
