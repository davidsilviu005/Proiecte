function mono = stereo_to_mono(stereo)
  mono = mean(stereo, 2);
  max_val = max(abs(mono));
  if max_val != 0
    mono = mono / max_val;
  end
end
