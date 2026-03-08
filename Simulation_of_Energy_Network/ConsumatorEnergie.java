package Tema1;

public abstract class ConsumatorEnergie extends ComponentaRetea {
    protected double cerere;
    protected int prioritate;
    protected boolean alimentat = true;

    public ConsumatorEnergie(String id, double cerere, int prioritate) {
        super(id);
        this.cerere = cerere;
        this.prioritate = prioritate;
    }

    public double getCerereCurenta() {
        return alimentat ? cerere : 0;
    }
    public void cupleazaLaRetea() {
        alimentat = true;
    }
    public void decupleazaDeLaRetea() {
        alimentat = false;
    }
    public int getPrioritate() {
        return prioritate;
    }
    public boolean isEsteAlimentat() {
        return alimentat;
    }
    public double getCerereEnergie() {
        return cerere;
    }
}
