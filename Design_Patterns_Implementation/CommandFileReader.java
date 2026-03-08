package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CommandFileReader {
    private CommandFileReader() {}

    public static List<CommandRow> read(Path inPath) throws IOException {
        List<CommandRow> rows = new ArrayList<>();
        try (BufferedReader br = Files.newBufferedReader(inPath)) {
            String headerLine = br.readLine();
            String[] header = headerLine.split("\\|", -1);
            String line;
            int lineNo = 0;

            while ((line = br.readLine()) != null) {
                lineNo++;
                String[] t = line.split("\\|", -1);

                Map<String, String> params = new HashMap<>();
                for (int i = 1; i < header.length; i++) {
                    String key = header[i];
                    String val = i < t.length ? t[i] : "";
                    params.put(key, val);
                }

                String cmd = t.length > 0 ? t[0] : "";
                rows.add(new CommandRow(cmd, params, lineNo));
            }
        }
        return rows;
    }
}
