function y_interp = P_spline (coef, x, x_interp)
	n = length(x) - 1;
	y_interp = zeros(length(x_interp), 1);
	for j = 1:length(x_interp)
		xi = x_interp(j);
		for i = 1:n
			if xi >= x(i) && xi <= x(i+1)
				a = coef((i-1)*4 +1);
				b = coef((i-1)*4 +2);
				c = coef((i-1)*4 +3);
				d = coef((i-1)*4 +4);
				dx = xi - x(i);
				y_interp(j) = a + b*dx + c*dx^2 + d*dx^3;
				break;
			endif
		end
	end
end
