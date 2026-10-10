module Modular where

import Data.Set (Set)
import qualified Data.Set as Set
import AlgebraicGraph hiding (Graph)
import Data.Foldable ( minimumBy )
import Data.Ord ( comparing )

type Graph a = AlgebraicGraph a

-- Graful descris în diagrama din enunțul temei
diagram :: AlgebraicGraph Int
diagram = ((1*2) * (3+4)) * 5

{-
O partiție este o mulțime de submulțimi ale unei alte mulțimi, disjuncte
(fără elemente comune) și care împreună conțin toate elementele originale.

De exemplu, pentru mulțimea [1,2,3], o posibilă partiție este [[1], [2,3]].
-}
type Partition a = Set (Set a)

{-
*** TODO ***

Funcția mapSingle din etapa 2.
-}
mapSingle :: (a -> a) -> [a] -> [[a]]
mapSingle f xs = go [] xs
  where
    -- Cand nu mai am elemente, nu mai am ce modifica
    go _ [] = []

    -- Am folosit before si after ca sa modific doar elementul curent
    go before (x : after) =
      (before ++ [f x] ++ after) : go (before ++ [x]) after

{-
*** TODO ***

Funcția partitions din etapa 2.
-}
partitions :: [a] -> [[[a]]]
partitions xs = go xs
  where
    -- Pentru lista goala am returnat partitia goala
    go [] = [[]]

    -- Am folosit smaller ca sa construiesc partitiile pentru x si restul listei
    go (x : rest) = [ [x] : p | p <- smaller] ++ [p2 | p <- smaller, p2 <- mapSingle (x :) p]
      where
        -- Am calculat partitiile pentru restul listei
        smaller = go rest

{-
*** TODO 10 (10p) ***

Implementați funcția isModule, care verifică dacă o mulțime este un modul,
i.e. dacă toate nodurile din mulțime au aceeași mulțime de vecini out și
aceeași mulțime de vecini in, în exteriorul mulțimii de plecare. Cu alte
cuvinte, excludem din verificare vecinii din interiorul mulțimii de plecare.

Hint: Set.map poate reduce dimensiunea unei mulțimi dacă elemente diferite
inițial sunt asociate cu același element final, întrucât nu pot exista
duplicate.

Exemple:

>>> isModule (Set.fromList [1,2,3,4]) diagram
True

>>> isModule (Set.fromList [5]) diagram
True

>>> isModule (Set.fromList [1,2]) diagram
True

>>> isModule (Set.fromList [3,4]) diagram
True

>>> isModule (Set.fromList [1,3]) diagram
False
-}
isModule :: Ord a
         => Set a
         -> Graph a
         -> Bool
isModule set graph =
    Set.size (Set.map out set) <= 1 &&
    Set.size (Set.map inn set) <= 1
  where
    -- Am folosit Set.difference ca sa scot vecinii din interiorul multimii
    out x = Set.difference (outNeighbors x graph) set

    -- Am folosit Set.difference si pe vecinii de intrare
    inn x = Set.difference (inNeighbors x graph) set

{-
*** TODO 11 (8p) ***

Implementați funcția isModularPartition, care verifică dacă o partiție
a mulțimii de noduri constituie o descompunere modulară. Partiția este
reprezentată ca o mulțime de mulțimi.

Hint: la fel ca la isModule.

Exemple:

>>> isModularPartition (toPartition [[1], [2], [3], [4], [5]]) diagram
True

>>> isModularPartition (toPartition [[1,2,3,4,5]]) diagram
True

>>> isModularPartition (toPartition [[1,2,3,4], [5]]) diagram
True

>>> isModularPartition (toPartition [[1,2], [3,4], [5]]) diagram
True

>>> isModularPartition (toPartition [[1,3], [2,4,5]]) diagram
False
-}
isModularPartition :: Ord a
                   => Partition a
                   -> Graph a
                   -> Bool
isModularPartition partition graph = coversAll && disjoint && allModules
  where
    -- Am folosit Set.foldr cu Set.union ca sa unesc toate partile
    unionParts = Set.foldr Set.union Set.empty partition

    -- Am adunat dimensiunile partilor ca sa verific daca se suprapun
    totalSize = sum (map Set.size (Set.toList partition))

    -- Am verificat daca partitia acopera toate nodurile grafului
    coversAll = unionParts == nodes graph

    -- Am comparat dimensiunile ca sa vad daca partile sunt disjuncte
    disjoint = totalSize == Set.size unionParts

    -- Am folosit isModule pe fiecare parte din partitie
    allModules = all (\part -> isModule part graph) (Set.toList partition)

{-
*** TODO 12 (12p) ***

Implementați funcția maximalModularPartition, care determină partiția maximală
dintr-o mulțime de partiții. Partiția maximală conține cele mai acoperitoare
submulțimi ale mulțimii de noduri. Cu alte cuvinte, partiția maximală conține
cel mai mic număr de submulțimi mai mare strict decât 1, pentru a exlcude
partiția banală care conține doar întreaga mulțime de noduri.

Hint: minimumBy din Data.Foldable. Funcția este folosită pentru a stabili
un criteriu ad-hoc de ordonare, conform valorii întoarse de o funcție f
când este aplicată pe elementele structurii, printr-o construcție de forma:

minimumBy (comparing f) structura.

Exemple:

> maximalModularPartition <mulțimea partițiilor> diagram
fromList [fromList [1,2,3,4],fromList [5]]

> maximalModularPartition <mulțimea partițiilor> $ removeNode 5 diagram
fromList [fromList [1,2],fromList [3,4]]
-}
maximalModularPartition :: Ord a
                        => Set (Partition a)
                        -> Graph a
                        -> Partition a
maximalModularPartition partitions graph
    -- Daca nu am partitii valide, intorc partitia cu toate nodurile
    | Set.null valid = Set.singleton (nodes graph)

    -- Am folosit minimumBy cu comparing Set.size ca sa aleg partitia cu cele mai putine parti
    | otherwise = minimumBy (comparing Set.size) valid
  where
    -- Am filtrat doar partitiile bune
    valid = Set.filter good partitions

    -- Am verificat sa nu fie partitia banala si sa fie modulara
    good partition =
        Set.size partition > 1 &&
        isModularPartition partition graph

{-
Obține descompunerea modulară a unui graf. O puteți utiliza pentru
a experimenta manual cu maximalModularPartition.

Exemple:

>>> modularlyDecompose diagram
fromList [fromList [1,2,3,4],fromList [5]]

>>> modularlyDecompose $ removeNode 5 diagram
fromList [fromList [1,2],fromList [3,4]]
-}
modularlyDecompose :: Ord a
                   => Graph a
                   -> Partition a
modularlyDecompose graph = maximalModularPartition partitionSet graph
  where
    parts = partitions $ Set.toList $ nodes graph
    partitionSet = Set.fromList $ map toPartition parts

toPartition :: Ord a => [[a]] -> Partition a
toPartition = Set.fromList . map Set.fromList
