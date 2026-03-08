package org.example;

public enum AlertType {
    ANOMALY,
    ADVISORY;

    public static AlertType safeParse(String s) {
        return AlertType.valueOf(s);
    }
}
