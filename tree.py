# -*- coding: utf-8 -*-
"""
FibonacciHeap - Фибоначчиева куча.
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

        def extract(self):
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
        h2.set_min(node)
        self.meld(h2)

    def set_min(self, node):
        """
        Установка минимального узла.

        Время работы: O(1)
        """
        self.min_node = node

    def update_min(self, node):
        """
        Обновление минимального узла, если ключ меньше.

        Время работы: O(1)
        """
        current = self.find_min()
        if not current:
            self.set_min(node)
        elif node and node.key < current.key:
            self.set_min(node)

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
            self.set_min(node2)
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
        self.update_min(node2)

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
        # Удаляем из списка минимальный узел
        self.unlink(root)
        # Устанавливаем временно минимальный узел на левый
        self.set_min(root.left)
        # Создаем новую кучу из потомков root (у них прежний parent)
        h = FibonacciHeap(root.child)
        self.meld(h)
        self._consolidate()
        root.extract()
        return root

    def unlink(self, node):
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
            self.update_min(melded)

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
        self.unlink(node2)
        node2.extract()
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

    def decrease_key(self, node, delta):
        """
        Уменьшение ключа узла node на значение delta > 0.

        Время работы: O(1)
        """
        assert delta >= 0
        node.key = node.key - delta
        if not node.parent:
            # Узел - корневой
            self.update_min(node)
            return

        parent = node.parent
        parent.rank -= 1
        parent.child = self.unlink(node)
        node.extract()
        self.insert(node)

    def _cut(self, node):
        """
        Подрезка дерева - перенос node в список корней.

        Время работы: O(1)
        """
        assert node is not None
        # Узел уже корневой
        parent = node.parent
        if not parent:
            return
        parent.rank -= 1
        parent.child = self.unlink(node)
        node.extract()
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
            self.unlink(node)
        else:
            parent.rank -= 1
            parent.child = self.unlink(node)
            self._cascading_cut(parent)

        h = FibonacciHeap(node.child)
        self.meld(h)
        self._consolidate()
        node.extract()
        return node
