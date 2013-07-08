`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    21:31:13 06/18/2013 
// Design Name: 
// Module Name:    foo 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////

module dacwriter(
	clk,
	dac_data,
	ship,
	dacbit,
	cs_active
);

input clk;
input dac_data;
input ship;
wire clk;
wire [13:0] dac_data;
wire ship;

reg [4:0] dac_counter;
reg [13:0] dac_data_latched;
reg cs_active;

// dacbit goes to out_b
// !clk goes to out_c
// !cs_active goes to out_d
// assign out_a = 0
assign dacbit = ((dac_data_latched >> (13 - dac_counter)) & 1) && (dac_counter < 14);

always @(posedge clk) begin
	fast_counter <= fast_counter + 1;
	if (ship) begin
		dac_counter <= 0;
		cs_active <= 1;
		dac_data_latched <= dac_data;
	end else if (dac_counter < 16) begin
		if (dac_counter == 15) begin
			cs_active <= 0;
		end
		dac_counter <= dac_counter + 1;
	end
end

endmodule;




module foo(
	 clk,
    out_a,
    out_b,
    out_c,
    out_d
    );

input clk;
output out_a;  // A0
output out_b;  // A1
output out_c;  // A2
output out_d;  // A3
wire out_a;
wire out_b;
wire out_c;
wire out_d;

reg [9:0] fast_counter;
reg [6:0] ramp_counter;
reg [4:0] dac_counter;
reg [14:0] dac_data;
reg cs_active;
wire clk40;
assign clk40 = fast_counter == 0;
assign out_c = !clk;
assign out_b = ((dac_data >> (13 - dac_counter)) & 1) && (dac_counter < 14);
assign out_d = !cs_active;
assign out_a = 0;

always @(posedge clk) begin
	if (clk40) begin
		ramp_counter <= ramp_counter + 1;
	end
	fast_counter <= fast_counter + 1;
	if (clk40) begin
		dac_counter <= 0;
		cs_active <= 1;
	end else if (dac_counter < 16) begin
		if (dac_counter == 15) begin
			dac_data <= (ramp_counter << 6) + (1 << 12);
			cs_active <= 0;
		end
		dac_counter <= dac_counter + 1;
	end
end

endmodule
