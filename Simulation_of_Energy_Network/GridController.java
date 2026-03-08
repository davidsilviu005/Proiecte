package Tema1;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
 
public class GridController {
    private enum TipProducator {
        SOLAR, TURBINA, REACTOR
    }

    private enum TipConsumator {
        SUPORT_VIATA, LABORATOR, ILUMINAT
    }

    private static class ProducatorEntry {
        String id;
        TipProducator tip;
        double putereSpecific;
        boolean operational = true;

        ProducatorEntry(String id, TipProducator tip, double putereSpecific) {
            this.id = id;
            this.tip = tip;
            this.putereSpecific = putereSpecific;
        }
    }

    private static class ConsumatorEntry {
        String id;
        TipConsumator tip;
        double cerere;
        int prioritate;
        boolean operational = true;
        boolean alimentat = true;

        ConsumatorEntry(String id, TipConsumator tip, double cerere, int prioritate) {
            this.id = id;
            this.tip = tip;
            this.cerere = cerere;
            this.prioritate = prioritate;
        }
    }

    private static class BaterieEntry {
        String id;
        double capacitate;
        double energie;
        boolean operational = true;
        String capacitateText;

        BaterieEntry(String id, double capacitate, String capacitateText) {
            this.id = id;
            this.capacitate = capacitate;
            this.capacitateText = capacitateText;
        }
    }

    private Map<String, Object> componente = new HashMap<>();
    private List<ProducatorEntry> producatori = new ArrayList<>();
    private List<ConsumatorEntry> consumatori = new ArrayList<>();
    private List<BaterieEntry> baterii = new ArrayList<>();

    private boolean inBlackout = false;
    private int tickCounter = 0;
    private List<String> istoric = new ArrayList<>();

    public boolean existaComponenta(String id) {
        return componente.containsKey(id);
    }
    public boolean esteInBlackout() {
        return inBlackout;
    }

    public String adaugaProducator(String tipStr, String id, double putere) {
        TipProducator tip;
        switch (tipStr) {
            case "solar" -> tip = TipProducator.SOLAR;
            case "turbina" -> tip = TipProducator.TURBINA;
            case "reactor" -> tip = TipProducator.REACTOR;
            default -> throw new IllegalArgumentException("Tip producator invalid");
        }
        ProducatorEntry p = new ProducatorEntry(id, tip, putere);
        producatori.add(p);
        componente.put(id, p);
        return "S-a adaugat producatorul " + id + " de tip " + tipStr;
    }

    public String adaugaConsumator(String tipStr, String id, double cerere) {
        TipConsumator tip;
        int prioritate;
        switch (tipStr) {
            case "suport_viata" -> {
                tip = TipConsumator.SUPORT_VIATA;
                prioritate = 1;
            }
            case "laborator" -> {
                tip = TipConsumator.LABORATOR;
                prioritate = 2;
            }
            case "iluminat" -> {
                tip = TipConsumator.ILUMINAT;
                prioritate = 3;
            }
            default -> throw new IllegalArgumentException("Tip consumator invalid");
        }
        ConsumatorEntry c = new ConsumatorEntry(id, tip, cerere, prioritate);
        consumatori.add(c);
        componente.put(id, c);
        return "S-a adaugat consumatorul " + id + " de tip " + tipStr;
    }

    public String adaugaBaterie(String id, double capacitate, String capacitateText) {
        BaterieEntry b = new BaterieEntry(id, capacitate, capacitateText);
        baterii.add(b);
        componente.put(id, b);
        return "S-a adaugat bateria " + id + " cu capacitatea " + capacitateText;
    }

    public String setDefect(String id, boolean statusOperational) {
        Object comp = componente.get(id);
        if (comp == null) {
            return "EROARE: Nu exista componenta cu id-ul " + id;
        }
        if (comp instanceof ProducatorEntry p) {
            p.operational = statusOperational;
        } else if (comp instanceof ConsumatorEntry c) {
            c.operational = statusOperational;
        } else if (comp instanceof BaterieEntry b) {
            b.operational = statusOperational;
        }

        if (!statusOperational) {
            return "Componenta " + id + " este acum defecta";
        } else {
            return "Componenta " + id + " este acum operationala";
        }
    }

    public String simuleazaTick(double factorSoare, double factorVant) {
        if (inBlackout) {
            return "EROARE: Reteaua este in BLACKOUT. Simulare oprita.";
        }
        tickCounter++;

        for (ConsumatorEntry c : consumatori) {
            c.alimentat = true;
        }

        double productieTotala = 0.0;
        for (ProducatorEntry p : producatori) {
            if (!p.operational) {
                continue;
            }
            double prod = 0.0;
            switch (p.tip) {
                case SOLAR -> prod = p.putereSpecific * factorSoare;
                case TURBINA -> prod = p.putereSpecific * factorVant;
                case REACTOR -> prod = p.putereSpecific;
            }
            productieTotala += prod;
        }

        double cerereTotala = 0.0;
        for (ConsumatorEntry c : consumatori) {
            if (!c.operational || !c.alimentat) {
                continue;
            }
            cerereTotala += c.cerere;
        }

        double delta = productieTotala - cerereTotala;
        List<String> decuplati = new ArrayList<>();

        if (delta > 0) {
            double surplus = delta;
            for (BaterieEntry b : baterii) {
                if (!b.operational) {
                    continue;
                }
                if (surplus <= 0) {
                    break;
                }
                double locLiber = b.capacitate - b.energie;
                if (locLiber <= 0) {
                    continue;
                }
                double inc = Math.min(locLiber, surplus);
                b.energie += inc;
                surplus -= inc;
            }
        } else if (delta < 0) {
            double deficit = -delta;

            for (BaterieEntry b : baterii) {
                if (!b.operational) {
                    continue;
                }
                if (deficit <= 0) {
                    break;
                }
                double poateDa = Math.min(b.energie, deficit);
                b.energie -= poateDa;
                deficit -= poateDa;
            }

            if (deficit > 0) {
                List<ConsumatorEntry> sortati = new ArrayList<>(consumatori);
                sortati.sort(Comparator.comparingInt((ConsumatorEntry c) -> c.prioritate).reversed());

                for (ConsumatorEntry c : sortati) {
                    if (deficit <= 0) {
                        break;
                    }
                    if (!c.operational || !c.alimentat) {
                        continue;
                    }
                    if (c.prioritate <= 1) {
                        continue;
                    }
                    c.alimentat = false;
                    deficit -= c.cerere;
                    decuplati.add(c.id);
                }
                if (deficit > 0) {
                    inBlackout = true;
                    String event = String.format(Locale.US, "Tick %d: BLACKOUT! SIMULARE OPRITA.", tickCounter);
                    istoric.add(event);
                    return "BLACKOUT! SIMULARE OPRITA.";
                }
            }
        }

        double energieBaterii = 0.0;
        for (BaterieEntry b : baterii) {
            energieBaterii += b.energie;
        }
        String decuplatiStr = String.join(", ", decuplati);
        String tickMsg = String.format(Locale.US, "TICK: Productie %.2f, Cerere %.2f. Baterii: %.2f MW. Decuplati: [%s]",
                productieTotala, cerereTotala, energieBaterii, decuplatiStr);
        return tickMsg;
    }

    public String statusGrid() {
        if (producatori.isEmpty() && consumatori.isEmpty() && baterii.isEmpty()) {
            return "Reteaua este goala";
        }

        String s = "";
        s += "Stare Retea: " + (inBlackout ? "BLACKOUT" : "STABILA") + "\n";
        for (ProducatorEntry p : producatori) {
            String tipClassName = switch (p.tip) {
                case SOLAR -> "PanouSolar";
                case TURBINA -> "TurbinaEoliana";
                case REACTOR -> "ReactorNuclear";
            };
            String status = p.operational ? "Operational" : "Defect";
            s += String.format(Locale.US,
                    "Producator %s (%s) - PutereBaza: %.2f - Status: %s%n",
                    p.id, tipClassName, p.putereSpecific, status);

        }
        for (ConsumatorEntry c : consumatori) {
            String tipClassName = switch (c.tip) {
                case SUPORT_VIATA -> "SistemSuportViata";
                case LABORATOR -> "LaboratorStiintific";
                case ILUMINAT -> "SistemIluminat";
            };
            String status;
            if (!c.operational) {
                status = "Defect";
            } else if (!c.alimentat) {
                status = "Decuplat";
            } else {
                status = "Alimentat";
            }

            s += String.format(Locale.US,
                    "Consumator %s (%s) - Cerere: %.2f - Prioritate: %d - Status: %s%n",
                    c.id, tipClassName, c.cerere, c.prioritate, status);

        }
        for (BaterieEntry b : baterii) {
            String status = b.operational ? "Operational" : "Defect";
            s += String.format(Locale.US,
                    "Baterie %s - Stocare: %.2f/%.2f - Status: %s%n",
                    b.id, b.energie, b.capacitate, status);
        }
        return s;
    }

    public String istoricEvenimente() {
        if (istoric.isEmpty()) {
            return "Istoric evenimente gol";
        }
        String s = "";
        for (String event : istoric) {
            s += event + "\n";
        }
        return s;
    }
}
