import sys; args = sys.argv[1:]
import math

def dotProduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])
def t1(x):
    return x
def t2(x):
    if x > 0: return x
    return 0
def t3(x):
    return 1 / (1 + math.exp(-x))
def t4(x):
    return 2*t3(x) - 1

def forwardProp(layeredWeights, transferFn, inputs):
    fnDict = {1: t1, 2: t2, 3: t3, 4: t4}
    fn = fnDict[transferFn]
    
    inputLayer = [float(i) for i in inputs]
    for layer in range(len(layeredWeights)):
        weights = layeredWeights[layer].split(" ")
        weights = [float(i) for i in weights]
        numWeightsOverInputs = len(weights) // len(inputLayer)
        if layer == len(layeredWeights) - 1: return [inputLayer[i] * weights[i] for i in range(len(inputLayer))]
        dotProductsOfInputsAndWeights = [dotProduct(inputLayer, weights[i*len(inputLayer):(i+1)*len(inputLayer)]) for i in range(numWeightsOverInputs)]
        inputLayer = [fn(dotProductsOfInputsAndWeights[i]) for i in range(len(dotProductsOfInputsAndWeights))]
    return inputLayer
        
def main():
    # args = ['NN/weights/weights103.txt', 'T2', '2.0', '1.1']
    layeredWeights, transferFn, inputs = open(args[0]).read().splitlines(), int(args[1][1:]), args[2:]
    print(str(forwardProp(layeredWeights, transferFn, inputs))[1:-1])

if __name__ == '__main__': main()

# Dhruv Chandna Period 6 2025