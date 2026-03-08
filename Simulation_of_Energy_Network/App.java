package Tema1;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;
import java.text.*;

public class App {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner scanner = new Scanner(System.in);
        GridController grid = new GridController();

        while (true) {
            if (!scanner.hasNextLine()) {
                break;
            }

            String line = scanner.nextLine().trim();
            if (line.isEmpty()) {
                continue;
            }

            String[] tokens = line.split("\\s+");
            String cmdStr = tokens[0];

            int cmd;
            try {
                cmd = Integer.parseInt(cmdStr);
            } catch (NumberFormatException e) {
                System.out.println("EROARE: Comanda necunoscuta.");
                continue;
            }
            if (cmd == 7) {
                System.out.println("Simulatorul se inchide.");
                break;
            }
            switch (cmd) {
                case 0 -> handleAppProducator(tokens, grid);
                case 1 -> handleAddConsumator(tokens, grid);
                case 2 -> handleAddBaterie(tokens, grid);
                case 3 -> handleTick(tokens, grid);
                case 4 -> handleSetDefect(tokens, grid);
                case 5 -> handleStatusGrid(tokens, grid);
                case 6 -> handleIstoric(tokens, grid);
                default -> System.out.println("EROARE: Comanda necunoscuta.");
            }
        }
        scanner.close();
    }
    private static void handleAppProducator(String[] tokens, GridController grid) {
        if (grid.esteInBlackout()) {
            System.out.println("EROARE: Reteaua este in BLACKOUT. Simulare oprita.");
            return;
        }
        if (tokens.length != 4) {
            System.out.println("EROARE: Format comanda invalid");
            return;
        }
        String tip = tokens[1];
        String id = tokens[2];
        String putereStr = tokens[3];

        double putere;
        try {
            putere = Double.parseDouble(putereStr);
        } catch (NumberFormatException e) {
            System.out.println("EROARE: Putere invalida");
            return;
        }

        if (putere <= 0) {
            System.out.println("EROARE: Putere invalida");
            return;
        }

        if (!tip.equals("solar") && !tip.equals("turbina") && !tip.equals("reactor")) {
            System.out.println("EROARE: Tip producator invalid");
            return;
        }
        if (grid.existaComponenta(id)) {
            System.out.println("EROARE: Exista deja o componenta cu id-ul " + id);
            return;
        }
        String msg = grid.adaugaProducator(tip, id, putere);
        System.out.println(msg);
    }

    private static void handleAddConsumator(String[] tokens, GridController grid) {
        if (grid.esteInBlackout()) {
            System.out.println("EROARE: Reteaua este in BLACKOUT. Simulare oprita.");
            return;
        }
        if (tokens.length != 4) {
            System.out.println("EROARE: Format comanda invalid");
            return;
        }
        String tip = tokens[1];
        String id = tokens[2];
        String cerereStr = tokens[3];

        double cerere;
        try {
            cerere = Double.parseDouble(cerereStr);
        } catch (NumberFormatException e) {
            System.out.println("EROARE: Cerere putere invalida");
            return;
        }

        if (cerere <= 0) {
            System.out.println("EROARE: Cerere putere invalida");
            return;
        }
        if (!tip.equals("suport_viata") && !tip.equals("laborator") && !tip.equals("iluminat")) {
            System.out.println("EROARE: Tip consumator invalid");
            return;
        }

        if (grid.existaComponenta(id)) {
            System.out.println("EROARE: Exista deja o componenta cu id-ul " + id);
            return;
        }

        String msg = grid.adaugaConsumator(tip, id, cerere);
        System.out.println(msg);
    }

    private static void handleAddBaterie(String[] tokens, GridController grid) {
        if (grid.esteInBlackout()) {
            System.out.println("EROARE: Reteaua este in BLACKOUT. Simulare oprita.");
            return;
        }
        if (tokens.length != 3) {
            System.out.println("EROARE: Format comanda invalid");
            return;
        }

        String id = tokens[1];
        String capacitateStr = tokens[2];
        double capacitate;
        try {
            capacitate = Double.parseDouble(capacitateStr);
        } catch (NumberFormatException e) {
            System.out.println("EROARE: Capacitate invalida");
            return;
        }

        if (capacitate <= 0) {
            System.out.println("EROARE: Capacitate invalida");
            return;
        }
        if (grid.existaComponenta(id)) {
            System.out.println("EROARE: Exista deja o componenta cu id-ul " + id);
            return;
        }
        String msg = grid.adaugaBaterie(id, capacitate, capacitateStr);
        System.out.println(msg);
    }

    private static void handleTick(String[] tokens, GridController grid) {
        if (tokens.length != 3) {
            System.out.println("EROARE: Format comanda invalid");
            return;
        }

        String fSoareStr = tokens[1];
        String fVantStr = tokens[2];

        double fSoare, fVant;
        try {
            fSoare = Double.parseDouble(fSoareStr);
            fVant = Double.parseDouble(fVantStr);
        } catch (NumberFormatException e) {
            System.out.println("EROARE: Factori invalizi");
            return;
        }

        String msg = grid.simuleazaTick(fSoare, fVant);
        System.out.println(msg);
    }

    private static void handleSetDefect(String[] tokens, GridController grid) {
        if (grid.esteInBlackout()) {
            System.out.println("EROARE: Reteaua este in BLACKOUT. Simulare oprita.");
            return;
        }

        if (tokens.length != 3) {
            System.out.println("EROARE: Format comanda invalid");
            return;
        }

        String id = tokens[1];
        String statusStr = tokens[2];

        Boolean status;
        if ("true".equals(statusStr)) {
            status = true;
        } else if ("false".equals(statusStr)) {
            status = false;
        } else {
            System.out.println("EROARE: Status invalid");
            return;
        }

        String msg = grid.setDefect(id, status);
        System.out.println(msg);
    }

    private static void handleStatusGrid(String[] tokens, GridController grid) {
        String msg = grid.statusGrid();
        System.out.println(msg);
    }

    private static void handleIstoric(String[] tokens, GridController grid) {
        String msg = grid.istoricEvenimente();
        System.out.println(msg);
    }
}