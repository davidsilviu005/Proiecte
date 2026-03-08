package org.example;

public class LocationException extends RuntimeException {
    public LocationException() {
        super("LocationException: Country is missing.");
    }
}
