module TestGraph where

import TestPP
import Data.Set (Set)
import qualified Data.Set as Set
import qualified StandardGraph as SG
import Algorithms
import AlgebraicGraph

-- algebraic graphs
algebraicTestGraph1 :: AlgebraicGraph Int
algebraicTestGraph1 = Overlay
                (Connect
                    (Node 1)
                    (Overlay (Node 2) (Node 3))
                )
                (Node 4)

algebraicTestGraph2 :: AlgebraicGraph Int
algebraicTestGraph2 = Overlay
                    (Connect (Node 1) (Node 2))
                    (Overlay
                        (Connect (Node 3) (Node 4))
                        (Overlay
                            (Connect (Node 4) (Node 5))
                            (Connect (Node 5) (Node 3))
                        )
                    )

algebraicTestGraph3 :: AlgebraicGraph Int
algebraicTestGraph3 = Overlay
                    (Connect
                        (Node 1)
                        (Overlay
                            (Node 4)
                            (Connect (Node 2) (Node 3))
                        )
                    )
                    (Connect (Node 4) (Node 1))

algebraicTestGraph4 :: AlgebraicGraph Int
algebraicTestGraph4 = Overlay
                    (Overlay
                        (Connect
                            (Node 1)
                            (Connect (Node 2) (Node 3))
                        )
                        (Connect
                            (Node 3)
                            (Connect (Node 4) (Node 5))
                        )
                    )
                    (Connect (Node 5) (Node 1))

algebraicTestGraph5 :: AlgebraicGraph Int
algebraicTestGraph5 = Overlay
                    (Overlay
                        (Overlay
                            (Connect
                                (Node 1)
                                (Overlay (Node 2) (Node 6))
                            )
                            (Overlay
                                (Connect
                                    (Node 6)
                                    (Overlay (Node 3) (Node 7))
                                )
                                (Connect
                                    (Overlay (Node 3) (Node 7))
                                    (Node 5)
                                )
                            )
                        )
                        (Connect (Node 2) (Node 3))
                    )
                    (Node 4)

algebraicTestGraph6 :: AlgebraicGraph Int
algebraicTestGraph6 = Overlay
                    (Overlay
                        (Connect
                            (Node 1)
                            (Overlay
                                (Node 2)
                                (Overlay (Node 3) (Node 4))
                            )
                        )
                        (Overlay
                            (Connect (Node 2) (Node 5))
                            (Connect (Node 3) (Node 6))
                        )
                    )
                    (Overlay
                        (Connect (Node 4) (Node 7))
                        (Connect (Node 6) (Node 8))
                    )

algebraicTestGraph7 :: AlgebraicGraph Int
algebraicTestGraph7 = Overlay
                    (Connect
                        (Node 1)
                        (Overlay
                            (Connect (Node 2) (Node 4))
                            (Node 3)
                        )
                    )
                    (Connect (Node 4) (Node 1))

standardTestGraph1 :: SG.StandardGraph Int
standardTestGraph1 = SG.fromComponents [1, 2, 3, 4] [(1, 2), (1, 3)]

standardTestGraph12 :: SG.StandardGraph Int
standardTestGraph12 = SG.fromComponents [4, 3, 3, 2, 1] [(1, 3), (1, 3), (1, 2)]

standardTestGraph2 :: SG.StandardGraph Int
standardTestGraph2 = SG.fromComponents [1, 2, 3, 4, 5] [(1, 2), (3, 4), (4, 5), (5, 3)]

standardTestGraph22 :: SG.StandardGraph Int
standardTestGraph22 = SG.fromComponents [1, 2, 3, 5, 1, 4, 4] [(1, 2), (3, 4), (4, 5), (5, 3), (3, 4), (4, 5), (5, 3)]

standardTestGraph3 :: SG.StandardGraph Int
standardTestGraph3 = SG.fromComponents [1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (2, 3), (1, 3)]

standardTestGraph32 :: SG.StandardGraph Int
standardTestGraph32 = SG.fromComponents [1, 2, 1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (1, 2), (1, 4), (2, 3), (1, 3)]

standardTestGraph4 :: SG.StandardGraph Int
standardTestGraph4 = SG.fromComponents [1, 2, 3, 4, 5] [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 1), (3, 5)]

standardTestGraph5 :: SG.StandardGraph Int
standardTestGraph5 = SG.fromComponents [1, 2, 3, 4, 5, 6, 7] [(1, 2), (2, 3), (3, 5), (1, 6), (6, 3), (6, 7), (7, 5)]

standardTestGraph6 :: SG.StandardGraph Int
standardTestGraph6 = SG.fromComponents [1, 2, 3, 4, 5, 6, 7, 8] [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 7), (6, 8)]

standardTestGraph7 :: SG.StandardGraph Int
standardTestGraph7 = SG.fromComponents [1, 2, 3, 4] [(1, 2), (1, 4), (4, 1), (2, 4), (1, 3)]

standardTestGraphSingle :: SG.StandardGraph Int
standardTestGraphSingle = SG.fromComponents [1] []

standardTestGraphLine :: SG.StandardGraph Int
standardTestGraphLine = SG.fromComponents [1,2,3,4,5] [(1, 3), (3, 2), (2, 4), (4, 5)]

standardTestForestAlone :: SG.StandardGraph Int
standardTestForestAlone = SG.fromComponents [1,2,3,4,5] [(2, 4)]

standardTestGraphMultilevel :: SG.StandardGraph Int
standardTestGraphMultilevel = SG.fromComponents [1..18] [(18, 13), (13, 2), (13, 11), (13, 6), (2, 12), (2, 4), (2, 15), (11, 10), (11, 17), (6, 16), (4, 8), (10, 1), (8, 5), (8, 9), (8, 7), (1, 3), (1, 14)]

testFoldr :: TestData
testFoldr = tests 1 15
    [
        testVal "test foldr 1"  0    $ foldr (-) 0 (Empty :: AlgebraicGraph Int),
        testVal "test foldr 2"  (-5) $ foldr (-) 10 (Node 5),

        testVal "test foldr 3"  [1] $ foldr (:) [] (Connect Empty (Node 1)),
        testVal "test foldr 4"  [1] $ foldr (:) [] (Overlay (Node 1) Empty),

        testVal "test foldr 5"  [1, 2, 3, 4]                         $ asList algebraicTestGraph1,
        testVal "test foldr 6"  [1, 2, 3, 4, 4, 5, 5, 3]             $ asList algebraicTestGraph2,
        testVal "test foldr 7"  [1, 4, 2, 3, 4, 1]                   $ asList algebraicTestGraph3,
        testVal "test foldr 8"  [1, 2, 3, 3, 4, 5, 5, 1]             $ asList algebraicTestGraph4,
        testVal "test foldr 9"  [1, 2, 6, 6, 3, 7, 3, 7, 5, 2, 3, 4] $ asList algebraicTestGraph5,
        testVal "test foldr 10" [1, 2, 3, 4, 2, 5, 3, 6, 4, 7, 6, 8] $ asList algebraicTestGraph6,
        testVal "test foldr 11" [1, 2, 4, 3, 4, 1]                   $ asList algebraicTestGraph7,

        testVal "test foldr 12" True $ null Empty,
        testVal "test foldr 13" True $ not (any null graphs),

        testVal "test foldr 14" True  $ all (3 `elem`) graphs,
        testVal "test foldr 15" True  $ not $ any (10 `elem`) graphs,

        testVal "test foldr 16" True  $ all (all (> 0)) graphs,
        testVal "test foldr 17" True  $ (not . all (all (> 3))) graphs,

        testVal "test foldr 18" [4, 8, 6, 8, 12, 12, 6]       $ map length graphs,
        testVal "test foldr 19" [10, 27, 15, 24, 49, 51, 15]  $ map sum graphs,
        testVal "test foldr 20" [4, 5, 4, 5, 7, 8, 4]         $ map maximum graphs
    ]
    where
        graphs = [algebraicTestGraph1, algebraicTestGraph2, algebraicTestGraph3, algebraicTestGraph4, algebraicTestGraph5, algebraicTestGraph6, algebraicTestGraph7]
        asList = foldr (:) []

testNodesWithFoldr :: TestData
testNodesWithFoldr = tests 2 5
    [
        testVal "test nodesWithFoldr 1" (Set.fromList [1, 2, 3, 4]) (nodesWithFoldr algebraicTestGraph1),
        testVal "test nodesWithFoldr 2" (Set.fromList [1, 2, 3, 4, 5]) (nodesWithFoldr algebraicTestGraph2),
        testVal "test nodesWithFoldr 3" (Set.fromList [1, 2, 3, 4]) (nodesWithFoldr algebraicTestGraph3),
        testVal "test nodesWithFoldr 4" (Set.fromList [1, 2, 3, 4, 5]) (nodesWithFoldr algebraicTestGraph4),
        testVal "test nodesWithFoldr 5" (Set.fromList [1, 2, 3, 4, 5, 6, 7]) (nodesWithFoldr algebraicTestGraph5),
        testVal "test nodesWithFoldr 6" (Set.fromList [1, 2, 3, 4, 5, 6, 7, 8]) (nodesWithFoldr algebraicTestGraph6),
        testVal "test nodesWithFoldr 7" (Set.fromList [1, 2, 3, 4]) (nodesWithFoldr algebraicTestGraph7)
    ]

testNodesEdges :: TestData
testNodesEdges = tests 3 20
    [
        testVal "test nodesEdges 1" (Set.empty, Set.empty)                     $ nodesEdges (Empty :: AlgebraicGraph Int),
        testVal "test nodesEdges 2" (Set.singleton 1, Set.empty)               $ nodesEdges (Node 1),

        testVal "test nodesEdges 3" (Set.fromList [1, 2], Set.empty)                $ nodesEdges (Overlay (Node 1) (Node 2)),
        testVal "test nodesEdges 4" (Set.fromList [1, 2], Set.fromList [(1, 2)])    $ nodesEdges (Connect (Node 1) (Node 2)),

        testVal "test nodesEdges 5" expectedNodeSets $ map (fst . nodesEdges) graphs,
        testVal "test nodesEdges 6" expectedEdgeSets $ map (snd . nodesEdges) graphs
    ]
  where
    graphs = [algebraicTestGraph1, algebraicTestGraph2, algebraicTestGraph3, algebraicTestGraph4, algebraicTestGraph5, algebraicTestGraph6, algebraicTestGraph7]
    expectedNodeSets =
        [ Set.fromList [1, 2, 3, 4]
        , Set.fromList [1, 2, 3, 4, 5]
        , Set.fromList [1, 2, 3, 4]
        , Set.fromList [1, 2, 3, 4, 5]
        , Set.fromList [1, 2, 3, 4, 5, 6, 7]
        , Set.fromList [1, 2, 3, 4, 5, 6, 7, 8]
        , Set.fromList [1, 2, 3, 4]
        ]
    expectedEdgeSets =
        [ Set.fromList [(1, 2), (1, 3)]
        , Set.fromList [(1, 2), (3, 4), (4, 5), (5, 3)]
        , Set.fromList [(1, 2), (1, 3), (1, 4), (2, 3), (4, 1)]
        , Set.fromList [(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (5, 1)]
        , Set.fromList [(1, 2), (1, 6), (2, 3), (3, 5), (6, 3), (6, 7), (7, 5)]
        , Set.fromList [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 7), (6, 8)]
        , Set.fromList [(1, 2), (1, 3), (1, 4), (2, 4), (4, 1)]
        ]

testNodes :: TestData
testNodes = tests 4 15
    [
        testVal "test nodes 1" (Set.fromList [1, 2, 3, 4]) (nodes algebraicTestGraph1),
        testVal "test nodes 2" (Set.fromList [1, 2, 3, 4, 5]) (nodes algebraicTestGraph2),
        testVal "test nodes 3" (Set.fromList [1, 2, 3, 4]) (nodes algebraicTestGraph3),
        testVal "test nodes 4" (Set.fromList [1, 2, 3, 4,5 ]) (nodes algebraicTestGraph4),
        testVal "test nodes 5" (Set.fromList [1, 2, 3, 4, 5, 6, 7]) (nodes algebraicTestGraph5),
        testVal "test nodes 6" (Set.fromList [1, 2, 3, 4, 5, 6, 7, 8]) (nodes algebraicTestGraph6),
        testVal "test nodes 7" (Set.fromList [1, 2, 3, 4]) (nodes algebraicTestGraph7)
    ]

testIsNode :: TestData
testIsNode = tests 5 15
    [
        testVal "test isNode 1" [True, True, True, False, False, False, True, False, False, False] $ map (`isNode` algebraicTestGraph1) nodeList,
        testVal "test isNode 2" [True, True, True, True, False, False, True, False, False, False] $ map (`isNode` algebraicTestGraph2) nodeList,
        testVal "test isNode 3" [True, True, True, False, False, False, True, False, False, False] $ map (`isNode` algebraicTestGraph3) nodeList,
        testVal "test isNode 4" [True, True, True, True, False, False, True, False, False, False] $ map (`isNode` algebraicTestGraph4) nodeList,
        testVal "test isNode 5" [True, True, True, True, False, False, True, False, True, True] $ map (`isNode` algebraicTestGraph5) nodeList,
        testVal "test isNode 6" [True, True, True, True, True, False, True, False, True, True] $ map (`isNode` algebraicTestGraph6) nodeList,
        testVal "test isNode 7" [True, True, True, False, False, False, True, False, False, False] $ map (`isNode` algebraicTestGraph7) nodeList
    ]
    where
        nodeList = [4, 2, 3, 5, 8, 9, 1, 10, 6, 7]

testEdges :: TestData
testEdges = tests 6 20
    [
        testVal "test edges 1" (Set.fromList [(1, 2),(1, 3)]) (edges algebraicTestGraph1),
        testVal "test edges 2" (Set.fromList [(1,2),(3,4),(4,5),(5,3)]) (edges algebraicTestGraph2),
        testVal "test edges 3" (Set.fromList [(1,2),(1,3),(1,4),(2,3),(4,1)]) (edges algebraicTestGraph3),
        testVal "test edges 4" (Set.fromList [(1,2),(1,3),(2,3),(3,4),(3,5),(4,5),(5,1)]) (edges algebraicTestGraph4),
        testVal "test edges 5" (Set.fromList [(1,2),(1,6),(2,3),(3,5),(6,3),(6,7),(7,5)]) (edges algebraicTestGraph5),
        testVal "test edges 6" (Set.fromList [(1,2),(1,3),(1,4),(2,5),(3,6),(4,7),(6,8)]) (edges algebraicTestGraph6),
        testVal "test edges 7" (Set.fromList [(1,2),(1,3),(1,4),(2,4),(4,1)]) (edges algebraicTestGraph7)
    ]

testDfsStack :: TestData
testDfsStack = tests 7 30
    [
        testVal "test dfsStack 1"  res1 (dfsStack 1 SG.tree),
        testVal "test dfsStack 2"  [4, 11, 12] (dfsStack 4 SG.tree),
        testVal "test dfsStack 3"  [1] (dfsStack 1 standardTestGraphSingle),
        testVal "test dfsStack 4"  [1, 3, 2 ,4, 5] (dfsStack 1 standardTestGraphLine),
        testVal "test dfsStack 5"  [5] (dfsStack 5 standardTestGraphLine),
        testVal "test dfsStack 6"  [3] (dfsStack 3 standardTestForestAlone),
        testVal "test dfsStack 7"  [1, 2, 3] (dfsStack 1 standardTestGraph1),
        testVal "test dfsStack 8"  [3] (dfsStack 3 standardTestGraph1),
        testVal "test dfsStack 9"  res9 (dfsStack 13 standardTestGraphMultilevel),
        testVal "test dfsStack 10" res10 (dfsStack 18 standardTestGraphMultilevel)
    ]
    where
        res1 = [1, 2, 7, 15, 8, 3, 9, 10, 4, 11, 12, 5, 13, 14, 6]
        res9 = [13, 2, 4, 8, 5, 7, 9, 12, 15, 6, 16, 11, 10, 1, 3, 14, 17]
        res10 = [18, 13, 2, 4, 8, 5, 7, 9, 12, 15, 6, 16, 11, 10, 1, 3, 14, 17]


checkAll = vmCheck $ algebraicGraph ++ algorithms
    where
        algebraicGraph =
            [ testFoldr
            , testNodesWithFoldr
            , testNodesEdges
            , testNodes
            , testIsNode
            , testEdges
            ]
        algorithms = [testDfsStack]
