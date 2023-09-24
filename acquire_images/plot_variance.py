import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Reading the CSV File
df = pd.read_csv('samples_body_1.csv', header=None, names=['timestamp', 'fps'])

# Step 2: Calculating Mean and Variance
fps_mean = df['fps'].mean()
fps_variance = df['fps'].var()

# Step 3: Plotting the Graph
plt.figure(figsize=(10, 6))
plt.hist(df['fps'], bins=20, alpha=0.7, label='FPS Distribution', color='blue', edgecolor='black')

# Plotting mean and variance
plt.axvline(fps_mean, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {fps_mean:.2f}')
plt.axvline(fps_mean + np.sqrt(fps_variance), color='green', linestyle='dashed', linewidth=2, label=f'Mean + 1 Std Dev: {fps_mean + np.sqrt(fps_variance):.2f}')
plt.axvline(fps_mean - np.sqrt(fps_variance), color='green', linestyle='dashed', linewidth=2, label=f'Mean - 1 Std Dev: {fps_mean - np.sqrt(fps_variance):.2f}')

plt.legend()
plt.title('FPS Distribution')
plt.xlabel('FPS')
plt.ylabel('Frequency')
plt.show()
