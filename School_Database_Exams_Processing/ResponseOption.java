package org.example;

public enum ResponseOption {
    A, B, C, D;

    public static ResponseOption fromString(String s) {
        return ResponseOption.valueOf(s.trim().toUpperCase());
    }
}