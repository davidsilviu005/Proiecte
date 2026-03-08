package org.example;

public class MissingIpAddressException extends RuntimeException {
    public MissingIpAddressException() {
        super("MissingIpAddressException: Server IP Address was not provided.");
    }
}
