import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            total = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            if grid[i, j] == 1 and total in [2, 3]:
                new_grid[i, j] = 1
            elif grid[i, j] == 0 and total == 3:
                new_grid[i, j] = 1
    return new_grid

def draw_grid(grid):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap="gray")
    ax.axis("off")
    return fig

# UI
st.title("Моделювання клітинної автоматизації")
grid_size = st.slider("Розмір сітки", min_value=10, max_value=500, value=100)
iterations = st.slider("Кількість ітерацій", min_value=1, max_value=50, value=10)

grid = np.random.choice([0, 1], size=(grid_size, grid_size))

for i in range(iterations):
    grid = update_grid(grid)

st.pyplot(draw_grid(grid))
