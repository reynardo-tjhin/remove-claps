import numpy as np

test = np.array([3.003523958, 2.40283502, 4.05250392])
print(test)

test = np.reshape(test, (1, test.shape[0]))
print(test)

test2 = np.array([[0.0, 0.0, 0.0]])
print(test2)