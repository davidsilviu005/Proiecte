{-# LANGUAGE TupleSections #-}
module StandardGraph where

import Data.Set (Set)
import qualified Data.Set as Set

{-
Graf ORIENTAT cu noduri de tipul a, reprezentat prin mulțimile (set) de noduri
și de arce.

Mulțimile sunt utile pentru că ignoră duplicatele și permit testarea egalității
a două grafuri independent de ordinea nodurilor și a arcelor.

type introduce un sinonim de tip, similar cu typedef din C.
-}
type StandardGraph a = (Set a, Set (a, a))

{-
Exemple de grafuri, construite pe baza funcției fromComponents de mai jos.
Observați nodurile și arcele duplicate.
-}
graph1 :: StandardGraph Int
graph1 = fromComponents [1, 3, 2, 3, 4] [(1, 2), (1, 3), (1, 2)]

graph2 :: StandardGraph Int
graph2 = fromComponents [4, 3, 3, 2, 1] [(1, 3), (1, 3), (1, 2)]

graph3 :: StandardGraph Int
graph3 = fromComponents [1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (2, 3), (1, 3)]

graph4 :: StandardGraph Int
graph4 = fromComponents [1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (2, 4), (1, 3)]

tree :: StandardGraph Int
tree = fromComponents
    [1 .. 15]
    [ (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)
    , (2, 7), (2, 8)
    , (3, 9), (3, 10)
    , (4, 11), (4, 12)
    , (5, 13), (5, 14)
    , (7, 15)
    ]

shouldBeTrue :: Bool
shouldBeTrue = graph1 == graph2

{-
*** TODO 1 (3p) ***

Implementați funcția fromComponents, care construiește un graf pe baza listelor
de noduri și de arce.

Constrângerea (Ord a) afirmă că valorile tipului a trebuie să fie ordonabile,
lucru necesar pentru reprezentarea internă a mulțimilor. Este doar un detaliu,
cu care nu veți opera explicit în această etapă. Veți întâlni această
constrângere și în tipurile funcțiilor de mai jos.

Hint: Set.fromList.

Exemple:

>>> graph1
(fromList [1,2,3,4],fromList [(1,2),(1,3)])
-}
fromComponents :: Ord a
               => [a]              -- lista nodurilor
               -> [(a, a)]         -- lista arcelor
               -> StandardGraph a  -- graful construit
fromComponents nodes edges = (Set.fromList nodes, Set.fromList edges)
-- Am transformat listele in Set-uri ca sa elimin automat duplicatele

{-
*** TODO 2 (1p) ***

Implementați funcția nodes, care întoarce mulțimea nodurilor grafului.

Exemple:

>>> nodes graph1
fromList [1,2,3,4]
-}
nodes :: StandardGraph a -> Set a
nodes = fst
-- Am folosit fst pentru ca nodurile sunt prima parte din perechea grafului

{-
*** TODO 3 (1p) ***

Implementați funcția edges, care întoarce mulțimea arcelor grafului.

>>> edges graph1
fromList [(1,2),(1,3)]
-}
edges :: StandardGraph a -> Set (a, a)
edges = snd
-- Am folosit snd pentru ca arcele sunt a doua parte din perechea grafului

{-
*** TODO 4 (10p) ***

Implementați funcția outNeighbors, care întoarce mulțimea nodurilor înspre care
pleacă arce dinspre un nod sursă.

Exemple:

>>> outNeighbors 1 graph3
fromList [2,3,4]
-}
outNeighbors :: Ord a => a -> StandardGraph a -> Set a
outNeighbors from graph =
    Set.fromList [to | (x, to) <- Set.toList (edges graph), x == from]
    -- Am parcurs arcele si am pastrat doar destinatiile unde sursa este nodul cautat

{-
*** TODO 5 (10p) ***

Implementați funcția inNeighbors, care întoarce mulțimea nodurilor dinspre care
pleacă arce înspre un nod destinație.

Exemple:

>>> inNeighbors 1 graph3
fromList [4]
-}
inNeighbors :: Ord a => a -> StandardGraph a -> Set a
inNeighbors to graph =
    Set.fromList [from | (from, x) <- Set.toList (edges graph), x == to]
    -- Am parcurs arcele si am pastrat doar sursele care ajung in nodul cautat

{-
*** TODO 6 (15p) ***

Implementați funcția removeNode, care întoarce graful rezultat prin eliminarea
unui nod și a arcelor în care acesta este implicat. Dacă nodul nu există,
întoarce același graf.

Exemple:

>>> removeNode 1 graph3
(fromList [2,3,4],fromList [(2,3)])
-}
removeNode :: Ord a => a -> StandardGraph a -> StandardGraph a
removeNode node graph =
    (newNodes, newEdges)
    where
        -- Am sters nodul primit din multimea de noduri
        newNodes = Set.delete node (nodes graph)

        -- Am pastrat doar arcele care nu contin nodul sters
        newEdges = Set.fromList
            [ (from, to) | (from, to) <- Set.toList (edges graph)
            , from /= node
            , to /= node
            ]

{-
*** TODO 7 (20p) ***

Implementați funcția splitNode, care divizează un nod în mai multe noduri,
cu eliminarea nodului inițial. Arcele în care era implicat vechiul nod trebuie
să devină valabile pentru noile noduri.

Exemplu:

>>> splitNode 2 (Set.fromList [5,6]) graph3
(fromList [1,3,4,5,6],fromList [(1,3),(1,4),(1,5),(1,6),(4,1),(5,3),(6,3)])
-}
splitNode :: Ord a
          => a                -- nodul divizat
          -> Set a            -- nodurile cu care este înlocuit
          -> StandardGraph a  -- graful existent
          -> StandardGraph a  -- graful obținut
splitNode old news graph = (newNodes, newEdges)
    where
        -- Am scos nodul vechi si am adaugat nodurile noi in locul lui
        newNodes = Set.union news (Set.delete old (nodes graph))

        -- Am refacut arcele folosind replace, ca nodul vechi sa fie inlocuit cu nodurile noi.
        newEdges = Set.fromList
            [ (fromNew, toNew) | (from, to) <- Set.toList (edges graph)
            , fromNew <- replace from
            , toNew <- replace to
            ]

        -- Daca gasesc nodul vechi, il inlocuiesc cu lista nodurilor noi
        -- Daca nu, il las asa cum era
        replace x
            | x == old = Set.toList news
            | otherwise = [x]

{-
*** TODO 8 (15p) ***

Implementați funcția mergeNodes, care îmbină mai multe noduri într-unul singur,
pe baza unei proprietăți respectate de nodurile îmbinate, cu eliminarea
acestora. Arcele în care erau implicate vechile noduri vor referi nodul nou.

Exemple:

>>> mergeNodes even 5 graph3
(fromList [1,3,5],fromList [(1,3),(1,5),(5,1),(5,3)])
-}
mergeNodes :: Ord a
           => (a -> Bool)      -- proprietatea îndeplinită de nodurile îmbinate
           -> a                -- noul nod
           -> StandardGraph a  -- graful existent
           -> StandardGraph a  -- graful obținut
mergeNodes prop node graph
    -- Daca nu am niciun nod care respecta proprietatea, las graful neschimbat.
    | Set.null oldNodes = graph
    | otherwise = (newNodes, newEdges)
    where
        -- Am cautat toate nodurile care trebuie unite
        oldNodes = Set.fromList [x | x <- Set.toList (nodes graph), prop x]

        -- Am pastrat nodurile care nu se unesc si am adaugat nodul nou
        newNodes = Set.insert node
            (Set.fromList [x | x <- Set.toList (nodes graph), not (prop x)])

        -- Am inlocuit in arce nodurile vechi cu nodul nou
        newEdges = Set.fromList
            [(replace from, replace to) | (from, to) <- Set.toList (edges graph)]

        -- Daca nodul respecta proprietatea, il transform in nodul nou
        -- Altfel ramane la fel
        replace x
            | prop x = node
            | otherwise = x
