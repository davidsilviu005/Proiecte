package org.example;

public enum Severity {
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL;

    public static Severity safeParse(String s) {
        try {
            return Severity.valueOf(s);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
