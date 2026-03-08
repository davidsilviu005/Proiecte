package org.example;

import java.time.LocalDateTime;
import java.util.*;

public class Exam {
    private final String name;
    private final LocalDateTime start;
    private final LocalDateTime end;

    private final List<Question> questions = new ArrayList<>();
    private final Map<String, Double> results = new HashMap<>();

    public Exam(String name, LocalDateTime start, LocalDateTime end) {
        this.name = name;
        this.start = start;
        this.end = end;
    }

    public void addQuestion(Question q) {
        questions.add(q);
    }

    public List<Question> getQuestionsSortedForExam() {
        List<Question> copy = new ArrayList<>(questions);
        copy.sort(Comparator.comparingInt(Question::getDifficulty)
                .thenComparing(Question::getText));
        return copy;
    }

    public List<Question> getQuestionsHistorySorted() {
        List<Question> copy = new ArrayList<>(questions);
        copy.sort(Comparator.comparing(Question::getAddedAt)
                .thenComparing(Question::getAuthor));
        return copy;
    }

    public void submit(Student student, List<String> answers, LocalDateTime ts)
            throws SubmissionOutsideTimeIntervalException {
        if(ts.isBefore(start) || ts.isAfter(end)) {
            throw new SubmissionOutsideTimeIntervalException(ts, student.getName());
        }

        double total = 0.0;
        List<Question> printOrder = getQuestionsSortedForExam();

        for (int i = 0; i < printOrder.size(); i++) {
            Question q = printOrder.get(i);
            Correctness c = q.checkAnswer(answers.get(i));
            total += q.getScorePercent(c) * q.getMaxScore();
        }

        results.put(student.getName(), total);
        student.setScore(name, total);
    }
    public Map<String, Double> getResults() {
        return results;
    }
}