package Tema1;

public class PanouSolar extends ProducatorEnergie {
    private double max;

    public PanouSolar(String id, double max) {
        super(id);
        this.max = max;
    }

    public double getPutereMaxima() {
        return max;
    }

    @Override
    public double calculeazaProductie(double factor) {
        return statusOperational ? max * factor : 0;
    }
}
