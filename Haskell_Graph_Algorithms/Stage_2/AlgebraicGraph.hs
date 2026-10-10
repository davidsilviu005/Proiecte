module AlgebraicGraph where

import Data.Set (Set)
import qualified Data.Set as Set

data AlgebraicGraph a
    = Empty
    | Node { label :: a }
    | Overlay { left :: AlgebraicGraph a, right :: AlgebraicGraph a }
    | Connect { left :: AlgebraicGraph a, right :: AlgebraicGraph a }
    deriving (Eq, Ord, Show)

-- (1, 2), (1, 3)
angle :: AlgebraicGraph Int
angle = Connect (Node 1) (Overlay (Node 2) (Node 3))

-- (1, 2), (1, 3), (2, 3)
triangle :: AlgebraicGraph Int
triangle = Connect (Node 1) (Connect (Node 2) (Node 3))

{-
*** TODO 1 (10p) ***

Implementați funcția nodes, care întoarce mulțimea nodurilor grafului.

Hint: Set.union

Exemple:

>>> nodes triangle
fromList [1,2,3]
-}
nodes :: Ord a => AlgebraicGraph a -> Set a
nodes graph= case graph of
    -- Pentru graful gol nu am niciun nod
    Empty -> Set.empty

    -- Pentru un singur nod fac un Set.singleton care contine doar acel nod
    Node x -> Set.singleton x

    -- La Overlay Set.union nodurile din partea stanga cu cele din partea dreapta
    Overlay l r -> Set.union (nodes l) (nodes r)

    -- La Connect tot trebuie sa iau nodurile din ambele parti
    Connect l r -> Set.union (nodes l) (nodes r)

{-
*** TODO 2 (10p) ***

Implementați funcția edges, care întoarce mulțimea arcelor grafului.

Hint: Set.union, Set.cartesianProduct

Exemple:

>>> edges triangle
fromList [(1,2),(1,3),(2,3)]
-}
edges :: Ord a => AlgebraicGraph a -> Set (a, a)
edges graph = case graph of
    -- Graful gol nu are arce
    Empty -> Set.empty

    -- Un singur nod nu formeaza niciun arc
    Node _ -> Set.empty

    -- La Overlay doar Set.union pe arcele care exista deja in cele doua parti
    Overlay l r -> Set.union (edges l) (edges r)

    -- La Connect pastrez arcele existente si adaug toate arcele din stanga spre dreapta
    Connect l r -> Set.unions [edges l, edges r, Set.cartesianProduct (nodes l) (nodes r)]

{-
*** TODO 3 (15p) ***

Implementați funcția outNeighbors, care întoarce mulțimea nodurilor înspre care
pleacă arce dinspre un nod sursă.

CONSTRÂNGERI:

* NU folosiți funcția edges definită mai sus, pentru că ar genera prea multe
  muchii inutile.
* Evitați trimiterea către apelurile recursive a parametrilor care nu se
  modifică. De exemplu, parametrul node nu se modifică, în timp ce parametrul
  graph se modifică. Pentru aceasta, definiți o funcție recursivă locală (de
  exemplu, în where), care să primească drept parametri doar entitățile
  variabile de la un apel recursiv la altul.

Exemple:

>>> outNeighbors 1 triangle
fromList [2,3]
-}
outNeighbors :: Ord a => a -> AlgebraicGraph a -> Set a
outNeighbors node graph = go graph
  where
      -- Pentru graful gol nu exista vecini
      go Empty = Set.empty

      -- Un nod singur nu are muchii care pleaca din el
      go (Node _) = Set.empty

      -- La Overlay caut vecinii in ambele parti si ii unesc
      go (Overlay l r) = Set.union (go l) (go r)

      -- La Connect iau vecinii existenti, iar daca nodul este in stanga,
      -- atunci toate nodurile din dreapta devin vecini de iesire
      go (Connect l r) = Set.unions [go l, go r, if Set.member node (nodes l) then nodes r else Set.empty]

{-
*** TODO 4 (15p) ***

Implementați funcția inNeighbors, care întoarce mulțimea nodurilor dinspre care
pleacă arce înspre un nod destinație.

CONSTRÂNGERI:

* NU folosiți funcția edges definită mai sus, pentru că ar genera prea multe
  muchii inutile.
* Evitați trimiterea către apelurile recursive a parametrilor care nu se
  modifică (vezi outNeighbors).

Exemple:

>>> inNeighbors 3 triangle
fromList [1,2]
-}
inNeighbors :: Ord a => a -> AlgebraicGraph a -> Set a
inNeighbors node graph = go graph
  where
    -- Pentru graful gol nu am vecini de intrare
    go Empty = Set.empty

    -- Un singur nod nu are arce care intra in el
    go (Node _) = Set.empty

    -- La Overlay caut in ambele parti si Set.union cu rezultatele
    go (Overlay l r) = Set.union (go l) (go r)

    -- La Connect, daca nodul cautat este in dreapta,
    -- atunci nodurile din stanga au arc spre el
    go (Connect l r) = Set.unions [go l, go r, if Set.member node (nodes r) then nodes l else Set.empty]

{-
*** TODO 5 (15p) ***

Implementați funcția removeNode, care întoarce graful rezultat prin eliminarea
unui nod și a arcelor în care acesta este implicat. Dacă nodul nu există,
întoarce același graf.

CONSTRÂNGERI:

* Evitați trimiterea către apelurile recursive a parametrilor care nu se
  modifică (vezi outNeighbors).

Exemple:

>>> removeNode 2 triangle
Connect {left = Node {label = 1}, right = Connect {left = Empty, right = Node {label = 3}}}

>>> nodes $ removeNode 2 triangle
fromList [1,3]

>>> edges $ removeNode 2 triangle
fromList [(1,3)]
-}
removeNode :: Eq a => a -> AlgebraicGraph a -> AlgebraicGraph a
removeNode node graph = go graph
  where
    -- Daca ajung la Empty, nu am ce sa sterg
    go Empty = Empty

    -- Daca nodul curent este cel cautat, il inlocuiesc cu Empty
    -- Altfel il las neschimbat
    go (Node x)
      | x == node = Empty
      | otherwise = Node x

    -- Aplic stergerea recursiv in ambele parti ale lui Overlay
    go (Overlay l r) = Overlay (go l) (go r)

    -- Aplic stergerea recursiv si in ambele parti ale lui Connect
    go (Connect l r) = Connect (go l) (go r)

{-
*** TODO 6 (20p) ***

Implementați funcția splitNode, care divizează un nod în mai multe noduri,
cu eliminarea nodului inițial. Arcele în care era implicat vechiul nod trebuie
să devină valabile pentru noile noduri.

CONSTRÂNGERI:

* Evitați trimiterea către apelurile recursive a parametrilor care nu se
  modifică (vezi outNeighbors).

Exemple:

>>> splitNode 2 (Set.fromList [4,5]) triangle
Connect {left = Node {label = 1}, right = Connect {left = Overlay {left = Node {label = 4}, right = Overlay {left = Node {label = 5}, right = Empty}}, right = Node {label = 3}}}

>>> nodes $ splitNode 2 (Set.fromList [4,5]) triangle
fromList [1,3,4,5]

>>> edges $ splitNode 2 (Set.fromList [4,5]) triangle
fromList [(1,3),(1,4),(1,5),(4,3),(5,3)]
-}
splitNode :: Ord a
          => a                 -- nodul divizat
          -> Set a             -- nodurile cu care este înlocuit
          -> AlgebraicGraph a  -- graful existent
          -> AlgebraicGraph a  -- graful obținut
splitNode node targets graph = go graph
  where
    -- Pentru Empty nu am ce sa impart
    go Empty = Empty

    -- Daca gasesc nodul cautat, il inlocuiesc cu toate nodurile din targets
    -- Daca nu, pastrez nodul asa cum era
    go (Node x)
      | x == node = makeNodes targets
      | otherwise = Node x

    -- Aplic impartirea recursiv in ambele parti ale lui Overlay
    go (Overlay l r) = Overlay (go l) (go r)

    -- Aplic impartirea recursiv in ambele parti ale lui Connect
    go (Connect l r) = Connect (go l) (go r)

    -- Transform Set-ul de noduri intr-un graf format cu Overlay
    makeNodes s
      | Set.null s = Empty
      | otherwise = Overlay (Node (Set.findMin s)) (makeNodes (Set.deleteMin s))

{-
*** TODO 7 (15p) ***

Implementați funcția mergeNodes, care îmbină mai multe noduri într-unul singur,
pe baza unei proprietăți respectate de nodurile îmbinate, cu eliminarea
acestora. Arcele în care erau implicate vechile noduri vor referi nodul nou.

CONSTRÂNGERI:

* Evitați trimiterea către apelurile recursive a parametrilor care nu se
  modifică (vezi outNeighbors).

Exemple:

>>> mergeNodes odd 4 triangle
Connect {left = Node {label = 4}, right = Connect {left = Node {label = 2}, right = Node {label = 4}}}

>>> nodes $ mergeNodes odd 4 triangle
fromList [2,4]

>>> edges $ mergeNodes odd 4 triangle
fromList [(2,4),(4,2),(4,4)]
-}
mergeNodes :: (a -> Bool)       -- proprietatea îndeplinită de nodurile îmbinate
           -> a                 -- noul nod
           -> AlgebraicGraph a  -- graful existent
           -> AlgebraicGraph a  -- graful obținut
mergeNodes prop node graph = go graph
  where
    -- Pentru Empty nu am ce sa unesc
    go Empty = Empty

    -- Daca nodul respecta proprietatea, il schimb cu nodul nou
    -- Daca nu, il las la fel
    go (Node x)
      | prop x = Node node
      | otherwise = Node x

    -- Aplic unirea recursiv in ambele parti ale lui Overlay
    go (Overlay l r) = Overlay (go l) (go r)

    -- Aplic unirea recursiv in ambele parti ale lui Connect
    go (Connect l r) = Connect (go l) (go r)
