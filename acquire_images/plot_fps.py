import matplotlib.pyplot as plt
import numpy as np


# read from test1.txt and convert to list of floats
with open('samples_1.txt', 'r') as f:
    body1_fps = f.readlines()
    for i in range(len(body1_fps)):
        body1_fps[i] = float(body1_fps[i])


with open('samples_2.txt', 'r') as f:
    body2_fps = f.readlines()
    for i in range(len(body2_fps)):
        body2_fps[i] = float(body2_fps[i])

# Create x-axis labels based on the number of samples
x_labels_body1 = np.arange(len(body1_fps))
x_labels_body2 = np.arange(len(body2_fps))

y_min = min(min(body1_fps), min(body2_fps))
y_max = max(max(body1_fps), max(body2_fps))

# Plotting the FPS for Body 1 and Body 2
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(x_labels_body1, body1_fps, 'r-', label='Body 1 FPS')
plt.xlabel('Sample')
plt.ylabel('FPS')
plt.title('FPS for Body 1')
plt.ylim(y_min, y_max)
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(x_labels_body2, body2_fps[:len(body1_fps)], 'b-', label='Body 2 FPS') 
plt.xlabel('Sample')
plt.ylabel('FPS')
plt.title('FPS for Body 2')
plt.ylim(y_min, y_max)
plt.grid(True)

plt.tight_layout()
plt.savefig('fps.png')
