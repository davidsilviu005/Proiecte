package org.example;

import java.time.LocalDateTime;

public class SubmissionOutsideTimeIntervalException extends Exception {
    private final LocalDateTime timestamp;
    private final String studentName;

    public SubmissionOutsideTimeIntervalException(LocalDateTime timestamp, String studentName) {
        this.timestamp = timestamp;
        this.studentName = studentName;
    }

    @Override
    public String toString() {
        return timestamp.format(Main.F) +
                " | Submission outside of time interval for student " + studentName;
    }
}