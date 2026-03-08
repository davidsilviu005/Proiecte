function signal = apply_reverb(signal, impulse_response)
  impulse_response = stereo_to_mono(impulse_response);
  signal = fftconv(signal, impulse_response);
  max_val = max(abs(signal));
  if max_val > 0
    signal = signal / max_val;
  end
end
