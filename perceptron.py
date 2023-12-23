import numpy as np

class Perceptron :
    def __init__(self,input_vector,weights,threshold) :
        input_vector.append(1)
        self.input_vector = np.array(input_vector)
        # adding a random bias for magic
        self.bias = np.random.randint(-3,3)
        weights.append(self.bias)
        self.weights = np.array(weights)
        self.threshold = threshold

    def predict(self):
        output = np.dot(self.weights,self.input_vector)
        return 1 if output >= self.threshold else 0
    