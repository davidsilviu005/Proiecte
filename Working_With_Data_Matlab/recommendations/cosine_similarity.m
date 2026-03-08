function similarity = cosine_similarity(A, B)
  A = A(:);
  B = B(:);
  norma_A = norm(A);
  norma_B = norm(B);
  if norma_A == 0 || norma_B == 0
    similarity = 0;
  else
    similarity = dot(A, B)/ (norma_A * norma_B);
  end
end
