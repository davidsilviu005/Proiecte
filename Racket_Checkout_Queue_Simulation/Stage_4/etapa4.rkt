#lang racket
(require racket/match)
(require "queue.rkt")

(provide (all-defined-out))

(define ITEMS 5)

(define-struct counter (index tt et queue open) #:transparent)


; TODO (0p)
; Aveți libertatea să vă structurați programul cum doriți
; (dar cu restricțiile de mai jos), astfel încât
; funcția serve să funcționeze conform specificației.
;
; Restricții (impuse de checker):
; - va exista în continuare funcția (empty-counter index)
; - veți reprezenta cozile folosind noul TDA queue
(define (empty-counter index)
  (counter index 0 0 empty-queue #t))


; TODO 7 (70p)
; Implementați funcția care simulează fluxul clienților pe la case.
; ATENȚIE: Față de etapa 3, apar modificări în:
; - formatul listei de cereri (requests)
; - formatul rezultatului funcției (explicat mai jos)
; requests conține 6 tipuri de cereri:
;   4 moștenite din etapa 3:
;   - (<name> <n-items>) - așază persoana <name> la coadă la o casă deschisă
;   - (delay <index> <minutes>) - întârzie casa <index> cu <minutes> minute
;   - (ensure <average>) - cât timp tt-ul mediu al caselor deschise depășește
;                          <average>, adaugă case fără restricții (case slow)
;   - <x> - actualizează starea caselor conform cu trecerea a <x> minute
;           de la ultima cerere (afectează câmpurile tt, et, queue)
;   plus 2 noi:
;   - (close <index>) - închide casa cu indexul <index> (casa există deja)
;   - (open <index>) - deschide casa cu indexul <index> (casa există deja)
; Sistemul procesează cererile în ordine, astfel:
; - așază persoana la casa DESCHISĂ cu tt minim la care are voie;
;   se garantează că persoana poate fi distribuită la o casă
; - nicio modificare pentru situația când o casă suferă o întârziere
; - dacă tt-ul mediu pentru toate casele DESCHISE > <average>,
;   adaugă case slow până când media <= <average>
; - nicio modificare în modelarea trecerii timpului
; - o casă care se închide nu mai primește clienți noi și:
;   - primul client (dacă există) își continuă treaba la această casă
;   - restul clienților se redistribuie la celelalte case,
;     în ordinea în care erau așezați la coadă
; - o casă care se deschide redevine disponibilă pentru clienți
; Funcția serve întoarce o pereche cu punct între:
; - lista clienților care au părăsit magazinul, sortată cronologic
;   - elementele listei au forma (index_casă . nume)
;   - când mai mulți clienți ies simultan, sortați după indexul casei
; - lista cozilor nevide în starea finală, sortată după indexul casei
;   - elementele listei au forma (index_casă . coadă) (coada este de tip queue)


;pt a adauga intarziere, a inchide/deschide o casa, etc
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

;simuleaza trecerea a 'minutes' pentru o casa
(define ((pass-time-through-counter minutes) C)
  (struct-copy counter C
               ;scade din tt si et si ne asiguram ca nu devine negativ
               [tt (max 0 (- (counter-tt C) minutes))]
               [et (max 0 (- (counter-et C) minutes))]))

;calc media valorilor pt o lista de case
;pt cererea (ensure average) sa verific daca media depaseste limita
(define (average-tt counters)
  (/ (apply + (map counter-tt counters))
     (length counters)))

;pastreaza doar casele deschise
(define (open-counters counters)
  (filter counter-open counters))

;adauga case slow noi pana media tt devine  <= average
(define (ensure-counters average fast slow)
  ;incepem cu lista de case slow
  (let loop ([slow-list slow]
             ;next-index este indexul pt casa noua
             [next-index (+ 1 (apply max (map counter-index (append fast slow))))])
    ;verificam media pe toate casele deschise, daca e buna, ne oprim
    (if (<= (average-tt (open-counters (append fast slow-list))) average)
        slow-list
        ;altfel adaug o casa noua goala, index++, loop
        (loop (append slow-list (list (empty-counter next-index)))
              (+ next-index 1)))))

;selecteaza casele unde clientul poate merge
(define (valid-counters items fast slow)
  (filter counter-open
          ;poate merge oriunde
          (if (<= items ITEMS)
              (append fast slow)
              ;merge doar la slow
              slow)))

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
             ;daca au terminat clientii
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

;doar inchide casa
(define (close-counter C)
  (struct-copy counter C [open #f]))

;doar deschide casa
(define (open-counter C)
  (struct-copy counter C [open #t]))

;Transforma coada intr-o lista normala
;pt a separa la close primul client de restul
(define (queue->list q)
  (if (queue-empty? q)
      '()
      (cons (top q)
            (queue->list (dequeue q)))))

;adauga mai multi clienti la casele potrivite
;luam nume si nr de produse
;alege casa cu tt minim
;adauga clientul acolo
;face asta pt toti
;o fol pt close cand restul clientilor tb redistribuiti in
;ordine in care era in coada
(define (add-clients clients fast slow)
  (if (null? clients)
      (append fast slow)
      (let* ([client (car clients)]
             [name (car client)]
             [items (cdr client)]
             [index (car (min-tt (valid-counters items fast slow)))]
             [all-counters (update (add-to-counter name items)
                                   (append fast slow)
                                   index)])
        (add-clients (cdr clients)
                     (take all-counters (length fast))
                     (drop all-counters (length fast))))))

;proceseaza recursiv toate cererile
;requests-cereri ramase; fast-lista de case fast
;slow-lista de case slow; left-store-lista clientilor care au plecat
(define (serve-helper requests fast slow left-store)
  ;daca nu mai sunt cereri intoarce lista clientilor iesiti
  ;si starea finala a caselor
  (if (null? requests)
      (cons left-store (append fast slow))
      ;un fel de switch
      (match (car requests)
        ;intarzie casa cu index cu minutes
        [(list 'delay index minutes)
         (let ([all-counters
                (update (lambda (c)
                          ;aplic tt+ minutes si et+ minutes
                          ((et+ minutes) ((tt+ minutes) c)))
                        (append fast slow)
                        index)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         left-store))]
        ;verifica media tt pe casele deschise si adauga case slow cu ensure-counters
        ;pana media devine suficienta
        [(list 'ensure average)
         (serve-helper (cdr requests)
                       fast
                       (ensure-counters average fast slow)
                       left-store)]
        ;inchide casa si redistribuie clientii din spatele primului
        [(list 'close index)
         (let* ([all (append fast slow)]
                ;gaseste casa cautata
                [target (findf (lambda (c) (= (counter-index c) index)) all)]
                ;transform coada in lista
                [q-list (queue->list (counter-queue target))]
                ;separ restul clientilor si verific daca e cineva
                [rest-clients (if (null? q-list) '() (cdr q-list))]
                ;construiesc o casa noua inchisa
                [closed-counter
                 (cond
                   ;daca nu are clienti, doar o inchide
                   [(null? q-list)
                    (close-counter target)]
                   [else
                    ;inchide casa, reconstruieste coada doar cu
                    ;primul client si tt=et
                    (struct-copy counter (close-counter target)
                                 [queue (enqueue (car q-list) empty-queue)]
                                 [tt (counter-et target)])])]
                ;inlocuim casa veche
                [updated-all (update (lambda (_) closed-counter) all index)]
                ;redistribuie restul clientilor
                [redistributed (add-clients rest-clients
                                            (take updated-all (length fast))
                                            (drop updated-all (length fast)))])
           (serve-helper (cdr requests)
                         (take redistributed (length fast))
                         (drop redistributed (length fast))
                         left-store))]
        ;redeschide casa prin open-counter
        [(list 'open index)
         (let ([all-counters
                (update open-counter
                        (append fast slow)
                        index)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         left-store))]
        ;a venit un client nou
        ;calculeaza casele valide, alege casa cu tt minim si pune clientul acolo
        [(list name items)
         (let* ([index (car (min-tt (valid-counters items fast slow)))]
                [all-counters
                 (update (add-to-counter name items)
                         (append fast slow)
                         index)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         left-store))]
        ;cererea nu e o lista ci un nr
        ;trec atatea minute
        ;apeleaza pass-time si continua cu noile case si noul left-store
        [minutes
         (let* ([result (pass-time minutes (append fast slow) left-store)]
                [new-left-store (car result)]
                [all-counters (cdr result)])
           (serve-helper (cdr requests)
                         (take all-counters (length fast))
                         (drop all-counters (length fast))
                         new-left-store))])))

(define (serve requests fast-counters slow-counters)
  ;apeleaza serve-helper si separa lista clientilor iesiti si lista finala de case
  ;pastreaza doar casele care mai au clienti
  ;transforma fiecare casa in index queue
  ;o pereche in care in st sunt clientii care au iesit si in dr cozile nevide ramase
  (let* ([result (serve-helper requests fast-counters slow-counters '())]
         [left-store (car result)]
         [all-counters (cdr result)])
    (cons left-store
          (map (lambda (c)
                 (cons (counter-index c)
                       (counter-queue c)))
               (non-empty-counters all-counters)))))
