package org.example;

import java.util.ArrayList;
import java.util.List;

public class Server implements AlertSubject {
    private final String ipAddress;
    private final Location location;
    private final User owner;

    private final String hostname;
    private final ServerStatus status;
    private final Integer cpuCores;
    private final Integer ramGb;
    private final Integer storageGb;

    private final List<AlertListener> listeners = new ArrayList<>();

    private Server(Builder b) {
        this.ipAddress = b.ipAddress;
        this.location = b.location;
        this.owner = b.owner;

        this.hostname = b.hostname;
        this.status = b.status;
        this.cpuCores = b.cpuCores;
        this.ramGb = b.ramGb;
        this.storageGb = b.storageGb;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public Location getLocation() {
        return location;
    }

    public User getOwner() {
        return owner;
    }

    public String getHostname() {
        return hostname;
    }

    public ServerStatus getStatus() {
        return status;
    }

    public Integer getCpuCores() {
        return cpuCores;
    }

    public Integer getRamGb() {
        return ramGb;
    }

    public Integer getStorageGb() {
        return storageGb;
    }

    public void raiseAlert(Alert alert, OutWriter writer) {
        notifyListeners(alert, writer);
    }

    @Override
    public void addListener(AlertListener listener) {
        listeners.add(listener);
    }

    @Override
    public void removeListener(AlertListener listener) {
        listeners.remove(listener);
    }

    @Override
    public void notifyListeners(Alert alert, OutWriter writer) {
        for (AlertListener l : listeners) {
            l.onAlert(alert, writer);
        }
    }

    //Builder
    public static class Builder {
        private final String ipAddress;
        private final Location location;
        private final User owner;

        private String hostname;
        private ServerStatus status = ServerStatus.UP;
        private Integer cpuCores;
        private Integer ramGb;
        private Integer storageGb;

        public Builder(String ipAddress, Location location, User owner) {
            this.ipAddress = ipAddress;
            this.location = location;
            this.owner = owner;
        }

        public Builder hostname(String hostname) {
            this.hostname = hostname;
            return this;
        }

        public Builder status(ServerStatus status) {
            if (status != null) {
                this.status = status;
            }
            return this;
        }

        public Builder cpuCores(Integer cpuCores) {
            this.cpuCores = cpuCores;
            return this;
        }

        public Builder ramGb(Integer ramGb) {
            this.ramGb = ramGb;
            return this;
        }

        public Builder storageGb(Integer storageGb) {
            this.storageGb = storageGb;
            return this;
        }

        public Server build() {
            return new Server(this);
        }
    }
}
