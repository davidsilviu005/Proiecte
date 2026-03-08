function coef = vandermonde(x, y)
    n = length(x);
    V = zeros(n, n);
    for i = 1:n
        for j = 1:n
            V(i, j) = x(i)^(j - 1);
        end
    end
    coef = V \ y;
endfunction
