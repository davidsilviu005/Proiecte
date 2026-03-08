package org.example;

import java.util.HashMap;
import java.util.Map;

public class Student {
    private final String name, group;
    private final Map<String, Double> examScores;

    public Student(String name, String group) {
        this.name = name;
        this.group = group;
        this.examScores = new HashMap<>();
    }

    public String getName() {
        return name;
    }
    public String getGroup() {
        return group;
    }

    public void setScore(String examName, double score) {
        examScores.put(examName, score);
    }

    public double getScore(String examName) {
        return examScores.getOrDefault(examName, 0.0);
    }
    public Map<String, Double> getAllScores() {
        return examScores;
    }
}