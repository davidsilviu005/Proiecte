module AlgebraicGraph where

import Data.Set (Set)
import qualified Data.Set as Set
import Data.Foldable

data AlgebraicGraph a
    = Empty
    | Node { label :: a }
    | Overlay { left :: AlgebraicGraph a, right :: AlgebraicGraph a }
    | Connect { left :: AlgebraicGraph a, right :: AlgebraicGraph a }
    deriving (Eq)

-- (1, 2), (1, 3)
-- 1 * (2 + 3)
angle :: AlgebraicGraph Int
angle = Connect (Node 1) (Overlay (Node 2) (Node 3))

-- (1, 2), (1, 3), (2, 3)
-- 1 * (2 * 3)
triangle :: AlgebraicGraph Int
triangle = Connect (Node 1) (Connect (Node 2) (Node 3))

{-
*** TODO 1 (15p) ***

Instanțiați clasa Foldable cu constructorul de tip AlgebraicGraph.
Nodurile trebuie prelucrate în ordinea în care apar în graf.

Odată ce implementați funcția foldr, multe alte funcții predefinite
care se bazează pe ea devin disponibile.

Exemple:

>>> toList triangle
[1,2,3]

>>> length triangle
3

>>> sum triangle
6

>>> maximum triangle
3
-}
instance Foldable AlgebraicGraph where
    foldr :: (a -> b -> b) -> b -> AlgebraicGraph a -> b
    foldr f acc graph = case graph of
        -- Am folosit acumulatorul pentru cazul Empty
        Empty -> acc

        -- Am aplicat functia f pe nod si pe acumulator
        Node node -> f node acc

        -- Am folosit foldr pe dreapta, apoi pe stanga, ca sa pastrez ordinea
        Overlay g1 g2 -> foldr f (foldr f acc g2) g1

        -- Am folosit foldr la fel si pentru Connect, pe cele doua subgrafuri
        Connect g1 g2 -> foldr f (foldr f acc g2) g1

{-
*** TODO 2 (5p) ***

Reimplementați funcția nodes folosind foldr.

CONSTRÂNGERI:

* NU puteți obține în prealabil lista nodurilor (de exemplu, folosind toList).
* Utilizați stilul point-free.
-}
nodesWithFoldr :: Ord a => AlgebraicGraph a -> Set a
nodesWithFoldr = foldr Set.insert Set.empty
-- Am folosit foldr cu Set.insert ca sa bag fiecare nod in Set

{-
*** TODO 3 (20p) ***

Este funcția edges din etapele 2 și 3 compozițională? Cu alte cuvinte:

* Asupra subgrafurilor se aplică numai funcția edges sau și alte funcții?
* Funcția edges însăși se aplică numai asupra subgrafurilor sau și asupra
  altor parametri?

Din păcate, veți oberva că nu este compozițională, întrucât asupra subgrafurilor
se aplică și funcția nodes, nu numai funcția edges. În plus, subgrafurile sunt
parcurse repetat, atât de edges, cât și de nodes, ceea ce duce la o eficiență
scăzută.

Utilizați tupling și equational reasoning pentru a o transforma într-o variantă
compozițională, numită nodesEdges. Mai precis, impuneți proprietatea

nodesEdges graph = (nodes graph, edges graph),

și derivați mai jos o definiție mai eficientă a funcției nodesEdges,
care să parcurgă graful o singură dată. Folosiți definițiile funcțiilor
nodes și edges din etapele 2 și 3.

DERIVARE:

{-
Proprietatea impusa:
(1) nodesEdges graph = (nodes graph, edges graph)

1. Cazul Empty:
nodesEdges Empty
= (nodes Empty, edges Empty)
= (Set.empty, Set.empty)

2. Cazul Node node:
nodesEdges (Node node)
= (nodes (Node node), edges (Node node))
= (Set.singleton node, Set.empty)

3. Cazul Overlay g1 g2:
nodesEdges (Overlay g1 g2)
= (nodes (Overlay g1 g2), edges (Overlay g1 g2))
= (Set.union nodes1 nodes2, Set.union edges1 edges2)
  unde (nodes1, edges1) = nodesEdges g1
       (nodes2, edges2) = nodesEdges g2

4. Cazul Connect g1 g2:
nodesEdges (Connect g1 g2)
= (nodes (Connect g1 g2), edges (Connect g1 g2))
= (Set.union nodes1 nodes2, Set.unions [edges1, edges2, newEdges])
  unde (nodes1, edges1) = nodesEdges g1
       (nodes2, edges2) = nodesEdges g2
       newEdges = Set.fromList [(x, y) | x <- Set.toList nodes1, y <- Set.toList nodes2]
-}

-}
nodesEdges :: Ord a => AlgebraicGraph a -> (Set a, Set (a, a))
nodesEdges graph = case graph of
    -- Am returnat doua Set-uri goale pentru graful gol
    Empty -> (Set.empty, Set.empty)

    -- Am pus nodul in primul Set si arcele raman goale
    Node node -> (Set.singleton node, Set.empty)

    -- Am calculat nodurile si arcele pentru ambele parti si le-am unit separat
    Overlay g1 g2 ->
        let (nodes1, edges1) = nodesEdges g1
            (nodes2, edges2) = nodesEdges g2
        in (Set.union nodes1 nodes2, Set.union edges1 edges2)

    -- Am folosit nodesEdges pe ambele parti si apoi am adaugat arcele dintre stanga si dreapta
    Connect g1 g2 ->
        let (nodes1, edges1) = nodesEdges g1
            (nodes2, edges2) = nodesEdges g2
            newEdges = Set.fromList [(x, y) | x <- Set.toList nodes1, y <- Set.toList nodes2]
        in (Set.union nodes1 nodes2, Set.unions [edges1, edges2, newEdges])

{-
Din păcate, deși nodesEdges este compozițională, ea nu poate fi implementată
cu foldr, întrucât cea din urmă expune o vedere liniară asupra grafului,
ascunzând structura sa ierarhică, cu subgrafuri combinate prin Overlay
și Connect.

În plus, deși nodesEdges este mai eficientă decât edges, pare că prețul plătit
pentru eficiența sporită este pierderea modularității și a reutilizării,
întrucât funcția nodes a trebuit reimplementată în definiția lui nodesEdges.

În vederea beneficierii atât de eficiență, cât și de modularitate/reutilizare,
soluția este definirea unui mecanism mai expresiv de reducere (folding) a
grafului, care să expună structura sa ierarhică.

Tipul de date AlgebraicGraphFolder reprezintă o colecție de funcții care
permit reducerea diverselor forme pe care le poate lua graful, presupunând
că subgrafurile au fost deja reduse recursiv.

Semnificația variabilelor de tip:

* a = tipul nodurilor din graf (la fel ca în AlgebraicGraph a)
* b = tipul rezultatului reducerii subgrafurilor
* c = tipul rezultatului reducerii grafului curent
-}
data AlgebraicGraphFolder a b c = AlgebraicGraphFolder
    { foldEmpty   :: c
    , foldNode    :: a -> c
    , foldOverlay :: b -> b -> c
    , foldConnect :: b -> b -> c
    }

{-
În măsura în care tipurile reducerilor subgrafurilor și a grafului curent
coincid (b), putem reduce întregul graf la același tip b. Observați parametrul
cu tipul (AlgebraicGraphFolder a b b).
-}
foldAlgebraicGraph :: AlgebraicGraphFolder a b b -> AlgebraicGraph a -> b
foldAlgebraicGraph folder = go
  where
    go Empty = foldEmpty folder
    go (Node node) = foldNode folder node
    go (Overlay g1 g2) = foldOverlay folder (go g1) (go g2)
    go (Connect g1 g2) = foldConnect folder (go g1) (go g2)

{-
*** TODO 4 (15p) ***

Reimplementați funcția nodes folosind noul mecanism de reducere. Propriu-zis,
trebuie să implementați doar AlgrabraicGraphFolder-ul.

CONSTRÂNGERI:

* Toate funcțiile din AlgebraicGraphFolder trebuie implementate folosind stilul
  point-free.

>>> nodes triangle
fromList [1,2,3]
-}
nodes :: Ord a => AlgebraicGraph a -> Set a
nodes = foldAlgebraicGraph nodesFolder
-- Am folosit foldAlgebraicGraph cu nodesFolder ca sa obtin nodurile

nodesFolder :: Ord a => AlgebraicGraphFolder a (Set a) (Set a)
nodesFolder = AlgebraicGraphFolder
    { foldEmpty   = Set.empty
    -- Am folosit Set.empty pentru cazul Empty

    , foldNode    = Set.singleton
    -- Am folosit Set.singleton pe fiecare nod

    , foldOverlay = Set.union
    -- Am folosit Set.union pe rezultatele din Overlay

    , foldConnect = Set.union
    -- Am folosit Set.union pe rezultatele din Connect
    }

{-
*** TODO 5 (15p) ***

Implementați funcția isNode, care verifică dacă un nod aparține într-adevăr
unui graf, utilizând noul mecanism de reducere. Propriu-zis, trebuie să
implementați doar AlgrabraicGraphFolder-ul.

CONSTRÂNGERI:

* Toate funcțiile din AlgebraicGraphFolder trebuie implementate folosind stilul
  point-free.

Exemple:

>>> isNode 1 triangle
True

>>> isNode 4 triangle
False
-}
isNode :: Eq a => a -> AlgebraicGraph a -> Bool
isNode = foldAlgebraicGraph . isNodeFolder
-- Am compus foldAlgebraicGraph cu isNodeFolder ca sa verific nodul cautat

isNodeFolder :: Eq a => a -> AlgebraicGraphFolder a Bool Bool
isNodeFolder node = AlgebraicGraphFolder
    { foldEmpty   = False
    -- Am folosit False pentru cazul Empty

    , foldNode    = (== node)
    -- Am folosit == node pe fiecare nod gasit

    , foldOverlay = (||)
    -- Am folosit || ca sa combin rezultatele din Overlay

    , foldConnect = (||)
    -- Am folosit || ca sa combin rezultatele din Connect
    }

{-
Operatorul (<+>) combină două foldere INDEPENDENTE, care reduc graful la tipuri
diferite (b și c), într-un folder care reduce graful la o pereche de tipuri
(b, c).

infixl (l = left) asigură asociativitatea la stânga a operatorului (vedeți
exemplul 2).

Exemple:

>>> foldAlgebraicGraph (nodesFolder <+> isNodeFolder 2) triangle
(fromList [1,2,3],True)

>>> foldAlgebraicGraph (nodesFolder <+> isNodeFolder 2 <+> nodesFolder) triangle
((fromList [1,2,3],True),fromList [1,2,3])
-}
infixl 5 <+>
(<+>) :: AlgebraicGraphFolder a b b
      -> AlgebraicGraphFolder a c c
      -> AlgebraicGraphFolder a (b, c) (b, c)
folder1 <+> folder2 = AlgebraicGraphFolder
    { foldEmpty = (foldEmpty folder1, foldEmpty folder2)
    , foldNode = \node -> (foldNode folder1 node, foldNode folder2 node)
    , foldOverlay = \(b1, c1) (b2, c2) ->
        (foldOverlay folder1 b1 b2, foldOverlay folder2 c1 c2)
    , foldConnect = \(b1, c1) (b2, c2) ->
        (foldConnect folder1 b1 b2, foldConnect folder2 c1 c2)
    }

{-
Operatorul (>.>) combină două foldere SEMIDEPENDENTE, care reduc graful la
tipuri diferite (b și c), într-un folder care reduce graful la o pereche de
tipuri (b, c).

Parantezele unghiulare indică sensul dependenței, de la stânga la dreapta.
Primul folder este independent, reducând graful la tipul b, în timp ce al
doilea folder este dependent de primul, și reduce graful la tipul c, pornind
de la informația calculată de AMBELE foldere, (b, c).

infixl (l = left) asigură asociativitatea la stânga a operatorului.
-}
infixl 5 >.>
(>.>) :: AlgebraicGraphFolder a  b     b
      -> AlgebraicGraphFolder a (b, c) c
      -> AlgebraicGraphFolder a (b, c) (b, c)
folder1 >.> folder2 = AlgebraicGraphFolder
    { foldEmpty = (foldEmpty folder1, foldEmpty folder2)
    , foldNode = \node -> (foldNode folder1 node, foldNode folder2 node)
    , foldOverlay = \(b1, c1) (b2, c2) ->
        (foldOverlay folder1 b1 b2, foldOverlay folder2 (b1, c1) (b2, c2))
    , foldConnect = \(b1, c1) (b2, c2) ->
        (foldConnect folder1 b1 b2, foldConnect folder2 (b1, c1) (b2, c2))
    }

{-
*** TODO 6 (20p) ***

Reimplementați funcția edges folosind noul mecanism de reducere. Propriu-zis,
trebuie să implementați doar AlgrabraicGraphFolder-ul.

De data aceasta, mulțimea de arce produsă de folder, Set (a, a), depinde
nu numai de mulțimile de muchii calculate pentru subgrafuri, Set (a, a), ci și
de mulțimile de noduri calculate pentru aceleași subgrafuri, Set a. Din acest
motiv, funcțiile din folder iau ca parametri perechi între o mulțime de noduri
și una de muchii, (Set a, Set (a, a)).

Observați că acum nu a mai trebuit să reimplementăm funcționalitatea lui nodes,
ca în funcția nodesEdges de mai sus. Am putut reutiliza funcționalitatea lui
nodes, dar nu la nivelul întregii funcții, ci doar la nivelul folderului său.

Exemple:

>>> edges triangle
fromList [(1,2),(1,3),(2,3)]
-}
edges :: Ord a => AlgebraicGraph a -> Set (a, a)
edges = snd . foldAlgebraicGraph (nodesFolder >.> edgesFolder)

edgesFolder :: Ord a => AlgebraicGraphFolder a (Set a, Set (a, a)) (Set (a, a))
edgesFolder = AlgebraicGraphFolder
      -- Set (a, a)
    { foldEmpty = Set.empty
      -- Am folosit Set.empty pentru cazul Empty

      -- a -> Set (a, a)
    , foldNode = const Set.empty
      -- Am folosit const Set.empty fiindca un nod singur nu are arce

      -- (Set a, Set (a, a)) -> (Set a, Set (a, a)) -> Set (a, a)
    , foldOverlay = \(_, edges1) (_, edges2) -> Set.union edges1 edges2
      -- Am folosit Set.union pe arcele din cele doua subgrafuri

      -- (Set a, Set (a, a)) -> (Set a, Set (a, a)) -> Set (a, a)
    , foldConnect = \(nodes1, edges1) (nodes2, edges2) ->
        let newEdges = Set.fromList [(x, y) | x <- Set.toList nodes1, y <- Set.toList nodes2]
        in Set.unions [edges1, edges2, newEdges]
      -- Am folosit Set.fromList pe toate perechile dintre nodurile din stanga si dreapta
    }
