function x = oscillator(freq, fs, dur, A, D, S, R)
  t = (0:1/fs:dur - 1/fs)';
  total = length(t);
  x = sin(2 * pi * freq * t);
  a = floor(A * fs);
  d = floor(D * fs);
  r = floor(R * fs);
  s = total - a - d - r;
  if s < 0
    s = 0;
    r = t - a - d;
    r = max(r, 0);
  end
  attack = linspace(0, 1, a)';
  decay = linspace(1, S, d)';
  sustain = ones(s, 1) * S;
  release = linspace(S, 0, r)';
  env = [attack; decay; sustain; release];
  env_len = length(env);
  if env_len < total
    env = [env; zeros(total - env_len, 1)];
  elseif env_len > total
    env = env(1:total);
  end
  x = x .* env;
end
