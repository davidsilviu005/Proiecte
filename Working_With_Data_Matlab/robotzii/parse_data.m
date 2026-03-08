function [x, y] = parse_data(filename)
    file = fopen(filename, 'r');
    n = fscanf(file, '%d', 1);
    x = fscanf(file, '%f', n + 1);
    y = fscanf(file, '%f', n + 1);
    fclose(file);
end