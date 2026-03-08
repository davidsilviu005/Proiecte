package Tema1;

public class ComponentaRetea {
    protected String id;
    protected boolean statusOperational = true;

    public ComponentaRetea(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }
    public boolean isStatusOperational() {
        return statusOperational;
    }
    public void setStatusOperational(boolean st) {
        statusOperational = st;
    }
}
