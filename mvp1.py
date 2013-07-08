# Level 1 mvp prototype

import sys
from myhdl import *


def genclocks(clk, clk40, clk2):
    counter1 = Signal(intbv(0)[9:])
    counter2 = Signal(intbv(0)[15])

    @always(clk.posedge)
    def foo():
        if counter1 >= 799:
            clk40.next = 1
            counter1.next = 0
            if counter2 >= 19999:
                counter2.next = 0
                clk2.next = 1
            else:
                counter2.next = counter2 + 1
                clk2.next = 0
        else:
            counter1.next = counter1 + 1
            clk40.next = 0
            clk2.next = 0

    return foo


def gen2(clk, clk40, clk2):
    counter = Signal(False)[15:]

    @always(clk.posedge)
    def foo():
        if clk40:
            if counter <= 0:
                counter.next = 20000
            else:
                counter.next = counter - 1
            clk2.next = 1
            clk2.next = 0

    return foo


def get_freq(pitch, freq):
    @always_comb
    def foo():
        if pitch == 0:
            freq.next = 139479
        if pitch == 1:
            freq.next = 124261
        if pitch == 2:
            freq.next = 110704
        if pitch == 3:
            freq.next = 104491
        if pitch == 4:
            freq.next = 93091
        if pitch == 5:
            freq.next = 82935
        if pitch == 6:
            freq.next = 73886
        if pitch == 7:
            freq.next = 69739
        if pitch == 8:
            freq.next = 62131
        if pitch == 9:
            freq.next = 55352
        if pitch == 10:
            freq.next = 52246
        if pitch == 11:
            freq.next = 46545
        if pitch == 12:
            freq.next = 41467
        if pitch == 13:
            freq.next = 36943
        else:
            freq.next = 34869
    return foo


def voice(clk, clk40, keydn, dphase, _out):

    ampl = Signal(intnv(0))[13:]
    phase = Signal(intnv(0))[23:]
    twave = Signal(intnv(0))[22:]
    _out = Signal(intnv(0))[13:]
    keydn_delay = Signal(False)

    @always(clk.posedge)
    def piece1():
        if not clk40:
            pass
        keydn_delay.next = keydn
        if keydn and not keydn_delay:
            ampl,next = 16383
        elif ampl > 0:
            ampl.next = ampl - 1
        phase.next = phase + dphase
        if phase >= (1 << 23):
            twave.next = (1 << 23) - (phase + 1)
        else:
            twave.next = phase
        _out = (ampl * (twave >> 9)) - (ampl << 13)

    return piece1


def dacwriter(clk, clk40, dac_data, dacbit, cs_active):
    dac_counter = Signal(intbv(0)[4:])
    dac_data_latched = Signal(intbv(0)[13:])
    cs_active = Signal(False)
    dacbit = Signal(False)

    @always(clk.posedge)
    def foo():
        if clk40:
            dac_counter.next = 0
            cs_active.next = 1
            dac_data_latched.next = dac_data;
        elif dac_counter < 16:
            if dac_counter == 15:
                cs_active.next = 0
            dac_counter.next = dac_counter + 1

    return foo


def fpga():
    out_a, out_b, out_c, out_d = [Signal(False) for i in range(4)]
    clk = Signal(False)
    clk40 = Signal(False)
    clk2 = Signal(False)
    cs_active = Signal(False)
    _out = Signal(intbv(0)[13:])

    g = genclocks(clk, clk40, clk2)
    dw = dacwriter(clk, clk40, _out, out_b, cs_active)

    @always_comb
    def out_acd():
        out_a.next = 0
        out_c.next = not clk
        out_d.next = not cs_active

    return (g, dw, out_acd)


if sys.argv[1:2] == ['calculate']:
    for i in (0, 2, 4, 5, 7, 9, 11):
        a = 440.0
        acount = 40000.0 / a
	count = (2.0 ** ((7.0 - i) / 12)) * acount
        print int(512 * count + 0.5)
    sys.exit(0)

toVerilog(fpga)
