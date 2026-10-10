#lang racket
(require racket/match)
(require "queue.rkt")

(provide (all-defined-out))

(define ITEMS 5)

;; ATENȚIE: Este necesar să implementați întâi
;;          TDA-ul queue în fișierul queue.rkt.
;; Reveniți la acest fișier după ce ați implementat tipul
;; queue și ați verificat implementarea folosind checker-ul.


; Structura counter nu se modifică.
; Se modifică însă implementarea câmpului queue:
; - în loc de listă, acesta va fi o structură de tip queue
; - modificarea nu este vizibilă în definiția structurii,
;   ci în implementarea operațiilor tipului counter
(define-struct counter (index tt et queue) #:transparent)


; TODO 6 (20p)
; Actualizați funcțiile de mai jos conform cu
; noua reprezentare a cozii de persoane.
; Elementele cozii rămân perechi (nume . nr_produse).
; RESTRICȚII (5p per abatere)
;  - Respectați "bariera de abstractizare", adică
;    operați cu coada folosind exclusiv interfața:
;    - empty-queue
;    - queue-empty?
;    - enqueue
;    - dequeue
;    - top
; Obs: Doar câteva funcții necesită actualizări.
(define (empty-counter index)           ; testată de checker
  (counter index 0 0 empty-queue))

;pt a adauga intarziere unei case, etc
(define (update f counters index)
  (map (lambda (c)
         (if (= (counter-index c) index)
             (f c)
             c))
       counters))

(define (tt+ minutes)
  (lambda(c)
    (struct-copy counter c
                 [tt (+ (counter-tt c) minutes)])))

(define (et+ minutes)
  (lambda (c)
    (struct-copy counter c
                 [et (+ (counter-et c) minutes)])))

;face o noua coada
(define ((add-to-counter name items) C) ; testată de checker
  (let ([new-q (enqueue (cons name items) (counter-queue C))]
        [new-tt (+ (counter-tt C) items)])
    ;verifica daca casa e goala, ori clientul devine primul si et devine tot new-tt
    ;fie et nu se schimba ca primul client e acelasi
    (if (queue-empty? (counter-queue C))
        (struct-copy counter C
                     [tt new-tt]
                     [et new-tt]
                     [queue new-q])
        (struct-copy counter C
                     [tt new-tt]
                     [queue new-q]))))

;alege cea mai buna casa dupa criteriul f
(define (best-counter f counters)
  (let ([first-counter (car counters)])
    (foldl (lambda (c best)
             ;daca valoarea (f c) e mai mica decat la best, alege c
             (if (or (< (f c) (f best))
                     ;daca sunt egale o ia pe aia cu indexul mai mic
                     (and (= (f c) (f best))
                          (< (counter-index c) (counter-index best))))
                 c
                 best))
           first-counter
           (cdr counters))))

;gaseste casa cu tt minim( intoarce indexul si tt-ul)
(define (min-tt counters)
  (let ([best (best-counter counter-tt counters)])
    (cons (counter-index best) (counter-tt best))))

;gaseste casa cu tt minim( intoarce indexul si et-ul)
(define (min-et counters)
  (let ([best (best-counter counter-et counters)])
    (cons (counter-index best) (counter-et best))))

;stergea primului client din coada
(define (remove-first-from-counter C)   ; testată de checker
  ;facem dequeue pe coada
  (let* ([new-queue (dequeue (counter-queue C))]
         ;scadem din tt timpul primului client, care e et
         [new-tt (- (counter-tt C) (counter-et C))]
         ;calc noul et, daca e cineva la coada
         [new-et (if (queue-empty? new-queue)
                     0
                     (cdr (top new-queue)))])
    (struct-copy counter C
                 [tt new-tt]
                 [et new-et]
                 [queue new-queue])))


; TODO 7 (10p)
; Implementați o funcție care calculează starea
; unei case după un număr dat de minute.
; Funcția presupune, fără să verifice, că în acest timp
; nu iese nimeni din coadă, deci se modifică
; doar câmpurile tt și et.
; Este responsabilitatea utilizatorului să nu apeleze
; funcția cu minutes > et și coadă nevidă.
; La casele fără clienți, este responsabilitatea
; voastră să nu produceți timpi negativi.
;simuleaza trecerea a 'minutes' pentru o casa
(define ((pass-time-through-counter minutes) C)
  (struct-copy counter C
               ;scade din tt si et si ne asiguram ca nu devine negativ
               [tt (max 0 (- (counter-tt C) minutes))]
               [et (max 0 (- (counter-et C) minutes))]))


; TODO 8 (60p)
; Implementați funcția care simulează fluxul clienților pe la case.
; ATENȚIE: Față de etapa 2, apar modificări în:
; - formatul listei de cereri (requests)
; - formatul rezultatului funcției (explicat mai jos)
; requests conține 4 tipuri de cereri:
;   3 moștenite din etapa 2:
;   - (<name> <n-items>) - așază persoana <name> la coadă la o casă
;   - (delay <index> <minutes>) - întârzie casa <index> cu <minutes> minute
;   - (ensure <average>) - cât timp tt-ul mediu al tuturor caselor depășește
;                          <average>, adaugă case fără restricții (case slow)
;   plus noutatea:
;   - <x> - actualizează starea caselor conform cu trecerea a <x> minute
;           de la ultima cerere (afectează câmpurile tt, et, queue)
; Obs: Cererile (remove-first) din etapa 2 sunt înlocuite de un mecanism
; mai sofisticat de a scoate clienții din coadă (pe măsură ce trece timpul).
; Sistemul procesează cererile în ordine, astfel:
; - nicio modificare pentru cererile moștenite din etapa 2
; - când timpul prin sistem avansează cu <x> minute, starea caselor
;   se actualizează pentru a reflecta trecerea timpului;
;   ieșirile clienților din coadă se rețin în ordine cronologică.
; Funcția serve întoarce o pereche cu punct între:
; - lista clienților care au părăsit magazinul, sortată cronologic
;   - elementele listei au forma (index_casă . nume)
;   - când mai mulți clienți ies simultan, sortați după indexul casei
; - lista caselor în starea finală (ca rezultatul din etapele 1 și 2)
; Sugestii:
; - gestionați cronologia folosind în mod repetat funcția min-et
; - pentru a menține lista clienților plecați, definiți o funcție ajutătoare
; (cu un parametru în plus față de serve), pe care serve doar o apelează.
; RESTRICȚII (5p per abatere)
;  - Folosiți minim un let și un let* (care nu ar putea fi let). (2*5p)
;  - Respectați "bariera de abstractizare" oricând operați cu tipul queue.

;calc media valorilor pt o lista de case
;pt cererea (ensure average) sa verific daca media depaseste limita
(define (average-tt counters)
  (/ (apply + (map counter-tt counters))
     (length counters)))

;adauga case slow noi pana media tt devine  <= average
(define (ensure-counters average fast slow)
  ;incepem cu lista de case slow
  (let loop ([slow-list slow]
             ;next-index este indexul pt casa noua
             [next-index (+ 1 (apply max (map counter-index (append fast slow))))])
    ;verificam media pe toate casele, daca e buna, ne oprim
    (if (<= (average-tt (append fast slow-list)) average)
        slow-list
        ;altfel adaug o casa noua goala, index++, loop
        (loop (append slow-list (list (empty-counter next-index)))
              (+ next-index 1)))))

;selecteaza casele unde clientul poate merge
(define (valid-counters items fast slow)
  ;poate merge oriunde
  (if (<= items ITEMS)
      (append fast slow)
      ;merge doar la slow
      slow))

;pastreaza doar casele unde au clienti
;casele fara clienti nu conteaza cand cauti cine termina primul
(define (non-empty-counters counters)
  (filter (lambda (c)
            (not (queue-empty? (counter-queue c))))
          counters))

;gaseste casele la care primul client a terminat exact acum
(define (finished-counters counters)
  (filter (lambda (c)
            ;sa nu aibe coada goala
            (and (not (queue-empty? (counter-queue c)))
                 ;sa aibe et = 0
                 (= (counter-et c) 0)))
          counters))

;simuleaza trecerea a minutes pt toate casele si actualizeaza
;timpii
;cozile
;lista clientilor care au plecat
(define (pass-time minutes counters left-store)
  (let ([active (non-empty-counters counters)])
    (cond
      ;nu mai am case active sau minute de procesat
      [(or (= minutes 0) (null? active))
       ;intorc starea actuala
       (cons left-store
             ;scade eventual minutele ramase din toate casele
             (map (pass-time-through-counter minutes) counters))]
      [else
       ;sare direct la urmatorul eveniment relevant
       ;fie expira toate minutele cerute, fie ajunge la
       ;momentul cand primul client de la o casa pleaca
       ;(min-et active) imi da cel mai mic timp pana la urm client gata
       (let* ([step (min minutes (cdr (min-et active)))]
              ;toate casele sunt avansate cu step
              [new-counters (map (pass-time-through-counter step) counters)]
              ;vad la ce case primul client are et = 0
              [done (finished-counters new-counters)])
         (if (null? done)
             ;daca nu a terminat nimeni doar intorc starea
             (cons left-store new-counters)
             (pass-time
              (- minutes step)
              ;scoate primii clienti din casele terminate
              ;pt fiecare casa din done scoate primul client
              (foldl (lambda (c acc)
                       (update remove-first-from-counter
                               acc
                               (counter-index c)))
                     new-counters
                     done)
              ;adauga clienti in left-store
              ;ia indexul casei, numele clientului din fata
              ;construieste perechea index nume
              (append left-store
                      (map (lambda (c)
                             (cons (counter-index c)
                                   (car (top (counter-queue c)))))
                           done)))))])))


;proceseaza recursiv toate cererile
(define (serve-helper requests fast slow left-store)
  (if (null? requests)
      ;lista clientilor iesiti + starea finala a caselor
      (cons left-store (append fast slow))
      (match (car requests)
        [(list 'delay index minutes)
         ;mareste tt si et pt casa data
         (let ([all-counters
                (update (lambda (c)
                          ((et+ minutes) ((tt+ minutes) c)))
                        (append fast slow)
                        index)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         left-store))]
        [(list 'ensure average)
         ;adauga case slow pana cand media devine suficient de mica
         (serve-helper (cdr requests)
                       fast
                       (ensure-counters average fast slow)
                       left-store)]
        [(list name items)
         ;client nou: alegem casa valida cu tt minim
         (let* ([index (car (min-tt (valid-counters items fast slow)))]
                [all-counters
                 (update (add-to-counter name items)
                         (append fast slow)
                         index)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         left-store))]
        [minutes
         ;cererea este un numar, deci trece timpul
         (let* ([result (pass-time minutes (append fast slow) left-store)]
                [new-left-store (car result)]
                [all-counters (cdr result)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         new-left-store))])))

;functia finala ceruta de tema
(define (serve requests fast-counters slow-counters)
  (serve-helper requests fast-counters slow-counters '()))
