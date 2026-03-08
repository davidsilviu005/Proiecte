package org.example;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        PathTypes pathType = PathTypes.fromValue(args[0]);
        Database db = Database.getInstance();
        switch (pathType) {
            case SERVERS:
                runServers(db, args[1]);
                break;
            case GROUPS:
                runGroups(db, args[1]);
                break;
            case LISTENER:
                String serversBase = args[1];
                String groupsBase = args[2];
                String eventsBase = args[3];
                runServers(db, serversBase);
                runGroups(db, groupsBase);
                runEvents(db, eventsBase);
                break;
            default:
                break;
        }
    }

    public static void runServers(Database db, String basePath) {
        Path inPath = Path.of(basePath + ".in");
        Path outPath = Path.of(basePath + ".out");

        try (OutWriter out = new OutWriter(outPath)) {
            List<CommandRow> rows = CommandFileReader.read(inPath);
            new ServerCommandProcessor(db, out).process(rows);
        } catch (IOException ignored) {
        }
    }

    public static void runGroups(Database db, String basePath) {
        Path inPath = Path.of(basePath + ".in");
        Path outPath = Path.of(basePath + ".out");

        try (OutWriter out = new OutWriter(outPath)) {
            List<CommandRow> rows = CommandFileReader.read(inPath);
            new GroupCommandProcessor(db, out).process(rows);
        } catch (IOException ignored) {
        }
    }

    public static void runEvents(Database db, String basePath) {
        Path inPath = Path.of(basePath + ".in");
        Path outPath = Path.of(basePath + ".out");

        try (OutWriter out = new OutWriter(outPath)) {
            List<CommandRow> rows = CommandFileReader.read(inPath);
            new EventCommandProcessor(db, out).process(rows);
        } catch (IOException ignored) {
        }
    }
}
