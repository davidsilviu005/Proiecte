package org.example;

public enum ServerStatus {
    UP,
    DOWN,
    DEGRADED;

    public static ServerStatus safeParse(String s) {
        try {
            return ServerStatus.valueOf(s);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
