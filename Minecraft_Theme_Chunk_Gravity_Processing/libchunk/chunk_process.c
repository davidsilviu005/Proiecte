#include "chunk.h"
#include <stdlib.h>
#define NUM_DIRECTIONS 18
char*** chunk_shell(
    char*** chunk, int width, int height, int depth,
    char target_block, char shell_block) {
    char*** new_chunk = (char***)malloc(width * sizeof(char**));
    for (int x = 0; x < width; x++) {
        new_chunk[x] = (char**)malloc(height * sizeof(char*));
        for (int y = 0; y < height; y++) {
            new_chunk[x][y] = (char*)malloc(depth * sizeof(char));
            for (int z = 0; z < depth; z++) {
                new_chunk[x][y][z] = chunk[x][y][z];
            }
        }
    }
    int directions[NUM_DIRECTIONS][3] = {
        { 1,  0,  0}, {-1,  0,  0}, { 0,  1,  0},
        { 0, -1,  0}, { 0,  0,  1}, { 0,  0, -1},
        { 1,  1,  0}, { 1, -1,  0}, {-1,  1,  0}, {-1, -1,  0},
        { 1,  0,  1}, { 1,  0, -1}, {-1,  0,  1}, {-1,  0, -1},
        { 0,  1,  1}, { 0,  1, -1}, { 0, -1,  1}, { 0, -1, -1}
    };
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            for (int z = 0; z < depth; z++) {
                if (chunk[x][y][z] == target_block) {
                    for (int d = 0; d < NUM_DIRECTIONS; d++) {
                        int nx = x + directions[d][0];
                        int ny = y + directions[d][1];
                        int nz = z + directions[d][2];
                        if (nx >= 0 && nx < width &&
                            ny >= 0 && ny < height &&
                            nz >= 0 && nz < depth) {
                            if (new_chunk[nx][ny][nz] != target_block) {
                                new_chunk[nx][ny][nz] = shell_block;
                            }
                        }
                    }
                }
            }
        }
    }
    return new_chunk;
}

char*** chunk_fill_xz(
    char*** chunk, int width, int height, int depth,
    int x, int y, int z, char block) {
    char target_block = chunk[x][y][z];
    if (target_block == block) {
        return chunk;
    }
    int** visited = (int**)malloc(width * sizeof(int*));
    for (int i = 0; i < width; i++) {
        visited[i] = (int*)calloc(depth, sizeof(int));
    }
    int stack_size = width * depth;
    int stack_index = 0;
    int* stack_x = (int*)malloc(stack_size * sizeof(int));
    int* stack_z = (int*)malloc(stack_size * sizeof(int));
    stack_x[stack_index] = x;
    stack_z[stack_index] = z;
    stack_index++;
    while (stack_index > 0) {
        stack_index--;
        int cx = stack_x[stack_index];
        int cz = stack_z[stack_index];
        if (cx < 0 || cx >= width || cz < 0 || cz >= depth || visited[cx][cz] || chunk[cx][y][cz] != target_block) {
            continue;
        }
        visited[cx][cz] = 1;
        chunk[cx][y][cz] = block;
        if (cx + 1 < width) {
            stack_x[stack_index] = cx + 1;
            stack_z[stack_index] = cz;
            stack_index++;
        }
        if (cx - 1 >= 0) {
            stack_x[stack_index] = cx - 1;
            stack_z[stack_index] = cz;
            stack_index++;
        }
        if (cz + 1 < depth) {
            stack_x[stack_index] = cx;
            stack_z[stack_index] = cz + 1;
            stack_index++; }
        if (cz - 1 >= 0) {
            stack_x[stack_index] = cx;
            stack_z[stack_index] = cz - 1;
            stack_index++; }
    }
    for (int i = 0; i < width; i++) {
        free(visited[i]);
    }
    free(visited);
    free(stack_x);
    free(stack_z);
    height = height + 1;
    return chunk;
}

void fill(char*** chunk, int width, int height, int depth,
          int x, int y, int z, char target_block, char block) {
    if (x < 0 || x >= width || y < 0 || y >= height || z < 0 || z >= depth) {
        return;
    }
    if (chunk[x][y][z] != target_block) {
        return;
    }
    chunk[x][y][z] = block;
    fill(chunk, width, height, depth, x + 1, y, z, target_block, block);
    fill(chunk, width, height, depth, x - 1, y, z, target_block, block);
    fill(chunk, width, height, depth, x, y + 1, z, target_block, block);
    fill(chunk, width, height, depth, x, y - 1, z, target_block, block);
    fill(chunk, width, height, depth, x, y, z + 1, target_block, block);
    fill(chunk, width, height, depth, x, y, z - 1, target_block, block);
}

char*** chunk_fill(
    char*** chunk, int width, int height, int depth,
    int x, int y, int z, char block) {
    char target_block = chunk[x][y][z];
    if (target_block == block) {
        return chunk;
    }
    fill(chunk, width, height, depth, x, y, z, target_block, block);
    return chunk;
}
