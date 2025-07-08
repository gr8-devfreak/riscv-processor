
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module load(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] rs1_val,
    input logic [31:0] imm,
    input logic [31:0] mem_data,
    input logic [4:0] rd_in,
    input logic [2:0] load_control,
    output logic stall_pc,
    output logic ignore_curr_inst,
    output logic rd_write_control,
    output logic [4:0] rd_out,
    output logic [31:0] rd_write_val,
    output logic mem_rw_mode,
    output logic [31:0] mem_addr
);

// Edit the code here begin ---------------------------------------------------
    logic [1:0]addr_offset;
    logic[7:0] data_byte;
    logic[15:0] half_word;
    logic [2:0] load_control_prev;
//MEALY FSM
    typedef enum  {S1,S2} state;   // S1: MEM_ACCESS , S2: REG_UPDATE
    state PS,NS;
    always@(*) begin           //Next state Decoder
           mem_rw_mode=1; //only read
           case(PS) 
           S1:begin
            load_control_prev=load_control;
            rd_write_control=0;
            rd_write_val=0;
            if(load_control!=`LD_NOP) begin
                mem_addr=(rs1_val+imm);
                addr_offset=rs1_val+imm; //takes last 2 LSB i.e. remainder
                stall_pc=1;
                NS=S2;
            end
            else begin
                mem_addr=0;
                stall_pc=0;
                NS=S1;
            end
           end
           S2:begin
            stall_pc=0;
            mem_addr=0;
            rd_write_control=1;
            case(addr_offset)
            2'b00:begin
                data_byte=mem_data[7:0];
                half_word=mem_data[15:0];
            end
            2'b01: begin
                data_byte=mem_data[15:8];
                half_word=mem_data[15:0];
           end
            2'b10:begin
                data_byte=mem_data[23:16];
                half_word=mem_data[31:16];
            end
            2'b11:begin
                data_byte=mem_data[31:24];
                half_word=mem_data[31:16];
            end
            endcase

            //load control changes on next clock cycle,so use load_control_prev
              case(load_control_prev)
              `LB:begin
                rd_write_val={ {24{data_byte[7]}} , data_byte };
              end
              `LH:begin
                rd_write_val={ {16{half_word[15]}} , half_word };
               end 
              `LW:begin
                rd_write_val=mem_data;
              end
              `LBU:begin
                rd_write_val={ 24'b0 , data_byte };
              end
              `LHU:begin
                rd_write_val={ 16'b0 , half_word };
              end
              endcase

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
            rd_out<=(load_control==`LD_NOP)? 0:rd_in ;
        end
    end

// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/load.vcd");
        $dumpvars(0, load);
    end
`endif

endmodule
