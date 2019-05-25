"""
FibonacciHeap - Фибоначчиева куча
"""

from sys import maxsize


class FibonacciHeap:
    """
    Фибоначчиева куча
    """
    # значение ключа, при котором элемент становится минимальным
    MINUS_INF = -maxsize + 1

    class Node:
        def __init__(self, x, key):
            # Содержимое узла
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
            # Ранг узла = кол-во потомков
            self.rank = 0
            # Флаг отметки
            self.marked = False

        def unlink(self):
            """
            Удаление связей перед переносом узла
            """
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """
        Создание новой фибоначчиевой кучи

        Время работы: O(1)
        """
        self.min_node = None

    def insert(self, node):
        """
        Вставка узла node

        Время работы: O(1)
        """
        h2 = FibonacciHeap()
        h2.set_min(node)
        self.meld(h2)

    def set_min(self, node):
        """
        Установка указателя минимального узла

        Время работы: O(1)
        """
        self.min_node = node

    def update_min(self, node):
        """
        Обновление минимального узла, если ключ меньше

        Время работы: O(1)
        """
        current = self.find_min()
        if not current:
            self.set_min(node)
        elif node and node.key < current.key:
            self.set_min(node)

    def find_min(self):
        """
        Поиск минимального узла

        Время работы: O(1)
        """
        return self.min_node

    def meld(self, h):
        """
        Объединение двух фибоначчиевых куч

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
        if node2.key < node1.key:
            self.set_min(node2)

    def delete_min(self):
        """
        Извлечение минимального узла

        Амортизированное время работы: O(log n)
           x
         / | \
        c1 c2 c3
        """
        root = self.find_min()
        # Удаляем из списка минимальный узел
        self.unlink(root)
        # Устанавливаем временно минимальный узел на левый
        self.set_min(root.left)
        child = root.child
        while child:
            prev = child
            child = child.right
            prev.unlink()
            self.insert(prev)
        self._consolidate()
        return root

    def unlink(self, node):
        """
        Извлечение узла из двухсвязного списка

        left - node - right = left - right
        """
        left = node.left
        right = node.right

        # В списке 1 элемент - удаляемый
        if not left:
            return

        if left == right:
            # В списке было 2 элемента
            left.left = left.right = None
        else:
            left.right = right
            right.left = left

    def _consolidate(self):
        """
        Уплотнение списка корней - склеивание деревьев с одинаковым рангом

        Обновляет указатель на минимальный узел
        Время работы: O(log n)
        """
        # временный минимальный узел
        root = self.find_min()
        if not root:
            return

        # Словарь корневых узлов вида ранг -> узел
        ranked = dict()
        ranked[root.rank] = root
        node = root.right

        while node and node != root:
            melded = node
            while melded.rank in ranked:
                # В списке корней есть дерево с таким же рангом. Склеиваем
                melded = self._link(melded, ranked[melded.rank])
            ranked[melded.rank] = melded
            # Обновляем минимальный узел
            self.update_min(melded)
            node = node.right

    def _link(self, node1, node2):
        """
        Склеивание двух корней

        Корнем становится узел с меньшим ключом, второй - его потомком
        Время работы: O(log n)
        """
        pass

    def decrease_key(self, node, key):
        """
        Уменьшение ключа узла node до значения key

        Время работы: O(1)
        """
        pass

    def _cut(self, x, y):
        """
        Подрезка дерева - перенос x из числа потомков y в список корней

        Время работы: O(1)
        """
        pass

    def _cascading_cut(self, y):
        """
        Подрезка дерева от узла y до его корня

        Время работы: O(1)
        """
        pass

    def delete(self, x):
        """
        Удаление узла x

        Амортизированное время работы: O(log n)
        """
        pass
