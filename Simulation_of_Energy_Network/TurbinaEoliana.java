package Tema1;

public class TurbinaEoliana extends ProducatorEnergie {
    private double baza;

    public TurbinaEoliana(String id, double baza) {
        super(id);
        this.baza = baza;
    }

    public double getPutereBaza() {
        return baza;
    }

    @Override
    public double calculeazaProductie(double factor) {
        return statusOperational ? baza * factor : 0;
    }
}
