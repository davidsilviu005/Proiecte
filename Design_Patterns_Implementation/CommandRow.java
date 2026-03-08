package org.example;

import java.util.Map;

public class CommandRow {
    private final String command;
    private final Map<String, String> params;
    private final int lineNo;

    public CommandRow(String command, Map<String, String> params, int lineNo) {
        this.command = command;
        this.params = params;
        this.lineNo = lineNo;
    }

    public String getCommand() {
        return command;
    }
    public Map<String, String> getParams() {
        return params;
    }
    public int getLineNo() {
        return lineNo;
    }
}
