import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Налаштування розміру гри
GRID_SIZE = 50
CELL_SIZE = 10

# Функція для створення початкового масиву
def create_grid():
    return np.random.randint(0, 2, size=(GRID_SIZE, GRID_SIZE))

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

# Streamlit UI
st.title("Гра 'Життя'")

# Початковий стан гри
if "grid" not in st.session_state:
    st.session_state.grid = create_grid()

# Кнопка для оновлення покоління
if st.button("Оновити покоління"):
    st.session_state.grid = update_grid(st.session_state.grid)

# Візуалізація гри
fig, ax = plt.subplots()
ax.imshow(st.session_state.grid, cmap="gray")
ax.axis("off")
st.pyplot(fig)

