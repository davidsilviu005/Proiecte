->Sistemul gestioneaza:
  - servere (cu status, locatie si owner)
  - grupuri de resurse asociate unui server (identificate prin IP)
  - membri in grupuri
  - alerte asociate unui server (tip, severitate, mesaj)

->Clase principale
  - Main – alege fluxul in functie de PathTypes si ruleaza procesul potrivit
  - CommandFileReader – citeste din fisier si parseaza header + linii, produce o lista de CommandRow
  - CommandRow – un rand de comanda: command, params (map cheie-valoare)
  - Database – stocare in memorie pentru servere, grupuri si alerte
  - ServerCommandProcessor – executa comenzi pentru servere
  - GroupCommandProcessor – executa comenzi pentru grupuri si membri
  - EventCommandProcessor – executa comenzi pentru evenimente/alerte

Colectii folosite
  - Map pentru acces rapid dupa IP (servere si grupuri)
  - Set pentru alerte (colectie de alerte)
  - List pentru lista de observatori (listeneri) in Observer pattern

Design pattern-uri implementate:
1) Singleton
  - Database are o singura instanta in toata aplicatia (accesata prin getInstance())

2) Factory
  - UserFactory creeaza tipul corect de user (User / Admin / Operator) pe baza campurilor disponibile din input

3) Builder
  - Server.Builder permite construirea unui server cu campuri optionale fara constructori lungi

4) Observer
  - Server este subject si notifica listenerii (AlertListener)
  - ResourceGroup este observer (listener) si primeste alerta prin onAlert()