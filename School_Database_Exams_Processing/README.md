Application structure

- main reads and parses commands, then calls Platform methods.
- platform coordinates the application logic, exams, students, and output files.
- exam models an exam, its questions, and students' score histories.
- question is the base class for the question types.
- openEndedQuestion, fillInTheBlankQuestion, and multipleChoiceQuestion check answers and calculate scores.
- student stores student information and the current exam score.
- submissionOutsideTimeIntervalException is thrown when a student attempts an exam outside the allowed interval.

Why these collections were chosen

=> HashMap
- Stores exams (Map<String, Exam>) and students (Map<String, Student>).
- Provides fast lookup by unique name, with expected O(1) access.
- Suitable because lookups occur frequently between other commands.

=> ArrayList
- Stores the questions of an exam.
- Allows fast iteration and efficient sorting.
- Fits a dynamic question count and the main operations of adding and sorting questions.

=> TreeMap
- Stores a student's scores in chronological order for an exam (TreeMap<LocalDateTime, Double>).
- Keeps timestamps ordered and supports finding the score at a given time with floorEntry.
- Provides O(log n) insertion and lookup for this use case.