package org.example;

public class UserException extends RuntimeException {
    public UserException() {
        super("UserException: Name and role can't be empty.");
    }
}
