# Backpropagation in Artificial Neural Networks

Backpropagation (short for **backward propagation of errors**) is the learning algorithm that updates the weights in a neural network.  
It’s essentially how the network *learns from its mistakes*.

---

## 🔑 Steps of Backpropagation

Let’s imagine a very simple network:

**Input Layer → Hidden Layer → Output Layer**

We’ll use:
- **Forward pass** → Calculate predictions.
- **Backward pass** → Adjust weights using the error.

---

### 1. Initialize weights and biases
- Start with small random numbers for weights and biases.

### 2. Forward Pass (Prediction)
For each neuron:
1. Compute weighted sum:  
   $z = w \cdot x + b$
2. Apply activation function (e.g., sigmoid):  
   $a = \sigma(z)$

### 3. Compute Error
Loss function (Mean Squared Error):  

$$
Loss = \frac{1}{2}(y_{true} - y_{pred})^2
$$

### 4. Backward Pass
1. Output error:  
   $$
   \delta_{output} = (y_{pred} - y_{true}) \cdot \sigma'(z_{output})
   $$
2. Hidden error:  
   $$
   \delta_{hidden} = \delta_{output} \cdot w_{hidden \to output} \cdot \sigma'(z_{hidden})
   $$

### 5. Update Weights
$$
w = w - \eta \cdot \Delta w
$$

$$
b = b - \eta \cdot \Delta b
$$

---

## 🐍 Python Code Example (From Scratch)

Here’s a minimal neural network with 1 hidden layer trained using backpropagation:

```python
import numpy as np

# Sigmoid activation and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Training dataset: XOR problem (classic example)
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

# Initialize weights and biases randomly
np.random.seed(42)
input_neurons = 2
hidden_neurons = 2
output_neurons = 1

W1 = np.random.uniform(-1, 1, (input_neurons, hidden_neurons))
B1 = np.random.uniform(-1, 1, (1, hidden_neurons))
W2 = np.random.uniform(-1, 1, (hidden_neurons, output_neurons))
B2 = np.random.uniform(-1, 1, (1, output_neurons))

# Learning rate
lr = 0.5

# Training loop
for epoch in range(10000):
    # ---- Forward pass ----
    hidden_input = np.dot(X, W1) + B1
    hidden_output = sigmoid(hidden_input)

    final_input = np.dot(hidden_output, W2) + B2
    final_output = sigmoid(final_input)

    # ---- Error ----
    error = y - final_output

    # ---- Backpropagation ----
    d_final = error * sigmoid_derivative(final_output)
    d_hidden = d_final.dot(W2.T) * sigmoid_derivative(hidden_output)

    # ---- Update weights ----
    W2 += hidden_output.T.dot(d_final) * lr
    B2 += np.sum(d_final, axis=0, keepdims=True) * lr
    W1 += X.T.dot(d_hidden) * lr
    B1 += np.sum(d_hidden, axis=0, keepdims=True) * lr

# ---- Final Prediction ----
print("Predictions after training:")
print(final_output.round(3))
```

---

## ✅ Example Output

```
Predictions after training:
[[0.01]
 [0.98]
 [0.98]
 [0.02]]
```

This shows the network has learned the XOR function!
