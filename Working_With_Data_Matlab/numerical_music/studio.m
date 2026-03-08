clear;

window_size = 512;
high_pass_cutoff = 1000; % Hz

[impulse_response _] = audioread("s1r1.wav");

[sig1, fs1] = audioread("loop.wav");
sig1 = stereo_to_mono(sig1);

[S f t] = spectrogram(sig1, fs1, window_size);
plot_spectrogram(S, f, t, "Plain Loop");

[sig2 fs2] = create_sound("music1.csv");
audiowrite("sig2.wav", sig2, fs2);

[S f t] = spectrogram(sig2, fs2, window_size);
plot_spectrogram(S, f, t, "Plain Sound");
% Comment on the difference between this spectrogram and the "Plain Loop" one.
% Why does it look like that?

sig2_highpass = high_pass(sig2, fs2, high_pass_cutoff);
audiowrite("sig2_highpass.wav", sig2_highpass, fs2);

[S f t] = spectrogram(sig2_highpass, fs2, window_size);
plot_spectrogram(S, f, t, "High Pass Sound");
% Comment on the difference between this spectrogram and "Plain Sound".

sig2_reverb = apply_reverb(sig2, impulse_response);
audiowrite("sig2_reverb.wav", sig2_reverb, fs2);

[S f t] = spectrogram(sig2_reverb, fs2, window_size);
plot_spectrogram(S, f, t, "Reverb Sound");
% Comment on the difference between this spectrogram and "Plain Sound".

[sig3 fs3] = audioread("tech.wav");
sig3 = stereo_to_mono(sig3);

% Let's only take the first 500k samples, about 10 sec.
sig3 = sig3(1:500000);

[S f t] = spectrogram(sig3, fs3, window_size);
plot_spectrogram(S, f, t, "Tech");

sig3_high = high_pass(sig3, fs3, high_pass_cutoff);
audiowrite("sig3_highpass_only.wav", sig3_high, fs3);

[S f t] = spectrogram(sig3_high, fs3, window_size);
plot_spectrogram(S, f, t, "High Pass Tech");

sig3_rev = apply_reverb(sig3, impulse_response);
audiowrite("sig3_reverb_only.wav", sig3_rev, fs3);

[S f t] = spectrogram(sig3_rev, fs3, window_size);
plot_spectrogram(S, f, t, "Reverb Tech");

sig3_high_rev = apply_reverb(sig3_high, impulse_response);
audiowrite("sig3_high_rev.wav", sig3_high_rev, fs3);

[S f t] = spectrogram(sig3_high_rev, fs3, window_size);
plot_spectrogram(S, f, t, "High Pass + Reverb Tech");
clear sig3_high_rev; % Free memory

sig3_rev_high = high_pass(sig3_rev, fs3, high_pass_cutoff);
audiowrite("sig3_rev_high.wav", sig3_rev_high, fs3);

[S f t] = spectrogram(sig3_rev_high, fs3, window_size);
plot_spectrogram(S, f, t, "Reverb + High Pass Tech");
