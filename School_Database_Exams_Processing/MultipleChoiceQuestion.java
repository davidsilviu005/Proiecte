package org.example;

import java.time.LocalDateTime;

public class MultipleChoiceQuestion extends Question {
    private final ResponseOption correctAnswer;

    public MultipleChoiceQuestion(String text, String author,
                                  LocalDateTime addedAt, int difficulty,
                                  double maxScore, ResponseOption correctAnswer) {
        super(text, author, addedAt, difficulty, maxScore);
        this.correctAnswer = correctAnswer;
    }

    @Override
    public Correctness checkAnswer(String answer) {
        try {
            ResponseOption given = ResponseOption.valueOf(answer);
            return given == correctAnswer
                    ? Correctness.CORRECT
                    : Correctness.WRONG;
        } catch (IllegalArgumentException e) {
            return Correctness.WRONG;
        }
    }

    @Override
    public double getScorePercent(Correctness correctness) {
        return correctness == Correctness.CORRECT ? 1.0 : 0.0;
    }

    @Override
    public String getCorrectAnswerAsString() {
        return correctAnswer.name();
    }
}