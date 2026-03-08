	Bonus – Statistici pentru examene

    => Descriere functionalitate
O functionalitate suplimentara care poate fi adaugata aplicatiei este generarea de statistici pentru un examen, pentru a oferi o imagine de ansamblu asupra performantei studentilor

    => Pentru fiecare examen, platforma poate genera:
- scorul minim
- scorul maxim
- scorul mediu
- numarul total de studenti evaluati

    => Clasa noua -> ExamStatistics
- contine campuri pentru: minScore, maxScore, averageScore, studentCount
- ofera metode de calcul si de afisare a statisticilor

    => Metode noi
- in clasa Exam:
  - ExamStatistics computeStatistics(LocalDateTime timestamp)
- in clasa Platform:
  - generateStatistics(String examName, LocalDateTime timestamp)

Aceasta extensie respecta principiile POO si poate fi integrata usor in arhitectura actuala.
