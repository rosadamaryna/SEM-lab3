import streamlit as st
import pandas as pd
import time
from solvers import KnapsackSolver

st.set_page_config(page_title="Задача про рюкзак", layout="wide")

st.title("Лабораторна робота №3 ")

# Налаштування вводу даних через сайдбар
st.sidebar.header("Вхідні дані")

# Вводимо списки текстом (дефолтні значення для нашого варіанту 26)
w_input = st.sidebar.text_input("Ваги (через кому):", "2, 4, 3, 5, 5")
v_input = st.sidebar.text_input("Ціни (через кому):", "3, 5, 4, 8, 7")

# Проста обробка вводу
try:
    weights = [int(x.strip()) for x in w_input.split(",")]
    values = [int(x.strip()) for x in v_input.split(",")]
    # Перевірка
    if len(weights) != len(values):
        st.error("Кількість ваг не відповідає кількості цін!")
        st.stop()
except ValueError:
    st.error("Помилка у форматі чисел!")
    st.stop()

# Максимальна місткість
capacity = st.sidebar.slider("Місткість (W):", 1, 50, 12)

# Вибір методу
method = st.sidebar.selectbox("Оберіть алгоритм:",
                              ["Brute Force", "Recursive", "Dynamic Programming", "Greedy", "Branch & Bound"])

# Ініціалізуємо наш об'єкт
solver = KnapsackSolver(weights, values, capacity)

# Виведемо табличку з тим, що ввели
st.write("### Поточний набір предметів")

# Створюємо датафрейм
df_view = pd.DataFrame({
    'Вага': weights,
    'Ціна': values,
    'Ефективність (v/w)': [round(v/w, 2) for v, w in zip(values, weights)]
})

# Змінюємо індексацію, щоб вона починалася з 1
df_view.index = df_view.index + 1

# Виводимо транспоновану таблицю (якщо хочеш рядками) або звичайну
st.table(df_view.T)

st.divider()

# Обробка логіки методів
if method == "Brute Force":
    res_v, res_items = solver.brute_force()
    st.success(f"Макс. цінність (повний перебір): {res_v}")
    st.write(f"ID предметів: {res_items}")

elif method == "Recursive":
    res_v = solver.solve_recursive()
    st.success(f"Результат рекурсії: {res_v}")
    st.info("Метод показує лише фінальну суму.")

elif method == "Dynamic Programming":
    st.write("### Робота динамічного програмування")

    if st.button("Покрокове заповнення"):
        t_space = st.empty()
        log_space = st.empty()

        # Цикл анімації
        for m, cur_i, cur_w in solver.solve_dp_animated():
            t_space.dataframe(pd.DataFrame(m))
            log_space.text(f"Крок: предмет {cur_i}, вага {cur_w}")
            time.sleep(0.05)

        # Фінал
        final_v, final_m, final_items = solver.solve_dp()
        st.success(f"Результат: {final_v}")
        st.write(f"Склад рюкзака: {sorted(final_items)}")
    else:
        # Звичайний вивід без кнопок
        v, m, items = solver.solve_dp()
        st.success(f"Оптимальна ціна: {v}")
        st.write(f"Предмети: {sorted(items)}")
        st.dataframe(pd.DataFrame(m))

elif method == "Greedy":
    v, items = solver.greedy_approach()
    st.success(f"Жадібний результат: {v}")
    st.write(f"Взяті предмети: {items}")
    st.warning("Може бути неточним!")

elif method == "Branch & Bound":
    v = solver.branch_and_bound()
    st.success(f"Результат (гілки та межі): {v}")

st.sidebar.markdown("---")
st.sidebar.write("Варіант №26")