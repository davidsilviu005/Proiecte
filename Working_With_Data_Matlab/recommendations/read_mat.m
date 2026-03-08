function mat = read_mat(path)
  citire = csvread(path, 1, 1);
  mat = citire;
end
