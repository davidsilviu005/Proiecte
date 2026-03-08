package org.example;

import java.time.LocalDateTime;

public abstract class Question implements Gradable {
    protected final String text;
    protected final String author;
    protected final LocalDateTime addedAt;
    protected final int difficulty;
    protected final double maxScore;

    protected Question(String text, String author, LocalDateTime addedAt, int difficulty, double maxScore) {
        this.text = text;
        this.author = author;
        this.addedAt = addedAt;
        this.difficulty = difficulty;
        this.maxScore = maxScore;
    }

    public int getDifficulty() {
        return difficulty;
    }

    public String getText() {
        return text;
    }

    public String getAuthor() {
        return author;
    }

    public LocalDateTime getAddedAt() {
        return addedAt;
    }

    public double getMaxScore() {
        return maxScore;
    }

    public abstract Correctness checkAnswer(String answer);
    public abstract String getCorrectAnswerAsString();
}