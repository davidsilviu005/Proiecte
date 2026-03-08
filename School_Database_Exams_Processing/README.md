        Structura aplicatiei
- main => se ocupa exclusiv de citirea si parsarea comenzilor si de apelarea metodelor din Platform
- platform => coordoneaza logica generala a aplicatiei (gestioneaza examenele, studentii si fisierele de output)
- exam => modeleaza un examen, contine intrebarile asociate si istoricul scorurilor studentilor
- question => clasa de baza pentru toate tipurile de intrebari
- openEndedQuestion, fillInTheBlankQuestion, multipleChoiceQuestion => implementeaza verificarea raspunsurilor si calculul punctajului
- student => retine informatii despre student si scorul curent obtinut la examene
- submissionOutsideTimeIntervalException => exceptie aruncata atunci cand un student incearca sa sustina un examen in afara intervalului permis

	Motivatia alegerii colectiilor
  
   =>HashMap
- folosit pentru stocarea examenelor (Map<String, Exam>) si a studentilor (Map<String, Student>)
- motivatie: acces rapid dupa nume (cheie unica), cu complexitate O(1)
- operatiile de cautare sunt frecvente si intercalate cu alte comenzi, deci aceasta structura este optima

   =>ArrayList
- utilizat pentru stocarea intrebarilor unui examen
- motivatie: permite parcurgere rapida si sortari eficiente
- numarul de intrebari este dinamic, iar operatiile principale sunt adaugarea si sortarea

   =>TreeMap
- folosit pentru gestionarea istoricului scorurilor unui student intr-un examen (TreeMap<LocalDateTime, Double>)
- motivatie: mentine scorurile ordonate cronologic si permite obtinerea eficienta a scorului „curent” la un anumit timestamp, folosind floorEntry
- complexitate: O(log n) pentru inserare si interogare, potrivit pentru cerintele aplicatiei

