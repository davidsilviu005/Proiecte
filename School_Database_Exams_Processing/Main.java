package org.example;

import java.io.BufferedReader;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class Main {
    static final DateTimeFormatter F = DateTimeFormatter.ofPattern("dd-MM-yyyy-HH-mm");

    public static void main(String[] args) {
        try {
            Path base = Paths.get("src/main/resources").resolve(args[0]);
            Platform p = new Platform(base);
            try (BufferedReader br = Files.newBufferedReader(base.resolve("input.in"))) {
                for (String line; (line = br.readLine()) != null; ) {
                    String[] x = line.split("\\|");
                    for (int i = 0; i < x.length; i++)
                        x[i] = x[i].trim();
                    if ("exit".equals(x[1]))
                        break;
                    LocalDateTime ts = LocalDateTime.parse(x[0], F);
                    switch (x[1]) {
                        case "create_exam" -> p.createExam(x[2], LocalDateTime.parse(x[3], F), LocalDateTime.parse(x[4], F));
                        case "add_question" -> p.addQuestion(x[2], x[3], x[4], Integer.parseInt(x[5]), Double.parseDouble(x[6]), x[7], x[8], ts);
                        case "register_student" -> p.registerStudent(x[2], x[3]);
                        case "print_exam" -> p.printExam(x[2], ts);
                        case "list_questions_history" -> p.listQuestionsHistory(x[2], ts);
                        case "submit_exam" -> p.submitExam(x[2], x[3], ts, Arrays.asList(Arrays.copyOfRange(x, 4, x.length)));
                        case "show_student_score" -> p.showStudentScore(x[2], x[3], ts);
                        case "generate_report" -> p.generateReport(x[2], ts);
                    }
                }
            } finally {
                p.close();
            }
        } catch (Exception ignored) { }
    }
}