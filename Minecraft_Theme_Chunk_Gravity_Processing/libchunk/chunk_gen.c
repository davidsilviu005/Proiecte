#include "chunk.h"
#include <math.h>

char*** chunk_place_block(
    char*** chunk, int width, int height, int depth,
    int x, int y, int z, char block) {
    if (x >= 0 && x < width && y >= 0 && y < height && z >= 0 && z < depth) {
        chunk[x][y][z] = block;
    }
    return chunk;
}
char*** chunk_fill_cuboid(
    char*** chunk, int width, int height, int depth,
    int x0, int y0, int z0, int x1, int y1, int z1, char block) {
    int xmin = (x0 < x1) ? x0 : x1;
    int ymin = (y0 < y1) ? y0 : y1;
    int zmin = (z0 < z1) ? z0 : z1;
    int xmax = (x0 > x1) ? x0 : x1;
    int ymax = (y0 > y1) ? y0 : y1;
    int zmax = (z0 > z1) ? z0 : z1;
    for (int x = xmin; x <= xmax; ++x) {
        for (int y = ymin; y <= ymax; ++y) {
            for (int z = zmin; z <= zmax; ++z) {
                chunk = chunk_place_block(chunk, width, height, depth, x, y, z, block);
            }
        }
    }
    return chunk;
}
char*** chunk_fill_sphere(
    char*** chunk, int width, int height, int depth,
    int x, int y, int z, double radius, char block) {
    int xmin = (int)(x - radius);
    int xmax = (int)(x + radius);
    int ymin = (int)(y - radius);
    int ymax = (int)(y + radius);
    int zmin = (int)(z - radius);
    int zmax = (int)(z + radius);
    for (int i = xmin; i <= xmax; ++i) {
        for (int j = ymin; j <= ymax; ++j) {
            for (int k = zmin; k <= zmax; ++k) {
                if ((i - x) * (i - x) + (j - y) * (j - y) + (k - z) * (k - z) <= radius * radius) {
                    chunk = chunk_place_block(chunk, width, height, depth, i, j, k, block);
                }
            }
        }
    }
    return chunk;
}
