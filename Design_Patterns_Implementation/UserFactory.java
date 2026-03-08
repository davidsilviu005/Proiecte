package org.example;

//factory
public final class UserFactory {
    private UserFactory() {}

    public static User create(String name, String role, String email, String department, Integer clearanceLevel) {
        if (clearanceLevel != null) {
            return new Admin(name, role, email, department, clearanceLevel);
        }
        if (department != null && !department.isEmpty()) {
            return new Operator(name, role, email, department);
        }
        return new User(name, role, email);
    }
}
