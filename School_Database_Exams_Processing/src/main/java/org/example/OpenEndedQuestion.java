package org.example;

import java.time.LocalDateTime;

public class OpenEndedQuestion extends Question {

    private final String correctAnswer;

    public OpenEndedQuestion(String text, String author,
                             LocalDateTime addedAt, int difficulty,
                             double maxScore, String correctAnswer) {
        super (text, author, addedAt, difficulty, maxScore);
        this.correctAnswer = correctAnswer;
    }

    @Override
    public Correctness checkAnswer(String answer) {
        if (answer.equals(correctAnswer)) {
            return Correctness.CORRECT;
        }

        int len = correctAnswer.length();
        int min = (int) (len * 0.7);
        int max = (int) (len * 1.3);

        if (answer.length() >= min && answer.length() <= max &&
                (correctAnswer.contains(answer) || answer.contains(correctAnswer))) {
            return Correctness.PARTIALLY_CORRECT;
        }
        return Correctness.WRONG;
    }

    @Override
    public double getScorePercent(Correctness correctness) {
        return switch (correctness) {
            case CORRECT -> 1.0;
            case PARTIALLY_CORRECT -> 0.7;
            case WRONG -> 0.0;
        };
    }

    @Override
    public String getCorrectAnswerAsString() {
        return correctAnswer;
    }
}