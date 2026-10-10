#lang racket
(require racket/match)

(provide (all-defined-out))

(define ITEMS 5)

;; Actualizăm structura counter cu informația et:
;; Exit time (et) al unei case reprezintă timpul
;; până la ieșirea primului client de la casa respectivă,
;; adică numărul de produse de procesat pentru acest client
;; + întârzierile suferite de casă (dacă există).
;; Ex:
;; la C3 s-au așezat Ana cu 3 produse, apoi Geo cu 7 produse,
;; și C3 a fost întârziată cu 5 minute =>
;; et pentru C3 este 3 + 5 = 8 (timpul până când va ieși Ana).


; Redefinim structura counter.
; Acum fiecare casă ține minte și et, adică timpul până pleacă primul client.
(define-struct counter (index tt et queue) #:transparent)


; TODO 1 (5p)
; Actualizați implementarea empty-counter astfel încât să conțină și câmpul et.
; Creează o casă goală: fără timp total, fără timp de ieșire și fără clienți.
(define (empty-counter index)
  (make-counter index 0 0 '()))


; TODO 2 (15p)
; Implementați o funcție care aplică o transformare f
; casei cu un anumit index.
; f = funcție unară cu un parametru de tip casă,
; counters = listă de case,
; index = indexul casei care trebuie transformată
; Veți întoarce lista actualizată de case.
; Dacă nu există în counters o casă cu acest index,
; întoarceți lista nemodificată.
; Aplică transformarea f doar casei cu indexul cerut.
; Restul caselor rămân identice.
(define (update f counters index)
  (if (null? counters)
      '()
      (if (= (counter-index (car counters)) index)
          (cons (f (car counters)) (cdr counters))
          (cons (car counters) (update f (cdr counters) index))))
  )


; TODO 3 (7.5p)
; Memento: tt+ crește tt-ul unei case cu un număr de minute.
; Obs: tt+ afectează doar câmpul tt, nu și câmpul et.
; Actualizați implementarea tt+ pentru:
; - a ține cont de noua reprezentare a unei case
; - a permite ca operații de tip tt+ să fie pasate ca argument
;   funcției update în cel mai facil mod
; Obs: Facil înseamnă că o aplicație parțială a funcției tt+
; va produce o funcție unară cu parametru de tip casă, fără
; să fie nevoie de funcții anonime sau funcții auxiliare.
; Scheletul nu menționează parametrii funcției tt+, întrucât
; trebuie să determinați voi înșivă cum este cel mai bine
; ca tt+ să își primească parametrii.
;
; Apoi implementați funcția checker-tt+, care apelează funcția
; tt+ pe o casă și un număr de minute.
; Funcția checker-tt își precizează clar parametrii și
; poate fi testată, acesta este singurul său rol.
; RESTRICȚII (5p)
;  - Implementați tt+ conform cerinței anterioare.
; Întoarce o funcție care, aplicată pe o casă, îi mărește doar câmpul tt.
(define tt+
  (lambda (minutes)
    (lambda (c)
      (make-counter
       (counter-index c)
       (+ (counter-tt c) minutes)
       (counter-et c)
       (counter-queue c))))
  )

; Funcție de test: aplică tt+ pe o casă concretă.
(define (checker-tt+ C minutes)
  ((tt+ minutes) C))


; TODO 4 (7.5p)
; Implementați o funcție care crește et-ul unei case
; cu un număr dat de minute.
; Obs: et+ afectează doar câmpul et, nu și câmpul tt.
; Păstrați formatul folosit pentru tt+.
; Apoi implementați funcția checker-et+ care apelează
; et+, pentru testare.
; RESTRICȚII (5p)
;  - Implementați et+ conform cerinței anterioare.
; Întoarce o funcție care mărește doar et-ul casei.
(define et+
  (lambda (minutes)
    (lambda (c)
      (make-counter
       (counter-index c)
       (counter-tt c)
       (+ (counter-et c) minutes)
       (counter-queue c))))
   )

; Funcție de test pentru et+.
(define (checker-et+ C minutes)
  ((et+ minutes) C))


; TODO 5 (10p)
; Memento: add-to-counter adaugă o persoană
; (reprezentată prin nume și număr de produse) la o casă.
; Actualizați implementarea add-to-counter din aceleași
; rațiuni pentru care ați actualizat funcția tt+.
; Atenție la cum se modifică tt și et!
; Apoi implementați funcția checker-add-to-counter
; care apelează add-to-counter, pentru testare.
; RESTRICȚII (5p)
;  - Implementați add-to-counter conform cerinței anterioare.
; Întoarce o funcție care adaugă un client la finalul cozii.
; tt crește mereu, iar et crește doar dacă înainte coada era goală.
(define add-to-counter
  (lambda (name n-items)
    (lambda (c)
      (make-counter
       (counter-index c)
       (+ (counter-tt c) n-items)
       (if (null? (counter-queue c))
           (+ (counter-et c) n-items)
           (counter-et c))
       (append (counter-queue c) (list (cons name n-items))))))
    )

; Funcție de test pentru add-to-counter.
(define (checker-add-to-counter C name n-items)
  ((add-to-counter name n-items) C))


; TODO 6 (15p)
; Întrucât vom folosi atât min-tt (implementat în etapa 1)
; cât și min-et (funcție nouă), definiți o funcție mai abstractă
; din care să derive ușor atât min-tt cât și min-et.
; Prin analogie cu min-tt, definim min-et astfel:
; min-et = funcție care primește o listă nevidă de case și
; întoarce o pereche dintre:
; - indexul casei (din listă) care are cel mai mic et
; - et-ul acesteia
; (la același et, este preferată casa cu indexul cel mai mic)
; Obs: în etapele 2-4, listele de case sunt sortate după index.
; RESTRICȚII (10p - 2*5p)
;  - min-tt și min-et vor fi aplicații parțiale ale funcției abstracte.
; Helper generic pentru a găsi casa minimă după criteriul f.
; Păstrează și regula de departajare după index mai mic.
(define (min-by-helper f counters best)
  (if (null? counters)
      (cons (counter-index best) (f best))
      (if (or (< (f (car counters)) (f best))
              (and (= (f (car counters)) (f best))
                   (< (counter-index (car counters))
                      (counter-index best))))
          (min-by-helper f (cdr counters) (car counters))
          (min-by-helper f (cdr counters) best))))

; Pornește căutarea minimului de la prima casă din listă.
(define (min-by f counters)
  (min-by-helper f (cdr counters) (car counters)))

; Aplicație parțială a lui min-by folosind criteriul counter-tt.
(define min-tt
  (lambda (counters)
    (min-by counter-tt counters))) ; folosind funcția de mai sus

; Aplicație parțială a lui min-by folosind criteriul counter-et.
(define min-et
  (lambda (counters)
    (min-by counter-et counters))) ; folosind funcția de mai sus


; TODO 7 (10p)
; Implementați o funcție care scoate prima persoană
; din coada unei case.
; Funcția presupune, fără să verifice, că există
; minim o persoană la coada casei C.
; Veți întoarce o nouă structură obținută prin
; modificarea cozii de așteptare.
; Atenție la cum se modifică tt și et!
; Dacă o casă tocmai a fost părăsită de cineva,
; înseamnă că ea nu mai are întârzieri.
; Elimină primul client din coadă și recalculează tt și et pentru noua stare.
; Dacă nu mai rămâne nimeni, ambele devin 0.
(define (remove-first-from-counter C)
  (make-counter
   (counter-index C)
   (if (null? (cdr (counter-queue C)))
       0
       (apply + (map cdr (cdr (counter-queue C)))))
   (if (null? (cdr (counter-queue C)))
       0
       (cdr (car (cdr (counter-queue C)))))
   (cdr (counter-queue C)))
   )


; TODO 8 (50p)
; Implementați funcția care simulează fluxul clienților pe la case.
; ATENȚIE: Față de etapa 1, funcția operează cu următoarele modificări:
; - nu mai avem doar 4 case, ci:
;   - fast-counters (o listă de case pentru maxim ITEMS produse)
;   - slow-counters (o listă de case fără restricții)
;   (Sugestie: folosiți funcția update pentru a procesa liste de case)
; - requests conține 4 tipuri de cereri (două în plus față de etapa 1):
;   - (<name> <n-items>) - așază persoana <name> la coadă la o casă
;   - (delay <index> <minutes>) - întârzie casa <index> cu <minutes> minute
;   - (remove-first) - cea mai avansată persoană părăsește casa la care este
;   - (ensure <average>) - cât timp tt-ul mediu al tuturor caselor depășește
;                          <average>, adaugă case fără restricții (case slow)
; Sistemul procesează cererile în ordine, astfel:
; - așază persoana la casa cu tt minim la care are voie
;   (ca înainte, dar folosind fast-counters și slow-counters)
; - când o casă suferă o întârziere, tt-ul și et-ul ei cresc
;   (chiar dacă nu are clienți)
; - persoana cea mai avansată este prima persoană la casa cu et-ul minim
;   (dintre casele care au clienți)
;   (dacă nicio casă nu are clienți, ignoră cererea)
; - dacă tt-ul mediu pentru toate casele > <average>,
;   adaugă case slow până când media <= <average>
;   (puteți determina matematic de câte case noi este nevoie sau
;   să adăugați recursiv una câte una cât timp este necesar)
; Considerați casele indexate de la 1 și mereu sortate după index.
; Ex:
; fast-counters conține casele 1-2, slow-counters conține casele 3-15
; => la nevoie adăugați întâi casa 16, apoi casa 17, etc.
; RESTRICȚII (25p - 5*5p)
;  - Folosiți minim două funcționale predefinite în Racket. (2*5p)
;  - Nu apelați checker-tt+, checker-et+, checker-add-to-counter,
;    ci doar tt+, et+, add-to-counter. (3*5p)

; Unește cele două liste de case într-una singură.
(define (all-counters fast-counters slow-counters)
  (append fast-counters slow-counters))

; Păstrează doar casele care au cel puțin un client la coadă.
(define (non-empty-counters fast-counters slow-counters)
  (filter (lambda (c) (not (null? (counter-queue c))))
          (all-counters fast-counters slow-counters)))

; Calculează media timpilor tt pentru toate casele existente.
(define (average-tt fast-counters slow-counters)
  (if (null? (all-counters fast-counters slow-counters))
      0
      (/ (apply + (map counter-tt (all-counters fast-counters slow-counters)))
         (length (all-counters fast-counters slow-counters)))))

; Dă indexul pe care îl va avea următoarea casă slow adăugată.
(define (next-counter-index fast-counters slow-counters)
  (+ 1 (length (all-counters fast-counters slow-counters))))

; Aplică delay-ul casei cerute: cresc atât tt, cât și et.
; Întoarce noile liste fast și slow.
(define (handle-delay index minutes fast-counters slow-counters)
  (list
   (update (et+ minutes)
           (update (tt+ minutes) fast-counters index)
           index)
   (update (et+ minutes)
           (update (tt+ minutes) slow-counters index)
           index)))

; Așază clientul la casa permisă cu tt minim.
; Pentru <= ITEMS poate merge și la fast, altfel doar la slow.
(define (handle-add name n-items fast-counters slow-counters)
  (if (<= n-items ITEMS)
      (list
       (update (add-to-counter name n-items)
               fast-counters
               (car (min-tt (all-counters fast-counters slow-counters))))
       (update (add-to-counter name n-items)
               slow-counters
               (car (min-tt (all-counters fast-counters slow-counters)))))
      (list
       fast-counters
       (update (add-to-counter name n-items)
               slow-counters
               (car (min-tt slow-counters))))))

; Scoate primul client de la casa cu et minim dintre casele nevidе.
; Dacă nu există clienți, lasă starea neschimbată.
(define (handle-remove-first fast-counters slow-counters)
  (if (null? (non-empty-counters fast-counters slow-counters))
      (list fast-counters slow-counters)
      (list
       (update remove-first-from-counter
               fast-counters
               (car (min-et (non-empty-counters fast-counters slow-counters))))
       (update remove-first-from-counter
               slow-counters
               (car (min-et (non-empty-counters fast-counters slow-counters)))))))

; Adaugă recursiv case slow până când media tt ajunge sub pragul cerut.
(define (handle-ensure average fast-counters slow-counters)
  (if (<= (average-tt fast-counters slow-counters) average)
      (list fast-counters slow-counters)
      (handle-ensure average
                     fast-counters
                     (append slow-counters
                             (list (empty-counter
                                    (next-counter-index fast-counters slow-counters)))))))

; Procesează toate cererile și întoarce lista finală de case.
; Pentru fiecare request apelează helper-ul potrivit și continuă recursiv.
(define (serve requests fast-counters slow-counters)
  (if (null? requests)
      (append fast-counters slow-counters)
      (match (car requests)
        [(list 'delay index minutes)
         (serve (cdr requests)
                (car (handle-delay index minutes fast-counters slow-counters))
                (cadr (handle-delay index minutes fast-counters slow-counters)))]
        [(list 'remove-first)
         (serve (cdr requests)
                (car (handle-remove-first fast-counters slow-counters))
                (cadr (handle-remove-first fast-counters slow-counters)))]
        [(list 'ensure average)
         (serve (cdr requests)
                (car (handle-ensure average fast-counters slow-counters))
                (cadr (handle-ensure average fast-counters slow-counters)))]
        [(list name n-items)
         (serve (cdr requests)
                (car (handle-add name n-items fast-counters slow-counters))
                (cadr (handle-add name n-items fast-counters slow-counters)))]

  )))
