import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 30  # Зменшене поле

# Початкове значення гри (порожнє поле)
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

# Оновлення поколінь (правильний баланс народження і смерті)
def update_grid(grid):
    new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1 and neighbors in [2, 3]:  # Виживання
                new_grid[x, y] = 1
            elif grid[x, y] == 0 and neighbors == 3:  # Народження
                new_grid[x, y] = 1
    return new_grid

# Генерація узорів (починається мінімум із 3 клітин)
def generate_random_pattern():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    num_patterns = np.random.randint(3, 6)  # Обмежена кількість стартових точок
    for _ in range(num_patterns):
        x, y = np.random.randint(1, GRID_SIZE-2, size=2)
        grid[x, y] = 1
        grid[x+1, y] = 1
        grid[x, y+1] = 1
    return grid

# UI Streamlit
st.title("Гра 'Життя'")

# Малювання вручну
st.write("**Намалюй живі клітини:**")
row = st.slider("Рядок", 0, GRID_SIZE-1)
col = st.slider("Стовпець", 0, GRID_SIZE-1)
if st.button("Додати клітину"):
    st.session_state.grid[row, col] = 1

# Кнопки керування
col1, col2, col3 = st.columns(3)
with col1:
    start_stop = st.button("Старт / Зупинити")
    if start_stop:
        st.session_state.running = not st.session_state.running
with col2:
    if st.button("Очистити"):
        st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
with col3:
    if st.button("Рандомний узор"):
        st.session_state.grid = generate_random_pattern()

# **Автоматичне оновлення поколінь без помилки**
if st.session_state.running:
    st.session_state.grid = update_grid(st.session_state.grid)
    st.session_state.running = True  # Фіксуємо помилку оновлення

# Візуалізація (тепер поле має **неонову рамку**)
fig, ax = plt.subplots(figsize=(6, 6))

# Малюємо саму рамку
ax.set_facecolor("black")  # Фон чорний для контрасту
ax.spines["top"].set_color("#ff007f")
ax.spines["right"].set_color("#ff007f")
ax.spines["bottom"].set_color("#ff007f")
ax.spines["left"].set_color("#ff007f")
ax.spines["top"].set_linewidth(5)
ax.spines["right"].set_linewidth(5)
ax.spines["bottom"].set_linewidth(5)
ax.spines["left"].set_linewidth(5)

# Малюємо саму гру
ax.imshow(st.session_state.grid, cmap="gray_r", interpolation="nearest")
ax.axis("off")
st.pyplot(fig)

