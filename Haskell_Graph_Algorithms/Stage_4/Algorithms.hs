module Algorithms where

import StandardGraph
import Data.Set (Set)
import qualified Data.Set as Set
import Debug.Trace
import qualified Control.Applicative as Set

type Graph a = StandardGraph a

{-
*** TODO 7 (30p) ***

Utilizând equational reasoning, rafinați implementarea dfs din etapa 1
pentru a obține implementarea eficientă bazată pe o stivă.

Pentru aceasta, generalizați funcția internă folosită în etapa 1 (să o numim
search), astfel încât să ia ca parametru nu doar nodul curent din care începe
parcurgerea, ci o listă de noduri (să numim noua funcție searchList). Mai
precis, impuneți proprietatea:

searchList :: Ord a => [a] -> [a]
searchList nodes = concatMap search nodes,

de unde rezultă că

search node = searchList [node].

De aici, derivați o nouă definiție mai eficientă pentru searchList, abordând
cazul de bază și cazul general.

DERIVARE: ...

{-
DERIVARE dfsStack:

Proprietati:
(1) searchList nodes = concatMap search nodes
(2) search node = searchList [node]

1. Cazul de baza:
Aici aplicam direct proprietatea (1) pe o listă vida. Deoarece `concatMap` pe o lista vida intoarce mereu o lista vida, evaluarea se face direct
pentru a opri recursivitatea.
searchList visited []
= concatMap search []
= []

2. Cazul recursiv:
searchList visited nodes
= searchList visited (x:xs)
= search x ++ concatMap search xs
= searchList visited [x] ++ searchList visited xs
=> Set.member x visited == True  -> searchList visited xs
=> Set.member x visited == False -> x : searchList (Set.insert x visited) (Set.toList (outNeighbors x graph) ++ xs)
-}

Exemple:

>>> dfsStack 1 tree
[1,2,7,15,8,3,9,10,4,11,12,5,13,14,6]

>>> dfsStack 4 tree
[4,11,12]
-}
dfsStack :: Ord a => a -> Graph a -> [a]
dfsStack node graph = searchList mempty [node]
    where
        -- Am pornit searchList cu Set gol si cu nodul initial in stiva
        searchList _ [] = []

        -- Am folosit lista ca stiva, primul element fiind nodul curent
        searchList visited (x : xs)
            -- Am folosit Set.member ca sa sar peste nodurile deja vizitate
            | Set.member x visited = searchList visited xs

            -- Am folosit Set.insert pentru vizitat si pun vecinii in fata stivei
            | otherwise = x : searchList (Set.insert x visited) (Set.toList (outNeighbors x graph) ++ xs)

{-
DEBUG

Funcții pentru debugging, care afișează un mesaj DEBUG de fiecare dată când
un element este implicat într-o operație de concatenare.

La fel ca (++), appendDebug este asociativă la dreapta în expresii de forma:

xs `appendDebug` ys `appendDebug` zs.

De exemplu, expresiile echivalente asociate la dreapta

[1,2] `appendDebug` ([3] `appendDebug` [4,5,6])
[1,2] `appendDebug`  [3] `appendDebug` [4,5,6]   (implicit la dreapta)

afișează utilizări unice ale elementelor:

[
DEBUG: 1
1,
DEBUG: 2
2,
DEBUG: 3
3,4,5,6],

în timp ce asocierea la stânga

([1,2] `appendDebug` [3]) `appendDebug` [4,5,6]

necesită utilizări repetate ale elementelor:

[
DEBUG: 1

DEBUG: 1
1,
DEBUG: 2

DEBUG: 2
2,
DEBUG: 3
3,4,5,6]
-}
infixr 5 `appendDebug`
appendDebug :: Show a => [a] -> [a] -> [a]
appendDebug xs ys = foldr (\x -> (trace ("\nDEBUG: " ++ show x) x :)) ys xs

concatMapDebug :: Show b => (a -> [b]) -> [a] -> [b]
concatMapDebug f = foldr (appendDebug . f) []
