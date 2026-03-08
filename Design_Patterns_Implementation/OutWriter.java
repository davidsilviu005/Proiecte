package org.example;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class OutWriter implements AutoCloseable {
    private final BufferedWriter bw;

    public OutWriter(Path outPath) {
        try {
            bw = Files.newBufferedWriter(outPath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void println(String line) {
        try {
            bw.write(line);
            bw.newLine();
        } catch (IOException ignored) {
        }
    }

    @Override
    public void close() {
        try {
            bw.close();
        } catch (IOException ignored) {
        }
    }
}
