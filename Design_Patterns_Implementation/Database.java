package org.example;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

//Singleton
public class Database {
    private static final Database instance = new Database(  );
    private final Map<String, Server> servers = new HashMap<>();
    private final Map<String, ResourceGroup> resourceGroups = new HashMap<>();
    private final Set<Alert> alerts = new HashSet<>();

    private Database() {}

    public static Database getInstance() {
        return instance;
    }

    public void addServer(Server server) {
        servers.put(server.getIpAddress(), server);
    }

    public void addResourceGroup(ResourceGroup group) {
        resourceGroups.put(group.getIpAddress(), group);
    }

    public boolean removeResourceGroup(String ipAddress) {
        return ipAddress != null && resourceGroups.remove(ipAddress) != null;
    }

    public void addAlert(Alert alert) {
        alerts.add(alert);
    }

    public Set<Server> getServers() {
        return Set.copyOf(servers.values());
    }

    public Set<ResourceGroup> getResourceGroups() {
        return Set.copyOf(resourceGroups.values());
    }

    public Set<Alert> getAlerts() {
        return Collections.unmodifiableSet(alerts);
    }

    public Optional<Server> findServer(String ipAddress) {
        //verificam daca ipAddress == null
        //daca ip-ul este invalid Optional.ofNullable intoarce server daca exista, altfel null
        return Optional.ofNullable(ipAddress == null ? null : servers.get(ipAddress));
    }

    public Optional<ResourceGroup> findGroup(String ipAddress) {
        return Optional.ofNullable(ipAddress == null ? null : resourceGroups.get(ipAddress));
    }
}
