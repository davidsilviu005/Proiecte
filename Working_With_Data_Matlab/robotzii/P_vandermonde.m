function y_interp = P_vandermonde (coef, x_interp)
	n = length(coef);
	y_interp = zeros(length(x_interp), 1);
	for i = 1:length(x_interp)
		xi = x_interp(i);
		for j = 1:n
			y_interp(i) += coef(j) * xi^(j - 1);
		end
	end
end
