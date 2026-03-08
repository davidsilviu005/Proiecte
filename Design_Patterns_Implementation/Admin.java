package org.example;

public class Admin extends Operator {
    private final int clearanceLevel;

    public Admin(String name, String role, String email, String department, int clearanceLevel) {
        super(name, role, email, department);
        this.clearanceLevel = clearanceLevel;
    }
    public int getClearanceLevel() {
        return clearanceLevel;
    }
}
