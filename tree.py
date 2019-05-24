"""
Фибоначчиева куча (англ. Fibonacci heap) — структура данных,
представляющая собой набор деревьев, упорядоченных в соответствии
со свойством неубывающей пирамиды. Фибоначчиевы кучи были введены
Майклом Фредманом и Робертом Тарьяном в 1984 году.
"""

from sys import maxsize


class FibonacciHeap:
    "Фибоначчиева куча"
    # значение ключа, при котором элемент становится минимальным
    MIN_KEY = -maxsize + 1

    def __init__(self):
        """Создание новой фибоначчиевой кучи
        Время работы: O(1)
        """
        pass

    def insert(self, x):
        """Вставка узла x
        Время работы: O(1)
        """
        pass

    def minumum(self):
        """Поиск минимального узла
        Время работы: O(1)
        """
        pass

    def union(self, h):
        """Объединение двух фибоначчиевых куч
        Время работы: O(1)
        """
        pass

    def extract_min(self):
        """Извлечение минимального узла
        Амортизированное время работы: O(log n)
        """
        pass

    def _consolidate(self):
        """Уплотнение списка корней - перенос корневых узлов в список потомков
        Время работы: O(log n)
        """
        pass

    def _link(self, y, x):
        """Перенос корня y - он становится потомком x
        Время работы: O(log n)
        """
        pass

    def decrease_key(self, x, k):
        """Уменьшение ключа x до значения k
        Время работы: O(1)
        """
        pass

    def _cut(self, x, y):
        """Подрезка дерева - перенос x из числа потомков y в список корней
        Время работы: O(1)
        """
        pass

    def _cascading_cut(self, y):
        """Подрезка дерева от узла y до его корня
        Время работы: O(1)
        """
        pass

    def delete(self, x):
        """Удаление узла x
        Амортизированное время работы: O(log n)
        """
        pass
