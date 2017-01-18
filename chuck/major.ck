0.2 => float factor;

SinOsc s0 => dac;
Std.mtof(60) => s0.freq;
0.72*factor => s0.gain;
//0.65*factor => s0.gain;

SinOsc s1 => dac;
Std.mtof(61) => s1.freq;
0 => s1.gain;
//0.07 *factor => s1.gain;

SinOsc s2 => dac;
Std.mtof(62) => s2.freq;
0.35 * factor => s2.gain;
//0.25 * factor => s2.gain;

SinOsc s3 => dac;
Std.mtof(63) => s3.freq;
0 * factor => s3.gain;
//0.65 *factor => s3.gain;

SinOsc s4 => dac;
Std.mtof(64) => s4.freq;
0.84 * factor => s4.gain;
//0.11 * factor => s4.gain;

SinOsc s5 => dac;
Std.mtof(65) => s5.freq;
0.08 * factor => s5.gain;
//0.07 * factor => s5.gain;


SinOsc s7 => dac;
Std.mtof(67) => s7.freq;
1 * factor => s7.gain;
//1 * factor => s7.gain;


SinOsc s8 => dac;
Std.mtof(68) => s8.freq;
0.12 *factor => s8.gain;
//0 => s8.gain;

SinOsc s10 => dac;
Std.mtof(70) => s10.freq;
0.08 * factor => s10.gain;
//0.32 * factor => s10.gain;

SinOsc s11 => dac;
Std.mtof(71) => s11.freq;
0.39 * factor => s11.gain;
//0.11 * factor => s11.gain;

4::second => now;