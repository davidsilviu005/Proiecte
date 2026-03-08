import org.example.Main;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class TestMain {
    String antetResources = "src/main/resources/";

    public boolean areFilesEqual(Path file1, Path file2) throws IOException {
        List<String> lines1 = Files.readAllLines(file1);
        List<String> lines2 = Files.readAllLines(file2);

        if (lines1.size() != lines2.size()) {
            return false;
        }

        for (int i = 0; i < lines1.size(); i++) {
            String line1 = lines1.get(i).trim();
            String line2 = lines2.get(i).trim();

            if (!line1.equals(line2)) {
                return false;
            }
        }

        return true;
    }

    public void emptyOutput(String test_name) {
        File[] files = new File(antetResources + test_name).listFiles();
        for (File file : files) {
            if (file.isFile() && file.getName().endsWith(".out")) {
                file.delete();
            }
        }
    }

    @Test
    public void minimalExamQuestionPrint01() throws IOException {
        String file = "01-minimal-exam-question-print";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "print_exam_JavaBasics_01-01-2025-09-10"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void onlyHistorySorting02() throws IOException {
        String file = "02-only-history-sorting";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "questions_history_POOTest_01-01-2025-09-25"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void onlyPrintExamSorting03() throws IOException {
        String file = "03-only-print-exam-sorting";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "print_exam_SortingExam_01-01-2025-08-20"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void simpleSubmission04() throws IOException {
        String file = "04-simple-submissions";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "console",
                "exam_report_Basics_01-01-2025-11-00",
                "print_exam_Basics_01-01-2025-10-25"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void simpleException05() throws IOException {
        String file = "05-simple-exception";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "console",
                "print_exam_ErrorExam_01-01-2025-08-25"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void multipleCallsAddPrint06() throws IOException {
        String file = "06-multiple-calls-add-print";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "print_exam_MixExam_01-01-2025-08-12",
                "print_exam_MixExam_01-01-2025-08-40",
                "questions_history_MixExam_01-01-2025-08-22"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void largeTestSingleExam07() throws IOException {
        String file = "07-large-test-single-exam";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "console",
                "exam_report_FullExam_03-01-2025-09-55",
                "print_exam_FullExam_01-01-2025-07-11",
                "print_exam_FullExam_01-01-2025-07-22",
                "questions_history_FullExam_01-01-2025-07-10",
                "questions_history_FullExam_01-01-2025-07-21"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void largeTestManyExamStudents08() throws IOException {
        String file = "08-large-test-many-exam-students";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "console",
                "exam_report_JavaExam_03-01-2025-09-25",
                "exam_report_OOPExam_04-01-2025-10-30",
                "print_exam_JavaExam_01-01-2025-07-32",
                "print_exam_JavaExam_01-01-2025-07-50",
                "print_exam_OOPExam_01-01-2025-07-33",
                "print_exam_OOPExam_01-01-2025-07-51",
                "questions_history_JavaExam_01-01-2025-07-30",
                "questions_history_JavaExam_01-01-2025-07-45",
                "questions_history_OOPExam_01-01-2025-07-31",
                "questions_history_OOPExam_01-01-2025-07-46"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void largeTestManyExamStudents09() throws IOException {
        String file = "09-large-test-many-exam-students";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "exam_report_Mixed_07-02-2025-09-20",
                "exam_report_Practice_06-02-2025-09-20",
                "exam_report_Theory_05-02-2025-09-20",
                "print_exam_Mixed_01-02-2025-09-12",
                "print_exam_Practice_01-02-2025-09-11",
                "print_exam_Theory_01-02-2025-09-10"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void largeTestManyExamStudents10() throws IOException {
        String file = "10-large-test-many-exam-students";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "console",
                "exam_report_Prog1_03-03-2025-10-25",
                "exam_report_Prog2_04-03-2025-10-25",
                "print_exam_Prog1_01-03-2025-09-10",
                "print_exam_Prog2_01-03-2025-09-11"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void twoReportsSameExam11() throws IOException {
        String file = "11-two-reports-same-exam";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "exam_report_RepoExam_03-01-2025-09-10",
                "exam_report_RepoExam_03-01-2025-10-00",
                "print_exam_RepoExam_01-01-2025-09-10"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }

    @Test
    public void mixedCommands() throws IOException {
        String file = "12-mixed-commands";
        emptyOutput(file);
        Main.main(new String[]{file});
        String[] test_file_names = {
                "console",
                "exam_report_AlphaExam_03-01-2025-09-20",
                "exam_report_AlphaExam_03-01-2025-10-00",
                "exam_report_BetaExam_04-01-2025-10-20",
                "exam_report_BetaExam_04-01-2025-11-00",
                "print_exam_AlphaExam_01-01-2025-07-10",
                "print_exam_AlphaExam_01-01-2025-07-48",
                "print_exam_AlphaExam_01-01-2025-08-15",
                "print_exam_BetaExam_01-01-2025-07-22",
                "print_exam_BetaExam_01-01-2025-07-49",
                "print_exam_BetaExam_01-01-2025-08-16",
                "print_exam_BetaExam_04-01-2025-10-40",
                "questions_history_AlphaExam_01-01-2025-07-13",
                "questions_history_AlphaExam_01-01-2025-07-45",
                "questions_history_AlphaExam_01-01-2025-08-12",
                "questions_history_BetaExam_01-01-2025-07-46"
        };
        for (String test_file_name : test_file_names) {
            Path out = Paths.get(antetResources + file + "/" + test_file_name + ".out");
            Path ref = Paths.get(antetResources + file + "/" + test_file_name + ".ref");
            assertTrue(areFilesEqual(out, ref));
        }
    }
}