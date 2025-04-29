import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 50  # Розмір поля
UPDATE_INTERVAL = 0.5  # Оновлення кожні 0.5 секунди

# Початкове значення гри (чисте поле)
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

# Функція для оновлення поколінь
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

# UI Streamlit
st.title("Гра 'Життя'")

# Малювання клітин
st.write("**Намалюй живі клітини**:")
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
    if st.button("Рандомне поле"):
        st.session_state.grid = np.random.randint(0, 2, size=(GRID_SIZE, GRID_SIZE))

# Генерація у реальному часі без оновлення сторінки
if st.session_state.running:
    st.session_state.grid = update_grid(st.session_state.grid)

# Візуалізація (тепер поле чисте, а живі клітини чорні)
fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(st.session_state.grid, cmap="gray_r", interpolation="nearest")
ax.axis("off")
st.pyplot(fig)
