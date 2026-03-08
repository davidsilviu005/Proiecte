package org.example;

public interface AlertSubject {
    void addListener(AlertListener listener);
    void removeListener(AlertListener listener);
    void notifyListeners(Alert alert, OutWriter writer);
}
