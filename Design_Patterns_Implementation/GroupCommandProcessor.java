package org.example;

import java.util.List;
import java.util.Map;

public class GroupCommandProcessor {
    private final Database db;
    private final OutWriter out;

    public GroupCommandProcessor(Database db, OutWriter out) {
        this.db = db;
        this.out = out;
    }

    public void process(List<CommandRow> rows) {
        for (CommandRow row : rows) {
            switch (norm(row.getCommand())) {
                case "ADD GROUP": addGroup(row); break;
                case "FIND GROUP": findGroup(row); break;
                case "REMOVE GROUP": removeGroup(row); break;
                case "ADD MEMBER": addMember(row); break;
                case "FIND MEMBER": findMember(row); break;
                case "REMOVE MEMBER": removeMember(row); break;
                default: break;
            }
        }
    }

    private void addGroup(CommandRow row) {
        try {
            String ip = ip(row.getParams());
            db.addResourceGroup(new ResourceGroup(ip));
            out.println("ADD GROUP: " + ip);
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException) {
                out.println("ADD GROUP: " + e.getMessage() + " ## line no: " + row.getLineNo());
            }
        }
    }

    private void findGroup(CommandRow row) {
        try {
            String ip = ip(row.getParams());
            out.println(db.findGroup(ip).isPresent()
                    ? "FIND GROUP: " + ip
                    : "FIND GROUP: Group not found: ipAddress = " + ip);
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException) {
                out.println("FIND GROUP: " + e.getMessage() + " ## line no: " + row.getLineNo());
            }
        }
    }

    private void removeGroup(CommandRow row) {
        try {
            String ip = ip(row.getParams());
            if (db.findGroup(ip).isPresent()) {
                db.removeResourceGroup(ip);
                out.println("REMOVE GROUP: " + ip);
            } else {
                out.println("REMOVE GROUP: Group not found: ipAddress = " + ip);
            }
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException) {
                out.println("REMOVE GROUP: " + e.getMessage() + " ## line no: " + row.getLineNo());
            }
        }
    }

    private void addMember(CommandRow row) {
        try {
            Map<String, String> p = row.getParams();
            String ip = ip(p);
            String name = name(p);
            String role = role(p);

            ResourceGroup group = db.findGroup(ip).orElse(null);
            if (group == null) {
                out.println("ADD MEMBER: Group not found: ipAddress = " + ip);
                return;
            }

            User user = UserFactory.create(
                    name,
                    role,
                    ParamUtil.get(p, "user_email", "email"),
                    ParamUtil.get(p, "user_department", "department"),
                    ParamUtil.getInt(p, "user_clearance_level", "clearance_level", "clearance")
            );
            group.addMember(user);

            out.println("ADD MEMBER: " + ip + ": name = " + name + " && role = " + role);
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException || e instanceof UserException) {
                out.println("ADD MEMBER: " + e.getMessage() + " ## line no: " + row.getLineNo());
            }
        }
    }

    private void findMember(CommandRow row) {
        try {
            Map<String, String> p = row.getParams();
            String ip = ip(p);
            String name = name(p);
            String role = role(p);
            ResourceGroup group = db.findGroup(ip).orElse(null);
            if (group == null) {
                out.println("FIND MEMBER: Group not found: ipAddress = " + ip);
                return;
            }
            out.println(group.containsMember(name, role)
                    ? "FIND MEMBER: " + ip + ": name = " + name + " && role = " + role
                    : "FIND MEMBER: Member not found: ipAddress = " + ip + ": name = " + name + " && role = " + role);
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException || e instanceof UserException) {
                out.println("FIND MEMBER: " + e.getMessage() + " ## line no: " + row.getLineNo());
            }
        }
    }

    private void removeMember(CommandRow row) {
        try {
            Map<String, String> p = row.getParams();
            String ip = ip(p);
            String name = name(p);
            String role = role(p);

            ResourceGroup group = db.findGroup(ip).orElse(null);
            if (group == null) {
                out.println("REMOVE MEMBER: Group not found: ipAddress = " + ip);
                return;
            }

            User member = group.findMember(name, role);
            if (member != null) {
                group.removeMember(member);
                out.println("REMOVE MEMBER: " + ip + ": name = " + name + " && role = " + role);
            } else {
                out.println("REMOVE MEMBER: Member not found: ipAddress = " + ip + ": name = " + name + " && role = " + role);
            }
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException || e instanceof UserException) {
                out.println("REMOVE MEMBER: " + e.getMessage() + " ## line no: " + row.getLineNo());
            }
        }
    }

    private static String ip(Map<String, String> p) {
        String ip = ParamUtil.get(p, "ip_address", "ipaddress", "ip");
        if (ip.isEmpty()) throw new MissingIpAddressException();
        return ip;
    }

    private static String name(Map<String, String> p) {
        String name = ParamUtil.get(p, "use_name", "user_name", "name", "member_name");
        if (name.isEmpty()) throw new UserException();
        return name;
    }

    private static String role(Map<String, String> p) {
        String role = ParamUtil.get(p, "user_role", "role", "member_role");
        if (role.isEmpty()) throw new UserException();
        return role;
    }

    private static String norm(String s) {
        return s.replaceAll("\\s+", " ");
    }
}
