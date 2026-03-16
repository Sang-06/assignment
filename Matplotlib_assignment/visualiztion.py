import numpy as np
import matplotlib.pyplot as plt


epochs = list(range(1, 11))

np.random.seed(0)
loss = np.linspace(1.0, 0.2, 10) + np.random.normal(0, 0.05, 10)

plt.figure(figsize=(8,5))
plt.plot(epochs, loss, marker='o')
plt.title("Training Loss vs Epoch")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,5))
plt.scatter(epochs, loss)
plt.title("Epoch vs Loss Scatter Plot")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.show()


models = ['Model A', 'Model B', 'Model C']
accuracy = [0.85, 0.90, 0.88]

plt.figure(figsize=(8,5))
plt.bar(models, accuracy)
plt.title("Model Accuracy Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy")
plt.show()