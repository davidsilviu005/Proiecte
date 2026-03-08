package org.example;

import java.util.List;
import java.util.Map;

public class EventCommandProcessor {
    private final Database db;
    private final OutWriter out;

    public EventCommandProcessor(Database db, OutWriter out) {
        this.db = db;
        this.out = out;
    }

    public void process(List<CommandRow> rows) {
        for (CommandRow row : rows) {
            String cmd = norm(row.getCommand());
            if ("ADD EVENT".equals(cmd) || "ADD ALERT".equals(cmd)) {
                addEvent(row);
            }
        }
    }

    private void addEvent(CommandRow row) {
        Map<String, String> p = row.getParams();

        String ip = ParamUtil.get(p, "ip_address", "ipaddress", "ip");

        AlertType type = AlertType.safeParse(ParamUtil.get(p, "alert_type", "type"));
        if (type == null) type = AlertType.ANOMALY;

        Severity sev = Severity.safeParse(ParamUtil.get(p, "alert_severity", "severity", "severity_level"));
        if (sev == null) sev = Severity.LOW;

        String msg = ParamUtil.get(p, "message", "alert_message");

        Alert alert = new Alert(type, sev, msg, ip);
        db.addAlert(alert);

        //Observer
        Server server = db.findServer(ip).orElse(null);
        ResourceGroup group = db.findGroup(ip).orElse(null);
        if (server != null && group != null) {
            server.removeListener(group);
            server.addListener(group);
            server.raiseAlert(alert, out);
        }
        out.println("ADD EVENT: " + ip + ": type = " + type + " && severity = " + sev + " && message = " + msg);
    }

    private String norm(String s) {
        return s.replaceAll("\\s+", " ");
    }
}
