import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Розмір гри
GRID_SIZE = 50

# Початкове значення гри
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

# Оновлення гри
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

# UI
st.title("Гра 'Життя'")

# Малювання клітини
row = st.slider("Рядок", 0, GRID_SIZE-1)
col = st.slider("Стовпець", 0, GRID_SIZE-1)
if st.button("Додати клітину"):
    st.session_state.grid[row, col] = 1

# Кнопки керування
if st.button("Старт"):
    st.session_state.running = True
if st.button("Зупинити"):
    st.session_state.running = False
if st.button("Очистити"):
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Гра у реальному часі
if st.session_state.running:
    st.session_state.grid = update_grid(st.session_state.grid)
    time.sleep(1)
    st.rerun()

# Візуалізація
fig, ax = plt.subplots()
ax.imshow(st.session_state.grid, cmap="gray")
ax.axis("off")
st.pyplot(fig)
