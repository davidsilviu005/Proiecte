package Tema1;

public abstract class ProducatorEnergie extends ComponentaRetea {
    public ProducatorEnergie(String id) {
        super(id);
    }
    public abstract double calculeazaProductie(double factor);
}
