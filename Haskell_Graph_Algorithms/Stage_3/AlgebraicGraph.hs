module AlgebraicGraph where

import Data.Set (Set)
import qualified Data.Set as Set

data AlgebraicGraph a
    = Empty
    | Node { label :: a }
    | Overlay { left :: AlgebraicGraph a, right :: AlgebraicGraph a }
    | Connect { left :: AlgebraicGraph a, right :: AlgebraicGraph a }
    deriving (Ord)

-- (1, 2), (1, 3)
-- 1 * (2 + 3)
angle :: AlgebraicGraph Int
angle = Connect (Node 1) (Overlay (Node 2) (Node 3))

-- (1, 2), (1, 3), (2, 3)
-- 1 * (2 * 3)
triangle :: AlgebraicGraph Int
triangle = Connect (Node 1) (Connect (Node 2) (Node 3))

{-
*** TODO ***

Funcția nodes din etapa 2.
-}
nodes :: Ord a => AlgebraicGraph a -> Set a
nodes graph= case graph of
    -- Am folosit Set.empty pentru graful fara noduri
    Empty -> Set.empty

    -- Am folosit Set.singleton pe eticheta nodului
    Node x -> Set.singleton x

    -- Am folosit Set.union pe nodurile din stanga si dreapta
    Overlay l r -> Set.union (nodes l) (nodes r)

    -- Am folosit Set.union si la Connect, tot pe cele doua parti
    Connect l r -> Set.union (nodes l) (nodes r)

{-
*** TODO ***

Funcția edges din etapa 2.
-}
edges :: Ord a => AlgebraicGraph a -> Set (a, a)
edges graph = case graph of
    -- Am folosit Set.empty fiindca Empty nu are arce
    Empty -> Set.empty

    -- Am folosit Set.empty fiindca un nod singur nu formeaza arc
    Node _ -> Set.empty

    -- Am folosit Set.union pe arcele din stanga si dreapta
    Overlay l r -> Set.union (edges l) (edges r)

    -- Am folosit Set.unions pentru arcele existente si produsul cartezian stanga-dreapta
    Connect l r -> Set.unions [edges l, edges r, Set.cartesianProduct (nodes l) (nodes r)]

{-
*** TODO ***

Funcția outNeighbors din etapa 2.
-}
outNeighbors :: Ord a => a -> AlgebraicGraph a -> Set a
outNeighbors node graph = go graph
  where
      -- Am folosit Set.empty pentru cazul fara graf
      go Empty = Set.empty

      -- Am folosit Set.empty fiindca un nod nu are vecini de iesire
      go (Node _) = Set.empty

      -- Am folosit Set.union pe vecinii gasiti in ambele parti
      go (Overlay l r) = Set.union (go l) (go r)

      -- Am folosit Set.member pe stanga ca sa vad daca adaug nodurile din dreapta
      go (Connect l r) = Set.unions [go l, go r, if Set.member node (nodes l) then nodes r else Set.empty]

{-
*** TODO ***

Funcția inNeighbors din etapa 2.
-}
inNeighbors :: Ord a => a -> AlgebraicGraph a -> Set a
inNeighbors node graph = go graph
  where
    -- Am folosit Set.empty pentru cazul fara graf
    go Empty = Set.empty

    -- Am folosit Set.empty fiindca un nod nu are vecini de intrare
    go (Node _) = Set.empty

    -- Am folosit Set.union pe vecinii gasiti in ambele parti
    go (Overlay l r) = Set.union (go l) (go r)

    -- Am folosit Set.member pe dreapta ca sa vad daca adaug nodurile din stanga
    go (Connect l r) = Set.unions [go l, go r, if Set.member node (nodes r) then nodes l else Set.empty]

{-
*** TODO 1 (10p) ***

Instanțiați clasa Num cu tipul (AlgebraicGraph a), astfel încât:

* un literal întreg să fie interpretat ca un singur nod cu eticheta egală
    cu acel literal
* operația de adunare să fie intepretată ca Overlay
* operația de înmulțire să fie interpretată drept Connect.

Celelalte funcții din clasă nu sunt relevante. Veți obține warning-uri
pentru neimplementarea lor, dar puteți să le ignorați.

După instanțiere, veți putea evalua în consolă expresii ca:

>>> 1 :: AlgebraicGraph Int
1

>>> 1*(2+3) :: AlgebraicGraph Int
(1*(2+3))
-}
instance Num a => Num (AlgebraicGraph a) where
    -- Am folosit fromInteger ca sa transform un numar intr-un nod
    fromInteger n = Node (fromInteger n)

    -- Am folosit Overlay pentru adunarea de grafuri
    (+) = Overlay

    -- Am folosit Connect pentru inmultirea de grafuri
    (*) = Connect

{-
*** TODO 2 (10p) ***

Instanțiați clasa Show cu tipul (AlgebraicGraph a), astfel încât reprezentarea
sub formă de șir de caractere a unui graf să reflecte expresiile aritmetice
definite mai sus. Puteți pune un nou rând de paranteze pentru fiecare
subexpresie compusă.

Exemple:

>>> Node 1
1

>>> Connect (Node 1) (Overlay (Node 2) (Node 3))
(1*(2+3))
-}
instance Show a => Show (AlgebraicGraph a) where
    show graph = case graph of
        -- Am afisat graful gol cu _
        Empty -> "_"

        -- Am folosit show pe eticheta nodului
        Node x -> show x

        -- Am pus + intre cele doua subgrafuri
        Overlay l r -> "(" ++ show l ++ "+" ++ show r ++ ")"

        -- Am pus * intre cele doua subgrafuri
        Connect l r -> "(" ++ show l ++ "*" ++ show r ++ ")"

{-
*** TODO 3 (10p) ***

Observați că instanța predefinită de Eq pentru tipul (AlgebraicGraph a)
nu surprinde corect egalitatea a două grafuri, deoarece același graf
conceptual poate avea două descrieri simbolice diferite.

Prin urmare, instanțiați clasa Eq cu tipul (AlgebraicGraph a), astfel încât
să comparați propriu-zis mulțimile de noduri și de arce.

Exemple:

>>> Node 1 == 1
True

>>> Node 1 == 2
False

>>> angle == 1*2 + 1*3
True

>>> triangle == (1*2)*3
True
-}
instance Ord a => Eq (AlgebraicGraph a) where
    -- Am comparat grafurile dupa noduri si dupa arce
    (==) g1 g2 = nodes g1 == nodes g2 && edges g1 == edges g2

{-
*** TODO 4 (15p) ***

Implementați funcția extend, care extinde un graf existent, atașând noi
subgrafuri arbitrare în locul nodurilor individuale. Funcția primită ca prim
parametru determină această corespondență între noduri și subgrafuri. Observați
că tipul etichetelor noi (b) poate diferi de al etichetelor vechi (a).

Exemplu:

>>> extend (\n -> if n == 1 then 4+5 else Node n) $ 1*(2+3)
((4+5)*(2+3))
-}
extend :: (a -> AlgebraicGraph b) -> AlgebraicGraph a -> AlgebraicGraph b
extend f graph = case graph of
    -- Am pastrat Empty tot ca Empty
    Empty -> Empty

    -- Am aplicat functia f pe eticheta nodului
    Node x -> f x

    -- Am aplicat extend recursiv pe ambele parti din Overlay
    Overlay l r -> Overlay (extend f l) (extend f r)

    -- Am aplicat extend recursiv pe ambele parti din Connect
    Connect l r -> Connect (extend f l) (extend f r)

{-
*** TODO 5 (15p) ***

Implementați funcția splitNode, care divizează un nod în mai multe noduri,
cu eliminarea nodului inițial. Arcele în care era implicat vechiul nod trebuie
să devină valabile pentru noile noduri.

CONSTRÂNGERI:

* Implementați splitNode folosind extend!

Exemple:

>>> splitNode 2 (Set.fromList [4,5]) triangle
(1*((4+(5+_))*3))
-}
splitNode :: Ord a
          => a                 -- nodul divizat
          -> Set a             -- nodurile cu care este înlocuit
          -> AlgebraicGraph a  -- graful existent
          -> AlgebraicGraph a  -- graful obținut
splitNode node targets graph = extend replace graph
  where
    -- Am folosit replace cu extend ca sa schimb doar nodul cautat
    replace x
        -- Am folosit Set.foldr pe targets ca sa fac Overlay intre nodurile noi
        | x == node = Set.foldr (Overlay . Node) Empty targets

        -- Am pastrat restul nodurilor neschimbate
        | otherwise = Node x

{-
*** TODO 6 (5p) ***

Instanțiați clasa Functor cu constructorul de tip AlgebraicGraph, astfel încât
să puteți aplica o funcție pe toate etichetele unui graf. fmap reprezintă
generalizarea lui map pentru alte structuri.

CONSTRÂNGERI:

* Implementați fmap folosind extend!

Exemple:

>>> fmap (+ 10) $ 1*(2+3) :: AlgebraicGraph Int
(11*(12+13))
-}
instance Functor AlgebraicGraph where
    -- fmap :: (a -> b) -> AlgebraicGraph a -> AlgebraicGraph b

    -- Am folosit extend cu Node . f ca sa modific toate etichetele
    fmap f graph = extend (Node . f) graph

{-
*** TODO 7 (10p) ***

Implementați funcția mergeNodes, care îmbină mai multe noduri într-unul singur,
pe baza unei proprietăți respectate de nodurile îmbinate, cu eliminarea
acestora. Arcele în care erau implicate vechile noduri vor referi nodul nou.

CONSTRÂNGERI:

* Implementați mergeNodes folosind fmap!

Exemple:

>>> mergeNodes odd 4 triangle
(4*(2*4))
-}
mergeNodes :: (a -> Bool)       -- proprietatea îndeplinită de nodurile îmbinate
           -> a                 -- noul nod
           -> AlgebraicGraph a  -- graful existent
           -> AlgebraicGraph a  -- graful obținut
mergeNodes prop node graph = fmap (\x -> if prop x then node else x) graph
-- Am folosit fmap ca sa inlocuiesc nodurile care respecta prop cu nodul nou

{-
*** TODO 8 (10p) ***

Implementați funcția filterGraph, care filtrează un graf, păstrând doar
nodurile care satisfac proprietatea dată.

CONSTRÂNGERI:

* Implementați filterGraph folosind extend!

Exemplu:

>>> filterGraph odd triangle
(1*(_*3))
-}
filterGraph :: (a -> Bool) -> AlgebraicGraph a -> AlgebraicGraph a
filterGraph prop graph = extend (\x -> if prop x then Node x else Empty) graph
-- Am folosit extend ca sa pastrez nodurile care respecta prop si sa sterg restul

{-
*** TODO 9 (5p) ***

Implementați funcția removeNode, care întoarce graful rezultat prin eliminarea
unui nod și a arcelor în care acesta este implicat. Dacă nodul nu există,
întoarce același graf.

CONSTRÂNGERI:

* Implementați removeNode folosind filterGraph!

Exemplu:

>>> removeNode 2 triangle
(1*(_*3))
-}
removeNode :: Eq a => a -> AlgebraicGraph a -> AlgebraicGraph a
removeNode node graph = filterGraph (/= node) graph
-- Am folosit filterGraph cu /= node ca sa elimin nodul cautat

class Graph g where

instance Graph AlgebraicGraph where

instance Graph (AlgebraicGraph a) where
