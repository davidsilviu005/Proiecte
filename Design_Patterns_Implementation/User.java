package org.example;

public class User {
    private final String name;
    private final String role;
    private final String email;

    public User(String name, String role, String email) {
        this.name = name;
        this.role = role;
        this.email = email;
    }

    public String getName() {
        return name;
    }

    public String getRole() {
        return role;
    }

    public String getEmail() {
        return email;
    }
}
