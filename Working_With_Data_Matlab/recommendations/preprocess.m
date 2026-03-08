function reduced_mat = preprocess(mat, min_reviews)
  cnt = sum(mat != 0, 2);
  reduced_mat = mat(cnt >= min_reviews, :);
end
