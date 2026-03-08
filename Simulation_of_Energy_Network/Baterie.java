package Tema1;

public class Baterie extends ComponentaRetea {
    private double max;
    private double energie = 0;

    public Baterie(String id, double cap) {
        super(id);
        this.max = cap;
    }

    public double getCapacitateMaxima() {
        return max;
    }
    public double getEnergieStocata() {
        return energie;
    }

    public double incarca(double x) {
        if (!statusOperational)
            return x;
        double spatiu = max - energie;
        double inc = Math.min(spatiu, x);
        energie += inc;
        return x - inc;
    }

    public double descarca(double x) {
        if (!statusOperational)
            return 0;
        double out = Math.min(energie, x);
        energie -= out;
        return out;
    }
}
