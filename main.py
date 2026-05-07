import streamlit as st
import pandas as pd
from solvers import KnapsackSolver

# Налаштування сторінки
st.set_page_config(page_title="Лабораторна №3", layout="wide")

# Дані згідно варіанту №26
weights = [2, 4, 3, 5, 5]
values = [3, 5, 4, 8, 7]
capacity = 12

st.title("🎒 Задача про рюкзак (Варіант №26)")

# Створюємо об'єкт нашого класу
solver = KnapsackSolver(weights, values, capacity)

# Вибір методу збоку
st.sidebar.header("Меню")
method = st.sidebar.selectbox("Оберіть метод:", ["Brute Force", "Recursive", "Dynamic Programming"])

if method == "Brute Force":
    val, items = solver.brute_force()
    st.success(f"Результат: {val}")
    st.write(f"Предмети: {items}")

elif method == "Recursive":
    val = solver.solve_recursive()
    st.success(f"Результат: {val}")
    st.info("Рекурсія рахує лише фінальну суму.")

elif method == "Dynamic Programming":
    val, matrix, items = solver.solve_dp()
    st.success(f"Оптимальна ціна: {val}")
    st.write(f"Предмети: {sorted(items)}")

    st.subheader("Таблиця розрахунків (DP Matrix)")
    # Виводимо матрицю у вигляді таблиці
    df = pd.DataFrame(matrix)
    st.dataframe(df)