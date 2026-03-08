#include "chunk.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#define AIR 0
#define BLOCK_GRASS 1
#define BLOCK_WOOD 2
#define BLOCK_STONE 3
void free_chunk(char*** v, int width, int height) {
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            free(v[i][j]);
        }
        free(v[i]);
    }
    free(v);
}
char*** chunk_rotate_y(
    char*** chunk, int width, int height, int depth) {
    int new_width = depth;
    int new_height = height;
    int new_depth = width;
    char*** rotated_chunk = (char***)malloc(new_width * sizeof(char**));
    for (int x = 0; x < new_width; x++) {
        rotated_chunk[x] = (char**)malloc(new_height * sizeof(char*));
        for (int y = 0; y < new_height; y++) {
            rotated_chunk[x][y] = (char*)malloc(new_depth * sizeof(char));
        }
    }
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            for (int z = 0; z < depth; z++) {
                int new_x = depth - z - 1;
                int new_y = y;
                int new_z = x;
                rotated_chunk[new_x][new_y][new_z] = chunk[x][y][z];
            }
        }
    }
    free_chunk(chunk, width, height);
    return rotated_chunk;
}

void flood_fill(char ***chunk, int x, int y, int z, int width, int height, int depth, char block_type, int ***visited) {
    if (x < 0 || x >= width || y < 0 || y >= height || z < 0 || z >= depth) return;
    if (chunk[x][y][z] != block_type || visited[x][y][z]) return;
    visited[x][y][z] = 1;
    flood_fill(chunk, x + 1, y, z, width, height, depth, block_type, visited);
    flood_fill(chunk, x - 1, y, z, width, height, depth, block_type, visited);
    flood_fill(chunk, x, y + 1, z, width, height, depth, block_type, visited);
    flood_fill(chunk, x, y - 1, z, width, height, depth, block_type, visited);
    flood_fill(chunk, x, y, z + 1, width, height, depth, block_type, visited);
    flood_fill(chunk, x, y, z - 1, width, height, depth, block_type, visited);
}
int find_lowest_position(char ***chunk, int ***visited, int width, int height, int depth) {
    int min_fall = height;
    for (int x = 0; x < width; x++) {
        for (int z = 0; z < depth; z++) {
            for (int y = 0; y < height; y++) {
                if (visited[x][y][z]) {
                    int fall = 0;
                    if (y-1 >= 0 && chunk[x][y-1][z] == chunk[x][y][z]) {
                        continue;
                    } else {
                        while (y - fall - 1 >= 0 && chunk[x][y - fall - 1][z] == AIR) {
                            fall++;
                        }
                        if (fall < min_fall) {
                            min_fall = fall;
                        }
                    }
                }
            }
        }
    }
    return min_fall;
}
void apply_gravity_to_body(char ***chunk, int ***visited, int width, int height, int depth, int fall_offset) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            for (int z = 0; z < depth; z++) {
                if (visited[x][y][z]) {
                    chunk[x][y - fall_offset][z] = chunk[x][y][z];
                    chunk[x][y][z] = AIR;
                }
            }
        }
    }
}
void reset_visited(int ***visited, int width, int height, int depth) {
    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            for (int z = 0; z < depth; z++)
                visited[x][y][z] = 0;
}
void free_char_triple_pointer(char ***array, int width, int height) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            free(array[x][y]);
        }
        free(array[x]);
    }
    free(array);
}
void free_int_triple_pointer(int ***array, int width, int height) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            free(array[x][y]);
        }
        free(array[x]);
    }
    free(array);
}
char*** chunk_apply_gravity(char ***chunk, int width, int height, int depth, int *new_height) {
    int ***visited = (int ***)malloc(width * sizeof(int **));
    for (int x = 0; x < width; x++) {
        visited[x] = (int **)malloc(height * sizeof(int *));
        for (int y = 0; y < height; y++) {
            visited[x][y] = (int *)calloc(depth, sizeof(int));
        }
    }
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            for (int z = 0; z < depth; z++) {
                if (!visited[x][y][z] && chunk[x][y][z] != AIR) {
                    flood_fill(chunk, x, y, z, width, height, depth, chunk[x][y][z], visited);
                    int fall_offset = find_lowest_position(chunk, visited, width, height, depth);
                    if (fall_offset > 0) {
                        apply_gravity_to_body(chunk, visited, width, height, depth, fall_offset);
                    }
                    reset_visited(visited, width, height, depth);
                }
            }
        }
    }
    char ***copie = malloc(width * sizeof(char**));
    for (int x = 0; x < width; x++) {
        copie[x] = malloc(height * sizeof(char*));
        for (int y = 0; y < height; y++) {
            copie[x][y] = malloc(depth * sizeof(char));
            for (int z = 0; z < depth; z++) {
                if (chunk[x][y][z] != AIR)
                    copie[x][y][z] = BLOCK_STONE;
                else
                    copie[x][y][z] = AIR;
            }
        }
    }
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            for (int z = 0; z < depth; z++) {
                if (!visited[x][y][z] && copie[x][y][z] != AIR) {
                    flood_fill(copie, x, y, z, width, height, depth, copie[x][y][z], visited);
                    int fall_offset = find_lowest_position(copie, visited, width, height, depth);
                    if (fall_offset > 0) {
                        apply_gravity_to_body(copie, visited, width, height, depth, fall_offset);
                        for (int i = 0; i < width; i++) {
                            for (int j = 0; j < height; j++) {
                                for (int k = 0; k < depth; k++) {
                                    if (visited[i][j][k]) {
                                        chunk[i][j - fall_offset][k] = chunk[i][j][k];
                                        chunk[i][j][k] = AIR;
                                    }
                                }
                            }
                        }
                    }
                    reset_visited(visited, width, height, depth);
                }
            }
        }
    }

    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            for (int z = 0; z < depth; z++) {
                if (!visited[x][y][z] && chunk[x][y][z] != AIR) {
                    flood_fill(chunk, x, y, z, width, height, depth, chunk[x][y][z], visited);
                    int fall_offset = find_lowest_position(chunk, visited, width, height, depth);
                    if (fall_offset > 0) {
                        apply_gravity_to_body(chunk, visited, width, height, depth, fall_offset);
                    }
                    reset_visited(visited, width, height, depth);
                }
            }
        }
    }
    int max_y = 0;
    for (int y = 0; y < height; y++) {
        int has_blocks = 0;
        for (int x = 0; x < width; x++) {
            for (int z = 0; z < depth; z++) {
                if (chunk[x][y][z] != AIR) {
                    has_blocks = 1;
                    break;
                }
            }
            if (has_blocks) break;
        }
        if (has_blocks) max_y = y;
    }
    *new_height = max_y + 1;
    for (int x = 0; x < width; x++) {
        for (int y = *new_height; y < height; y++) {
            free(chunk[x][y]);
        }
    }
    free_int_triple_pointer(visited, width, height);
    free_char_triple_pointer(copie, width, height);
    return chunk;
}
