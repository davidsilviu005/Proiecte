package Tema1;

public class ReactorNuclear extends ProducatorEnergie {
    private double constanta;

    public ReactorNuclear(String id, double c) {
        super(id);
        this.constanta = c;
    }

    public double getPutereConstanta() {
        return constanta;
    }

    @Override
    public double calculeazaProductie(double factor) {
        return statusOperational ? constanta : 0;
    }
}
