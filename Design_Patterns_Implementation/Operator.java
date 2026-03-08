package org.example;

public class Operator extends User {
    private final String department;

    public Operator(String name, String role, String email, String department) {
        super(name, role, email);
        this.department = department;
    }

    public String getDepartment() {
        return department;
    }
}
