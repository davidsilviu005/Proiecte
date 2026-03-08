package org.example;

public class Alert {
    private final AlertType type;
    private final Severity severity;
    private final String message;
    private final String ipAddress;

    public Alert(AlertType type, Severity severity, String message, String ipAddress) {
        this.type = type;
        this.severity = severity;
        this.message = message;
        this.ipAddress = ipAddress;
    }
    public AlertType getType() {
        return type;
    }
    public Severity getSeverity() {
        return severity;
    }
    public String getMessage() {
        return message;
    }
    public String getIpAddress() {
        return ipAddress;
    }
}
