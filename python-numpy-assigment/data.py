
import numpy as np

data = np.array([10,20,30,40])

mean = np.mean(data)
std = np.std(data)

normalised = (data - mean) / std

reshaped = normalised.reshape(2,2)

print('orginal data:', data)
print('mean:', round(mean,2))
print('standard deviation:', round(std,2))
print('normalised data:',np.round(normalised,2))
print('reshaped data shape:', reshaped.shape)


