package org.example;

import java.util.ArrayList;
import java.util.List;

public class ResourceGroup implements AlertListener {
    private final String ipAddress;
    private final List<User> members = new ArrayList<>();

    public ResourceGroup(String ipAddress) {
        this.ipAddress = ipAddress;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public void addMember(User member) {
        if (member != null) members.add(member);
    }

    public boolean removeMember(User member) {
        return members.remove(member);
    }

    public boolean containsMember(String name, String role) {
        for (User u : members) {
            if (name.equals(u.getName()) && role.equals(u.getRole())) return true;
        }
        return false;
    }

    public User findMember(String name, String role) {
        for (User u : members) {
            if (name.equals(u.getName()) && role.equals(u.getRole())) return u;
        }
        return null;
    }

    @Override
    public void onAlert(Alert alert, OutWriter writer) {
        //...
    }
}
