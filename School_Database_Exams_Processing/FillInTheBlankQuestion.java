package org.example;

import java.time.LocalDateTime;

public class FillInTheBlankQuestion extends Question {
    private final String correctAnswer;

    public FillInTheBlankQuestion(String text, String author,
                                  LocalDateTime addedAt, int difficulty,
                                  double maxScore, String correctAnswer) {
        super(text, author, addedAt, difficulty, maxScore);
        this.correctAnswer = correctAnswer;
    }

    @Override
    public Correctness checkAnswer(String answer) {
        if (answer.equals(correctAnswer)) {
            return Correctness.CORRECT;
        }

        int len = correctAnswer.length();

        if (Math.abs(answer.length() - len) <= 2 &&
                (correctAnswer.contains(answer) || answer.contains(correctAnswer))) {
            return Correctness.PARTIALLY_CORRECT;
        }
        return Correctness.WRONG;

    }
    @Override
    public double getScorePercent(Correctness correctness) {
        return switch (correctness) {
            case CORRECT -> 1.0;
            case PARTIALLY_CORRECT -> 0.5;
            case WRONG -> 0.0;
        };
    }

    @Override
    public String getCorrectAnswerAsString() {
        return correctAnswer;
    }
}