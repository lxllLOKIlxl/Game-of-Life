import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 50  # Розмір поля
UPDATE_INTERVAL = 0.5  # Час оновлення гри

# Початкове значення (чисте поле)
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
if "running" not in st.session_state:
    st.session_state.running = False

# Функція для отримання сусідів
def count_neighbors(grid, x, y):
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    return sum(grid[(x+i)%GRID_SIZE, (y+j)%GRID_SIZE] for i, j in neighbors)

# Функція для генерації нового покоління
def update_grid(grid):
    new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1 and (neighbors == 2 or neighbors == 3):
                new_grid[x, y] = 1
            elif grid[x, y] == 0 and neighbors == 3:
                new_grid[x, y] = 1
    return new_grid

# Функція для створення **маленького випадкового узору**
def generate_random_pattern():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    num_cells = np.random.randint(5, 15)  # Кількість живих клітин (5–15)
    for _ in range(num_cells):
        x, y = np.random.randint(0, GRID_SIZE, size=2)
        grid[x, y] = 1
    return grid

# UI Streamlit
st.title("Гра 'Життя'")

# Малювання клітин
st.write("**Намалюй живі клітини вручну:**")
row = st.slider("Рядок", 0, GRID_SIZE-1)
col = st.slider("Стовпець", 0, GRID_SIZE-1)
if st.button("Додати клітину"):
    st.session_state.grid[row, col] = 1

# Кнопки керування
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Старт / Зупинити"):
        st.session_state.running = not st.session_state.running
with col2:
    if st.button("Очистити"):
        st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
with col3:
    if st.button("Рандомний узор"):
        st.session_state.grid = generate_random_pattern()

# Генерація у реальному часі
if st.session_state.running:
    st.session_state.grid = update_grid(st.session_state.grid)

# Візуалізація (тепер чорні живі клітини видно правильно)
fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(st.session_state.grid, cmap="gray_r", interpolation="nearest")
ax.axis("off")
st.pyplot(fig)

