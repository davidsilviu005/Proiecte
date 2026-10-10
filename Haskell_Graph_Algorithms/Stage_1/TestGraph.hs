module TestGraph where

import TestPP
import qualified Data.Set as Set
import StandardGraph
import Algorithms


testGraph1 :: StandardGraph Int
testGraph1 = fromComponents [1, 2, 3, 4] [(1, 2), (1, 3)]

testGraph12 :: StandardGraph Int
testGraph12 = fromComponents [4, 3, 3, 2, 1] [(1, 3), (1, 3), (1, 2)]

testGraph2 :: StandardGraph Int
testGraph2 = fromComponents [1, 2, 3, 4, 5] [(1, 2), (3, 4), (4, 5), (5, 3)]

testGraph22 :: StandardGraph Int
testGraph22 = fromComponents [1, 2, 3, 5, 1, 4, 4] [(1, 2), (3, 4), (4, 5), (5, 3), (3, 4), (4, 5), (5, 3)]

testGraph3 :: StandardGraph Int
testGraph3 = fromComponents [1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (2, 3), (1, 3)]

testGraph32 :: StandardGraph Int
testGraph32 = fromComponents [1, 2, 1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (1, 2), (1, 4), (2, 3), (1, 3)]

testGraph4 :: StandardGraph Int
testGraph4 = fromComponents [1, 2, 3, 4, 5] [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 1), (3, 5)]

testGraph5 :: StandardGraph Int
testGraph5 = fromComponents [1, 2, 3, 4, 5, 6, 7] [(1, 2), (2, 3), (3, 5), (1, 6), (6, 3), (6, 7), (7, 5)]

testGraph6 :: StandardGraph Int
testGraph6 = fromComponents [1, 2, 3, 4, 5, 6, 7, 8] [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 7), (6, 8)]

testGraph7 :: StandardGraph Int
testGraph7 = fromComponents [1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (2, 4), (1, 3)]

testGraphSingle :: StandardGraph Int
testGraphSingle = fromComponents [1] []

testGraphLine :: StandardGraph Int
testGraphLine = fromComponents [1,2,3,4,5] [(1, 3), (3, 2), (2, 4), (4, 5)]

testForestAlone :: StandardGraph Int
testForestAlone = fromComponents [1,2,3,4,5] [(2, 4)]

testGraphMultilevel :: StandardGraph Int
testGraphMultilevel = fromComponents [1..18] [(18, 13), (13, 2), (13, 11), (13, 6), (2, 12), (2, 4), (2, 15), (11, 10), (11, 17), (6, 16), (4, 8), (10, 1), (8, 5), (8, 9), (8, 7), (1, 3), (1, 14)]

testGraphConstruction :: TestData
testGraphConstruction = tests 1 3
    [
        testCond "test graph equality 1" (testGraph1 == testGraph12),
        testCond "test graph equality 2" (testGraph2 == testGraph22),
        testCond "test graph equality 3" (testGraph3 == testGraph32)
    ]

testNodes :: TestData
testNodes = tests 2 1
    [
        testVal "nodes testGraph1" (Set.fromList [1,2,3,4]) (nodes testGraph1),
        testVal "nodes testGraph2" (Set.fromList [1,2,3,4]) (nodes testGraph12),
        testVal "nodes testGraph3" (Set.fromList [1,2,3,4,5]) (nodes testGraph22),
        testVal "nodes testGraph4" (Set.fromList [1,2,3,4]) (nodes testGraph3),
        testVal "nodes testGraph5" (Set.fromList [1,2,3,4,5,6,7]) (nodes testGraph5),
        testVal "nodes testGraph6" (Set.fromList [1,2,3,4,5,6,7,8]) (nodes testGraph6)
    ]

testEdges :: TestData
testEdges = tests 3 1
    [
        testVal "edges testGraph1" (Set.fromList [(1,2),(1,3)]) (edges testGraph1),
        testVal "edges testGraph2" (Set.fromList [(1,2),(1,3)]) (edges testGraph12),
        testVal "edges testGraph3" (Set.fromList [(1,2),(3,4),(4,5),(5,3)]) (edges testGraph2),
        testVal "edges testGraph4" (Set.fromList [(1,2),(1,3),(2,3),(3,4),(3,5),(4,5),(5,1)]) (edges testGraph4),
        testVal "edges testGraph5" (Set.fromList [(1,2),(1,6),(2,3),(3,5),(6,3),(6,7),(7,5)]) (edges testGraph5),
        testVal "edges testGraph6" (Set.fromList [(1,2),(1,3),(1,4),(2,4),(4,1)]) (edges testGraph7)
    ]

testOutNeighbors :: TestData
testOutNeighbors = tests 4 10
    [
        testVal "test outNeighbors 1" (Set.fromList [2, 3]) (outNeighbors 1 testGraph1),
        testVal "test outNeighbors 2" (Set.fromList []) (outNeighbors 3 testGraph1),
        testVal "test outNeighbors 3" (Set.fromList [5]) (outNeighbors 4 testGraph2),
        testVal "test outNeighbors 4" (Set.fromList [2, 3, 4]) (outNeighbors 1 testGraph3),
        testVal "test outNeighbors 5" (Set.fromList []) (outNeighbors 3 testGraph3),
        testVal "test outNeighbors 6" (Set.fromList [2, 6]) (outNeighbors 1 testGraph5)
    ]

testInNeighbors :: TestData
testInNeighbors = tests 5 10
    [
        testVal "test inNeighbors 1" (Set.fromList []) (inNeighbors 1 testGraph1),
        testVal "test inNeighbors 2" (Set.fromList [1]) (inNeighbors 3 testGraph1),
        testVal "test inNeighbors 3" (Set.fromList [3]) (inNeighbors 4 testGraph2),
        testVal "test inNeighbors 4" (Set.fromList [4]) (inNeighbors 1 testGraph3),
        testVal "test inNeighbors 5" (Set.fromList [1, 2]) (inNeighbors 3 testGraph3),
        testVal "test inNeighbors 6" (Set.fromList [5]) (inNeighbors 1 testGraph4)
    ]

testRemoveNode :: TestData
testRemoveNode = tests 6 15
    [
        testVal "test removeNode 1" res1 (removeNode 1 testGraph1),
        testVal "test removeNode 2" res2 (removeNode 3 testGraph1),
        testVal "test removeNode 3" res3 (removeNode 4 testGraph2),
        testVal "test removeNode 4" res4 (removeNode 2 testGraph3),
        testVal "test removeNode 5" res5 (removeNode 1 testGraph3),
        testVal "test removeNode 6" res6 (removeNode 5 testGraph4)
    ]
    where
        res1 = fromComponents [2, 3, 4] []
        res2 = fromComponents [1, 2, 4] [(1, 2)]
        res3 = fromComponents [1, 2, 3, 5] [(1, 2), (5, 3)]
        res4 = fromComponents [1, 3, 4] [(1, 4), (4, 1), (1, 3)]
        res5 = fromComponents [2, 3, 4] [(2, 3)]
        res6 = fromComponents [1, 2, 3, 4] [(1, 2), (1, 3), (2, 3), (3, 4)]


testSplitNode :: TestData
testSplitNode = tests 7 20
    [
        testVal "test splitNode 1" res1 (splitNode 1 (Set.fromList [5, 6, 7]) testGraph1),
        testVal "test splitNode 2" res2 (splitNode 4 (Set.fromList [5, 6]) testGraph1),
        testVal "test splitNode 3" res3 (splitNode 3 (Set.fromList [6, 7]) testGraph2),
        testVal "test splitNode 4" res4 (splitNode 2 Set.empty testGraph3),
        testVal "test splitNode 5" res5 (splitNode 3 (Set.fromList [5, 6]) testGraph3),
        testVal "test splitNode 6" res6 (splitNode 5 (Set.fromList [7]) testGraph4)
    ]
    where
        res1 = fromComponents [5, 6, 7, 2, 3, 4] [(5, 2), (5, 3), (6, 2), (6, 3), (7, 2), (7, 3)]
        res2 = fromComponents [1, 2, 3, 5, 6] [(1, 2), (1, 3)]
        res3 = fromComponents [1, 2, 6, 7, 4, 5] [(1, 2), (6, 4), (7, 4), (4, 5), (5, 6), (5, 7)]
        res4 = fromComponents [1, 3, 4] [(1, 4), (4, 1), (1, 3)]
        res5 = fromComponents [1, 2, 4, 5, 6] [(1, 2), (1, 4), (4, 1), (2, 5), (2, 6), (1, 5), (1, 6)]
        res6 = fromComponents [1, 2, 3, 4, 7] [(1, 2), (1, 3), (2, 3), (3, 4), (4, 7), (7, 1), (3, 7)]


testMergeNodes :: TestData
testMergeNodes = tests 8 15
    [
        testVal "test mergeNodes 1" res1 (mergeNodes (\x -> elem x [2, 3]) 5 testGraph1),
        testVal "test mergeNodes 2" res2 (mergeNodes (\x -> elem x [1, 2]) 5 testGraph1),
        testVal "test mergeNodes 3" res3 (mergeNodes (\x -> elem x []) 7 testGraph2),
        testVal "test mergeNodes 4" res4 (mergeNodes (\x -> elem x [1, 2, 3]) 5 testGraph3),
        testVal "test mergeNodes 5" res5 (mergeNodes (\x -> elem x [1, 4]) 5 testGraph3),
        testVal "test mergeNodes 6" res6 (mergeNodes (\x -> elem x [1, 2, 3]) 6 testGraph4)
    ]
    where
        res1 = fromComponents [1, 4, 5] [(1,5)]
        res2 = fromComponents [3, 4, 5] [(5,3),(5,5)]
        res3 = fromComponents [1, 2, 3, 4, 5] [(1, 2), (3, 4), (4, 5), (5, 3)]
        res4 = fromComponents [4,5] [(4,5),(5,4),(5,5)]
        res5 = fromComponents [2,3,5] [(2,3),(5,2),(5,3),(5,5)]
        res6 = fromComponents [4,5,6] [(4,5),(5,6),(6,4),(6,5),(6,6)]


testBFS :: TestData
testBFS = tests 9 15
    [
        testVal "test bfs 1"  [1] (bfs 1 testGraphSingle),
        testVal "test bfs 2"  [1, 2, 3] (bfs 1 testGraph1),
        testVal "test bfs 3"  [3] (bfs 3 testGraph1),
        testVal "test bfs 4"  [1, 3, 2, 4, 5] (bfs 1 testGraphLine),
        testVal "test bfs 5"  [5] (bfs 5 testGraphLine),
        testVal "test bfs 6"  [2, 4] (bfs 2 testForestAlone),
        testVal "test bfs 7"  [1, 2, 3, 4, 5, 6, 7, 8] (bfs 1 testGraph6),
        testVal "test bfs 8"  res8 (bfs 1 tree),
        testVal "test bfs 9"  res9 (bfs 13 testGraphMultilevel),
        testVal "test bfs 10" res10 (bfs 18 testGraphMultilevel)
    ]
    where
        res8 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        res9 = [13, 2, 6, 11, 4, 12, 15, 16, 10, 17, 8, 1, 5, 7, 9, 3, 14]
        res10 = [18, 13, 2, 6, 11, 4, 12, 15, 16, 10, 17, 8, 1, 5, 7, 9, 3, 14]


testDFS :: TestData
testDFS = tests 10 15
    [
        testVal "test dfs 1"  res1 (dfs 1 tree),
        testVal "test dfs 2"  [4, 11, 12] (dfs 4 tree),
        testVal "test dfs 3"  [1] (dfs 1 testGraphSingle),
        testVal "test dfs 4"  [1, 3, 2 ,4, 5] (dfs 1 testGraphLine),
        testVal "test dfs 5"  [5] (dfs 5 testGraphLine),
        testVal "test dfs 6"  [3] (dfs 3 testForestAlone),
        testVal "test dfs 7"  [1, 2, 3] (dfs 1 testGraph1),
        testVal "test dfs 8"  [3] (dfs 3 testGraph1),
        testVal "test dfs 9"  res9 (dfs 13 testGraphMultilevel),
        testVal "test dfs 10" res10 (dfs 18 testGraphMultilevel)
    ]
    where
        res1 = [1, 2, 7, 15, 8, 3, 9, 10, 4, 11, 12, 5, 13, 14, 6]
        res9 = [13, 2, 4, 8, 5, 7, 9, 12, 15, 6, 16, 11, 10, 1, 3, 14, 17]
        res10 = [18, 13, 2, 4, 8, 5, 7, 9, 12, 15, 6, 16, 11, 10, 1, 3, 14, 17]


testCountIntermediate :: TestData
testCountIntermediate = tests 11 15
    [
        testVal "test countIntermediate 1" (Just (1, 1)) (countIntermediate 1 3 testGraph1),
        testVal "test countIntermediate 2" (Just (0, 0)) (countIntermediate 1 2 testGraph1),
        testVal "test countIntermediate 3" (Just (3, 3)) (countIntermediate 1 5 testGraphLine),
        testVal "test countIntermediate 4" (Just (6, 4)) (countIntermediate 1 8 testGraph6),
        testVal "test countIntermediate 5" Nothing (countIntermediate 3 1 testGraph1),
        testVal "test countIntermediate 6" Nothing (countIntermediate 5 1 testGraphLine),
        testVal "test countIntermediate 7" Nothing (countIntermediate 2 1 testGraph2),
        testVal "test countIntermediate 8" (Just (9, 8)) (countIntermediate 1 11 tree),
        testVal "test countIntermediate 9" (Just (12, 12)) (countIntermediate 1 14 tree),
        testVal "test countIntermediate 10" (Just (16, 15)) (countIntermediate 18 14 testGraphMultilevel)
    ]

checkAll :: IO ()
checkAll = vmCheck $ standardGraph ++ algorithms
    where
        standardGraph =
            [ testGraphConstruction
            , testNodes
            , testEdges
            , testOutNeighbors
            , testInNeighbors
            , testRemoveNode
            , testSplitNode
            , testMergeNodes
            ]
        algorithms =
            [ testBFS
            , testDFS
            , testCountIntermediate
            ]
