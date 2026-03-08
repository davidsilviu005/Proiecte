function recoms = recommendations(path, liked_theme, num_recoms, min_reviews, num_features)
  mat = read_mat(path);
  mat = preprocess(mat, min_reviews);
  [m, n] = size(mat);
  cnt = min([num_features, m, n]);
  [~, ~, V] = svds(mat, cnt);
  ceva = size(V, 1);
  ceva1 = V(liked_theme, :)';
  similaritati = zeros(cnt, 1);
  for i = 1:ceva
    similaritati(i) = cosine_similarity(V(i, :)', ceva1);
  end
  similaritati(liked_theme) = -Inf;
  [~, indici_sortati] = sort(similaritati, 'descend');
  varf_k = min(num_recoms, ceva - 1);
  recoms = indici_sortati(1:varf_k)';
end
