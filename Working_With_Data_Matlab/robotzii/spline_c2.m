function coef = spline_c2 (x, y)
	n = length(x) - 1;
	A = zeros(4 * n, 4 * n);
	b = zeros(4 * n, 1);
	row = 1;
	for i = 1:n
		A(row, (i - 1) * 4 + 1) = 1;
		b(row) = y(i);
		row += 1;
	end
	dx = x(n+1) - x(n);
	A(row, end - 3) = 1;
	A(row, end - 2) =  dx;
	A(row, end - 1) = dx^2;
	A(row, end) = dx^3;
	b(row) = y(n + 1);
	row += 1;
	for i = 1:n-1
		dx = x(i+1) - x(i);
		A(row, (i-1)*4 + 1 : (i-1)*4 + 4) = [1 dx dx^2 dx^3];
		A(row, i*4 + 1) = -1;
		b(row) = 0;
		row += 1;
	end
	for i = 1:n-1
		dx = x(i+1) - x(i);
		A(row, (i-1)*4 + 2 : (i-1)*4 + 4) = [1 2*dx 3*dx^2];
		A(row, i*4 + 2) = -1;
		b(row) = 0;
		row += 1;
	end
	for i = 1:n-1
		dx = x(i+1) - x(i);
		A(row, (i-1)*4 + 3 : (i-1)*4 + 4) = [2 6*dx];
		A(row, i*4 + 3) = -2;
		b(row) = 0;
		row += 1;
	end
	A(row, 3) = 2;
	b(row) = 0;
	row += 1;
	dx = x(n+1) - x(n);
	A(row, end - 1) = 2;
	A(row, end) = 6 * dx;
	b(row) = 0;
	coef = A \ b;
end

