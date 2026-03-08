function signal = high_pass(signal, fs, cutoff_freq)
  val = fft(signal);
  len = length(signal);
  ceva = (0:len-1)' * fs / len;
  masca = ceva > cutoff_freq;
  for i = 1:floor(len / 2)
    masca (len - i + 1) = masca(i);
  end
  val = val .* masca;
  semnal = ifft(val);
  signal = semnal / max(abs(semnal));
end
