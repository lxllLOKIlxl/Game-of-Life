import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 30
CELL_SIZE = 10

# Ініціалізація гри
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
if "running" not in st.session_state:
    st.session_state.running = False

# Функція для перевірки сусідів
def neighbours(x, y, grid):
    O = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
    return sum(grid[i % GRID_SIZE, j % GRID_SIZE] for i, j in O if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE)

# Функція для перевірки існування клітини
def exist(x, y, grid):
    return grid[x, y] == 1

# Функція оновлення поколінь
def update_grid(grid):
    new_grid = grid.copy()
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            N = neighbours(x, y, grid)
            if grid[x, y] == 1 and (N < 2 or N > 3):  # Загибель
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and N == 3:  # Народження
                new_grid[x, y] = 1
    
    return new_grid

# Функція для додавання нових клітин
def add_cell(x, y):
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        st.session_state.grid[x, y] = 1

# UI Streamlit
st.title("Гра 'Життя' в Streamlit")

# Малювання вручну
st.write("**Вибери координати для клітини:**")
row = st.slider("Рядок", 0, GRID_SIZE-1, format="Row: %d")
col = st.slider("Стовпець", 0, GRID_SIZE-1, format="Column: %d")
if st.button("Додати клітину"):
    add_cell(row, col)

# **Кругла кнопка "Тапалка" для старту**
if st.button("🔵 Тапалка (Старт/Стоп)"):
    st.session_state.running = not st.session_state.running

# Кнопка для очищення поля
if st.button("Очистити поле"):
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Оновлення поколінь у реальному часі
if st.session_state.running:
    st.session_state.grid = update_grid(st.session_state.grid)

# **Візуалізація гри**
fig, ax = plt.subplots(figsize=(6, 6))

ax.set_xticks(range(0, GRID_SIZE, CELL_SIZE))
ax.set_yticks(range(0, GRID_SIZE, CELL_SIZE))
ax.grid(True, color="white", linewidth=0.5)

ax.imshow(st.session_state.grid, cmap="inferno", interpolation="nearest")
ax.set_title("Живі клітини")
ax.axis("off")

st.pyplot(fig)
