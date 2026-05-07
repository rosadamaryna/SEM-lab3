import itertools

class KnapsackSolver:
    def __init__(self, weights, values, capacity):
        # Ініціалізація основних параметрів задачі
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.n = len(weights)

    def brute_force(self):
        # Метод повного перебору комбінацій
        best_value = 0
        best_combination = []

        # r - кількість предметів у підмножині (від 0 до n)
        for r in range(self.n + 1):
            # Генеруємо всі можливі комбінації індексів для поточної кількості r
            for indices in itertools.combinations(range(self.n), r):
                w_sum = sum(self.weights[i] for i in indices)
                v_sum = sum(self.values[i] for i in indices)

                # Якщо комбінація підходить по вазі і краща за попередню
                if w_sum <= self.capacity and v_sum > best_value:
                    best_value = v_sum
                    # Зберігаємо ID предметів (індекс + 1)
                    best_combination = [i + 1 for i in indices]

        return best_value, best_combination

    def solve_recursive(self, n=None, cap=None):
        # Рекурсивна функція (брати чи не брати предмет)
        if n is None: n = self.n
        if cap is None: cap = self.capacity

        # Вихід з рекурсії: якщо закінчилися предмети або місткість рюкзака
        if n == 0 or cap == 0:
            return 0

        # Якщо предмет не влізає — йдемо до наступного
        if self.weights[n - 1] > cap:
            return self.solve_recursive(n - 1, cap)

        # Повертаємо максимум між варіантами з предметом та без нього
        return max(
            self.values[n - 1] + self.solve_recursive(n - 1, cap - self.weights[n - 1]),
            self.solve_recursive(n - 1, cap)
        )