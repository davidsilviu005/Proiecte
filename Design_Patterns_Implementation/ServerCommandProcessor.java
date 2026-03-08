package org.example;

import java.util.List;
import java.util.Map;

public class ServerCommandProcessor {
    private final Database db;
    private final OutWriter out;

    public ServerCommandProcessor(Database db, OutWriter out) {
        this.db = db;
        this.out = out;
    }

    public void process(List<CommandRow> rows) {
        for (CommandRow row : rows) {
            if ("ADD SERVER".equals(row.getCommand())) {
                add(row);
            }
        }
    }

    private void add(CommandRow row) {
        Map<String, String> p = row.getParams();
        int ln = row.getLineNo();

        try {
            String ip = req(p, "ip_address", new MissingIpAddressException());
            String name = req(p, "user_name", new UserException());
            String role = req(p, "user_role", new UserException());
            String country = req(p, "country", new LocationException());

            User owner = UserFactory.create(
                    name,
                    role,
                    ParamUtil.get(p, "user_email"),
                    ParamUtil.get(p, "user_department"),
                    ParamUtil.getInt(p, "user_clearance_level")
            );

            Location loc = new Location(country, ParamUtil.get(p, "city"), null, null, null);

            ServerStatus st = ServerStatus.safeParse(ParamUtil.get(p, "server_status"));
            if (st == null) st = ServerStatus.UP;

            Server s = new Server.Builder(ip, loc, owner).status(st).build();
            db.addServer(s);
            out.println("ADD SERVER: " + ip + ": " + s.getStatus());
        } catch (RuntimeException e) {
            if (e instanceof MissingIpAddressException || e instanceof UserException || e instanceof LocationException) {
                out.println("ADD SERVER: " + e.getMessage() + " ## line no: " + ln);
            }
        }
    }

    private static String req(Map<String, String> p, String k, RuntimeException ex) {
        String v = ParamUtil.get(p, k);
        if (v.isEmpty()) throw ex;
        return v;
    }
}
