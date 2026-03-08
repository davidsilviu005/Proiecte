package org.example;

public enum PathTypes {
    GROUPS("GROUPS"),
    LISTENER("LISTENER"),
    SERVERS("SERVERS");

    private final String value;

    PathTypes(String value) {
        this.value = value;
    }

    public String getValue() {
        return this.value;
    }

    public static PathTypes fromValue(String v) {
        for (PathTypes t : values()) {
            if (t.value.equals(v) || t.name().equals(v)) {
                return t;
            }
        }
        throw new IllegalArgumentException("Unknown path type: " + v);
    }
}
