import matplotlib.pyplot as plt
import numpy as np
import csv


# Read samples_body_1.csv and convert to lists of floats
with open('samples_body_1.csv', 'r') as f:
    reader = csv.reader(f)
    body1_data = list(reader)
    body1_timestamps = [float(row[0]) for row in body1_data]
    body1_fps = [float(row[1]) for row in body1_data]

# Read samples_body_2.csv and convert to lists of floats
with open('samples_body_2.csv', 'r') as f:
    reader = csv.reader(f)
    body2_data = list(reader)
    body2_timestamps = [float(row[0]) for row in body2_data]
    body2_fps = [float(row[1]) for row in body2_data]

# # read from test1.txt and convert to list of floats
# with open('samples_body_1.csv', 'r') as f:
#     body1_fps = f.readlines()
#     for i in range(len(body1_fps)):
#         body1_fps[i] = float(body1_fps[i])


# with open('samples_body_2.csv', 'r') as f:
#     body2_fps = f.readlines()
#     for i in range(len(body2_fps)):
#         body2_fps[i] = float(body2_fps[i])

# Create x-axis labels based on the number of samples
x_labels_body1 = np.arange(len(body1_fps))
x_labels_body2 = np.arange(len(body2_fps))

y_min = min(min(body1_fps), min(body2_fps))
y_max = max(max(body1_fps), max(body2_fps))


# Plotting
plt.figure(figsize=(16, 6))

# Plot for Body 1
plt.subplot(1, 2, 1)
plt.plot(body1_timestamps, body1_fps, 'r-', label='Body 1 FPS')
plt.scatter(body1_timestamps, body1_fps, color='r', marker='o')
plt.xlabel('Timestamp')
plt.ylabel('FPS')
plt.title('FPS for Body 1')
plt.ylim(y_min, y_max)
plt.grid(True)

# Plot for Body 2
plt.subplot(1, 2, 2)
plt.plot(body2_timestamps, body2_fps, 'b-', label='Body 2 FPS')
plt.scatter(body2_timestamps, body2_fps, color='b', marker='o')
plt.xlabel('Timestamp')
plt.ylabel('FPS')
plt.title('FPS for Body 2')
plt.ylim(y_min, y_max)
plt.grid(True)

plt.tight_layout()
plt.savefig('fps.png')
