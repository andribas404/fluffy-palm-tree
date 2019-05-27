# -*- coding: utf-8 -*-
"""
class FibonacciHeap - Фибоначчиева куча.
class Graph - Граф с вершинами и ребрами.
class AlgorithmDijkstra - Реализация алгоритма Дейкстры.
"""


class FibonacciHeap:
    """
    Фибоначчиева куча.
    """

    class Node:
        def __init__(self, x, key):
            # Содержимое узла.
            self.x = x
            # Ключ
            self.key = key
            # Предок узла
            self.parent = None
            # Левый братский / сестринский узел
            self.left = None
            # Правый братский / сестринский узел
            self.right = None
            # Прямой потомок узла
            self.child = None
            # Ранг узла = кол-во прямых потомков
            self.rank = 0
            # Перемещались ли ранее потомки этого узла
            self.marked = False

        def _extract(self):
            """
            Удаление связей перед переносом узла.
            """
            self.parent = None
            self.left = None
            self.right = None

        def __repr__(self):
            return 'Node(x={})'.format(self.x)

    def __init__(self, node=None):
        """
        Создание новой фибоначчиевой кучи

        Время работы: O(1)
        """
        self.min_node = node

    def insert(self, node):
        """
        Вставка узла node в список корневых узлов.

        Время работы: O(1)
        """
        h2 = FibonacciHeap()
        h2._set_min(node)
        self.meld(h2)

    def _set_min(self, node):
        """
        Установка минимального узла.

        Время работы: O(1)
        """
        self.min_node = node

    def _update_min(self, node):
        """
        Обновление минимального узла, если ключ меньше.

        Время работы: O(1)
        """
        current = self.find_min()
        if not current:
            self._set_min(node)
        elif node and node.key <= current.key:
            self._set_min(node)

    def find_min(self):
        """
        Поиск минимального узла.

        Время работы: O(1)
        """
        return self.min_node

    def meld(self, h):
        """
        Объединение двух фибоначчиевых куч.

        Время работы: O(1)
        """
        node1 = self.find_min()
        node2 = h.find_min()
        # Склеивание двух двусвязных списков (колец)
        # x - удаляемая связь
        # left1 <-x node1 -> right1
        #       X
        # left2 <-x node2 -> right2

        # Добавляемая куча пуста
        if not node2:
            return

        # Исходная куча пуста
        if not node1:
            self._set_min(node2)
            return

        # Поскольку список двусвязный кольцевой, то если есть левый узел,
        # то существует правый (равен левому или другому)
        # Если в списке 1 элемент, то он не указывает сам на себя = None
        left1 = node1.left
        left2 = node2.left

        # В исходной куче 1 корневой узел
        if not left1:
            if left2:
                # По левому узлу второй кучи
                #      node1
                #   |        |
                # left2 <-x node2
                node1.left = left2
                node1.right = node2
                left2.right = node1
                node2.left = node1
            else:
                # В обеих кучах 1 корневой узел
                # node1
                #   |
                # node2
                node1.left = node1.right = node2
                node2.left = node2.right = node1
        else:
            # Склеиваем через левый корневой узел второй кучи
            if left2:
                # left1 <-x node1
                #        X
                # left2 <-x node2
                # наискосок
                left1.right = node2
                node1.left = left2
                left2.right = node1
                node2.left = left1
            # Во второй куче 1 корневой узел
            else:
                # left1 <-x node1
                #   |        |
                #      node2
                node2.left = left1
                node2.right = node1
                left1.right = node2
                node1.left = node2

        # Если нужно, обновляем минимум
        self._update_min(node2)

    def delete_min(self):
        """
        Извлечение минимального узла.

           x
         / | \
        c1 c2 c3
        Амортизированное время работы: O(log n)
        """
        root = self.find_min()
        if not root:
            raise ValueError('Куча пуста')
        # Устанавливаем временно минимальный узел на левый
        self._set_min(root.left)
        # Удаляем из списка минимальный узел
        self._unlink(root)
        # Создаем новую кучу из потомков root (у них прежний parent)
        h = FibonacciHeap(root.child)
        self.meld(h)
        self._consolidate()
        root._extract()
        root.child = None
        return root

    def _unlink(self, node):
        """
        Извлечение узла из двухсвязного списка.

        Возвращает левый узел из оставшихся в списке, либо None
        left - node - right = left - right
        Время работы: O(1)
        """
        left = node.left
        right = node.right

        # В списке 1 элемент - удаляемый
        if not left:
            return None

        if left == right:
            # В списке было 2 элемента
            left.left = left.right = None
        else:
            left.right = right
            right.left = left

        return left

    def _consolidate(self):
        """
        Уплотнение списка корней - склеивание деревьев с одинаковым рангом.

        Обновляет минимальный узел
        и устанавливает parent=None для всех корневых узлов
        Время работы: O(log n)
        """
        # временный минимальный узел
        root = self.find_min()
        if not root:
            return

        # Словарь корневых узлов вида ранг -> узел
        ranked = dict()
        ranked[root.rank] = root
        root.parent = None
        node = root.right

        while node:
            # У корня нет предков
            node.parent = None
            # Текущий узел
            melded = node
            # Следующий просматриваемый узел
            node = node.right
            if ranked.get(node.rank, None) == node:
                # Мы там уже были, поэтому эта итерация последняя
                node = None

            while melded.rank in ranked:
                # В списке корней есть дерево с таким же рангом.
                rank = melded.rank
                # Склеиваем
                melded = self._link(melded, ranked[rank])
                # и удаляем из словаря прежний ранг
                del ranked[rank]
            # обновляем с новым значением ранга получившееся дерево
            ranked[melded.rank] = melded
            # Обновляем минимальный узел
            self._update_min(melded)

    def _link(self, node1, node2):
        """
        Склеивание двух корней.

        Корнем становится узел с меньшим ключом, второй - его потомком
        Возвращает получившийся корень
        Время работы: O(1)
        """
        if node1.key > node2.key:
            node1, node2 = node2, node1
        # node1              node1
        #   |    ->            |
        # child      node2 - child

        # node2 извлекается из списка корней
        self._unlink(node2)
        node2._extract()
        # убирается отметка
        node2.marked = False
        # и он становится потомком node1
        node2.parent = node1
        # Обновляем ранг получившегося дерева
        node1.rank += 1

        # Потомок первого корня
        child = node1.child
        if not child:
            # Если нет потомков
            node1.child = node2
        else:
            left = child.left
            if not left:
                # Один потомок
                # child - node2
                child.left = child.right = node2
                node2.left = node2.right = child
            else:
                # left <-x child
                #   |        |
                #      node2
                node2.left = left
                node2.right = child
                left.right = node2
                child.left = node2

        return node1

    def decrease_key(self, node, newkey):
        """
        Уменьшение ключа узла node до значения newkey.

        Время работы: O(1)
        """
        assert newkey < node.key
        node.key = newkey

        if not node.parent:
            # Узел - корневой
            self._update_min(node)
            return

        parent = node.parent
        parent.rank -= 1
        parent.child = self._unlink(node)
        self._cascading_cut(parent)
        node._extract()
        self.insert(node)

    def _cut(self, node):
        """
        Подрезка дерева - перенос node в список корней.

        Время работы: O(1)
        """
        assert node is not None
        parent = node.parent
        if not parent:
            # Узел уже корневой
            return
        parent.rank -= 1
        parent.child = self._unlink(node)
        node._extract()
        self.insert(node)

    def _cascading_cut(self, node):
        """
        Каскадная подрезка дерева.

        Начиная от узла node, и пока предшествующий узел имеет отметку
        о перемещении (marked = True), все они становятся корневыми.

        Время работы: O(log n)
        """
        parent = node
        while parent:
            if not parent.marked:
                parent.marked = True
                return
            else:
                node = parent
                parent = node.parent
                self._cut(node)

    def delete(self, node):
        """
        Удаление узла node

        Амортизированное время работы: O(log n)
        """
        if node == self.find_min():
            # Узел - минимальный
            return self.delete_min()
        parent = node.parent
        if not parent:
            # Узел - корневой
            self._unlink(node)
        else:
            parent.rank -= 1
            parent.child = self._unlink(node)
            self._cascading_cut(parent)

        h = FibonacciHeap(node.child)
        self.meld(h)
        self._consolidate()
        node._extract()
        node.child = None
        return node


class Graph:
    """
    Граф с вершинами и ребрами.
    """

    class Vertex:
        """
        Вершина графа.
        """

        def __init__(self, x):
            self.x = x
            self.edges = []

    def __init__(self, n, edges):
        """
        Инициализация графа.

        Вершины пронумерованы от 1 до n
        edges - список ребер в формате [(вершина1, вершина2, вес ребра),...]
        Полагаем, что веса неотрицательные
        """
        # self.nodes[i] = Vertex(i+1)
        self.nodes = [Graph.Vertex(x) for x in range(1, n+1)]

        for v1, v2, weight in edges:
            node1 = self.nodes[v1-1]
            node2 = self.nodes[v2-1]

            node1.edges.append((node2, weight))
            node2.edges.append((node1, weight))


class AlgorithmDijkstra:
    """
    Реализация алгоритма Дейкстры.

    Находит кратчайший путь от заданной вершины до всех других вершин графа.
    """
    class Link:
        """
        Связывает вершину исходного графа,
        соответствующий ей узел в очереди на просмотр,
        текущее расстояние до нее,
        а также предшествующую ей вершину в оптимальном маршруте
        """
        UNLABELED = 'unlabeled'
        LABELED = 'labeled'
        SCANNED = 'scanned'

        def __init__(self, v):
            self.vertex = v
            self.heap_node = None
            self.distance = None
            self.pred = None
            self.label = AlgorithmDijkstra.Link.UNLABELED

    def __init__(self):
        pass

    def solve(self, graph, start_ind):
        """
        Находит кратчайший путь от вершины с номером start_ind до всех других
        вершин графа graph.
        """
        links = [AlgorithmDijkstra.Link(v) for v in graph.nodes]

        heap = FibonacciHeap()

        heap_node = FibonacciHeap.Node(start_ind, 0)
        link_start = links[start_ind - 1]
        link_start.distance = 0
        link_start.heap_node = heap_node
        link_start.label = AlgorithmDijkstra.Link.LABELED
        heap.insert(heap_node)

        while True:
            try:
                # Извлекаем из очереди вершину с минимальным расстоянием до нее
                heap_node = heap.delete_min()
                link = links[heap_node.x - 1]
                link.label = AlgorithmDijkstra.Link.SCANNED
                # Проход по всем вершинам, смежных с текущей
                for vertex, weight in link.vertex.edges:
                    # Суммарное расстояние до смежной
                    distance = link.distance + weight
                    # Индекс смежной вершины
                    vertex_ind = vertex.x
                    # Соответствующая запись в таблице связей
                    link_next = links[vertex_ind - 1]

                    if link_next.label == AlgorithmDijkstra.Link.SCANNED:
                        continue

                    if link_next.distance is None:
                        # Если ранее в этой вершине не были то добавляем ее
                        # в очередь на просмотр с ключом равным текущему
                        # расстоянию и сохраняем связь
                        heap_node = FibonacciHeap.Node(vertex_ind, distance)
                        heap.insert(heap_node)
                        link_next.heap_node = heap_node
                        link_next.distance = distance
                        link_next.pred = link.vertex.x
                        link_next.label = AlgorithmDijkstra.Link.LABELED
                    else:
                        # Вершина уже находится в очереди на просмотр
                        if distance < link_next.distance:
                            # и расстояние через текущую вершину короче
                            heap.decrease_key(link_next.heap_node, distance)
                            link_next.distance = distance
                            link_next.pred = link.vertex.x
            except ValueError:
                # Конец очереди
                break

        # Возвращаем список расстояний до вершин пропуская вершину s
        # Всего (n-1) значение. Если вершина недостижима, расстояние = -1
        distances = []
        for link in links:
            if link.vertex.x == start_ind:
                continue
            if link.distance is None:
                distances.append(-1)
            else:
                distances.append(link.distance)

        return distances
