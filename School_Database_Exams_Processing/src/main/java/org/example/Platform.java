package org.example;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.*;

public class Platform {
    private final Map<String, Exam> exams = new HashMap<>();
    private final Map<String, Student> students = new HashMap<>();
    private final FileWriter console;
    private final Path basePath;

    public Platform(Path base) throws IOException {
        this.basePath = base;
        this.console = new FileWriter(basePath.resolve("console.out").toString());
    }

    public void createExam(String name, LocalDateTime start, LocalDateTime end) {
        exams.put(name, new Exam(name, start, end));
    }

    public void addQuestion(String type, String examName, String author,
                            int difficulty, double maxScore, String text,
                            String correctAnswer, LocalDateTime timestamp) {
        Exam exam = exams.get(examName);
        Question q;

        switch (type) {
            case "open_ended":
                q = new OpenEndedQuestion(text, author, timestamp, difficulty, maxScore, correctAnswer);
                break;
            case "fill_in_the_blank":
                q = new FillInTheBlankQuestion(text, author, timestamp, difficulty, maxScore, correctAnswer);
                break;
            case "multiple_choice":
                q = new MultipleChoiceQuestion(text, author, timestamp, difficulty, maxScore,
                        ResponseOption.valueOf(correctAnswer));
                break;
            default:
                return;
        }
        exam.addQuestion(q);
    }

    public void printExam(String examName, LocalDateTime ts) throws IOException {
        Exam exam = exams.get(examName);
        FileWriter fw = new FileWriter(
                basePath.resolve("print_exam_" + examName + "_" + ts.format(Main.F) + ".out").toString());
        for (Question q : exam.getQuestionsSortedForExam()) {
            fw.write(String.format("%.1f | %s | %d | %s\n",
                    q.getMaxScore(), q.getText(),
                    q.getDifficulty(), q.getCorrectAnswerAsString()));
        }
        fw.close();
    }

    public void listQuestionsHistory(String examName, LocalDateTime ts) throws IOException {
        Exam exam = exams.get(examName);

        FileWriter fw = new FileWriter(basePath.resolve("questions_history_" + examName + "_" +
                ts.format(Main.F) + ".out").toString());
        for (Question q : exam.getQuestionsHistorySorted()) {
            fw.write(String.format("%s | %s | %s | %d | %.1f | %s\n",
                    q.getAddedAt().format(Main.F), q.getText(), q.getCorrectAnswerAsString(),
                    q.getDifficulty(), q.getMaxScore(), q.getAuthor()));
        }
        fw.close();
    }

    public void registerStudent(String name, String group) {
        students.put(name, new Student(name, group));
    }

    public void submitExam(String examName, String studentName, LocalDateTime ts, List<String> answers)
            throws IOException {
        Exam exam = exams.get(examName);
        Student student = students.get(studentName);
        try {
            exam.submit(student, answers, ts);
        } catch (SubmissionOutsideTimeIntervalException e) {
            student.setScore(examName, 0.0);
            console.write(e.toString() + "\n");
        }
    }

    public void showStudentScore(String studentName, String examName, LocalDateTime ts) throws IOException {
        double score = students.get(studentName).getScore(examName);

        console.write(String.format("%s | The score of %s for exam %s is %.2f\n",
                ts.format(Main.F), studentName, examName, score));
    }

    public void generateReport(String examName, LocalDateTime ts) throws IOException {
        Exam exam = exams.get(examName);
        FileWriter fw = new FileWriter(basePath.resolve("exam_report_" + examName + "_" +
                ts.format(Main.F) + ".out").toString());

        List<Map.Entry<String, Double>> list = new ArrayList<>(exam.getResults().entrySet());
        list.sort(Map.Entry.comparingByKey());

        for (var e : list) {
            fw.write(e.getKey() + " | " + String.format("%.2f", e.getValue()) + "\n");
        }
        fw.close();
    }

    public void close() throws IOException {
        console.close();
    }
}