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

    def solve_dp(self):
        # Динамічне програмування: робимо таблицю (матрицю)
        # Спочатку заповнюємо все нулями
        dp = [[0] * (self.capacity + 1) for _ in range(self.n + 1)]

        for i in range(1, self.n + 1):
            for w in range(self.capacity + 1):
                # Якщо предмет влізає по вазі
                if self.weights[i - 1] <= w:
                    # Шукаємо максимум між "взяти" і "не взяти"
                    dp[i][w] = max(self.values[i - 1] + dp[i - 1][w - self.weights[i - 1]],
                                   dp[i - 1][w])
                else:
                    # Якщо не вліз - копіюємо значення зверху
                    dp[i][w] = dp[i - 1][w]

        # Тепер йдемо по таблиці назад, щоб знайти вибрані предмети
        selected_items = []
        w = self.capacity
        for i in range(self.n, 0, -1):
            # Якщо значення в клітинці змінилось - значить предмет у рюкзаку
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(i)
                w -= self.weights[i - 1]

        # Повертаємо ціну, всю таблицю і список предметів
        return dp[self.n][self.capacity], dp, selected_items