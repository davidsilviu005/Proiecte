function [S f t] = spectrogram(signal, fs, window_size)
	signal = signal(:);
  N = length(signal);
  num_windows = floor(N / window_size);
  n = (0:window_size - 1)';
  val = 0.5 - 0.5 * cos(2 * pi * n / (window_size - 1));
  S = zeros(window_size, num_windows);
  for i = 1:num_windows
    poz_start = (i - 1) * window_size + 1;
    segment = signal(poz_start : poz_start + window_size - 1);
    val1 = segment .* val;
    dim1 = [val1; zeros(window_size, 1)];
    spectrum = abs(fft(dim1));
    S(:, i) = spectrum(1:window_size);
  end
  f = (0:window_size - 1)' * (fs / (2 * window_size));
  t = (0:num_windows - 1)' * (window_size / fs);
end
