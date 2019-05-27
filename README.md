# Имплементация алгоритма Дейкстры с использованием Фибоначчиевых куч

## Постановка задачи:

Реализовать алгоритм для поиска оптимального пути во взвешенном неориентированном графе.

## Решение:
1. Пусть G - граф, V - множество его вершин, n = |V|
2. Пронумеруем вершины графа от 1 до n.
3. Граф неориентированный - матрица смежности симметрична
4. Посчитаем оптимальный путь алгоритмом Дейкстры

## Пример использования:

```python
from tree import Graph, AlgorithmDijkstra

graph = Graph(n, edges)
algo = AlgorithmDijkstra()
distances = algo.solve(graph, s)
```

## Использованная литература

> Michael L. Fredman and Robert Endre Tarjan. 1987. Fibonacci heaps and their uses in improved network optimization algorithms. J. ACM 34, 3 (July 1987), 596-615. DOI: https://doi.org/10.1145/28869.28874

```
MICHAEL L. FREDMAN
University of California, San Diego, La Jolla, California
AND
ROBERT ENDRE TARJAN
AT&T Bell Laboratories, Murray Hill, New Jersey
```

Сделано для компании Bell Integrator

Лицензия MIT
