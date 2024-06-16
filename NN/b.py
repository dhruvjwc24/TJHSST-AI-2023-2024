import sys; args = sys.argv[1:]
import math, random
LR = 0.1

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

def calcErrorCells(trueVal, output, layeredWeights):
    errorCellsRev = []
    outputRev = output[::-1]
    layeredWeightsRev = layeredWeights[::-1]

    for outputLayerNum, outputLayer in enumerate(outputRev):
        errorCellLayer = []
        if not errorCellsRev:
            errorCellLayer = [trueVal-outputLayer[i] for i in range(len(outputLayer))]
            errorCellsRev.append(errorCellLayer)
        else:
            for outputLayerValueNum, outputLayerValue in enumerate(outputLayer):
                errorCellLayer.append(outputLayerValue*(1-outputLayerValue)*layeredWeights[-outputLayerNum][outputLayerValueNum]*errorCellsRev[-1][0])
            errorCellsRev.append(errorCellLayer)
    return errorCellsRev[::-1]

def calcPartials(inputLayer, output, errorCells):
    partials = []
    outputWithInput = [inputLayer] + output
    for layerNum, layer in enumerate(outputWithInput[:-1]):
        partialsOfLayer = []
        for inputValue in outputWithInput[layerNum]:
            partialsOfLayer.append([inputValue*errorCells[layerNum][i] for i in range(len(errorCells[layerNum]))])
        partials.append(partialsOfLayer)
    return partials

def updateWeights(outputWithInput, layeredWeights, partials, lr):
    for layerNum in range(len(layeredWeights)):
        # inc = len(layeredWeights[layer]) // len(outputWithInput[layer])
        for partialSetNum, partialSet in enumerate(partials[layerNum]):
            for i in range(len(partialSet)):
                layeredWeights[layerNum][partialSetNum+i*len(outputWithInput[layerNum])] += lr*partialSet[i]
    return layeredWeights
            
def averagePartials(partialsAll):
    # partialsMean = []
    for layerNum in range(len(partialsAll[0])):
        # partialsMeanLayer = []
        for i in range(len(partialsAll[0][layerNum])):
            for j in range(len(partialsAll[0][layerNum][i])):
                partialsAll[0][layerNum][i][j] = sum([partialsAll[k][layerNum][i][j] for k in range(len(partialsAll))])/len(partialsAll)
        # partialsMean.append(partialsMeanLayer)
    return partialsAll[0]

def evaluate(expectedOutput, predictedOutput):
    correct = 0
    for i in range(len(expectedOutput)):
        if expectedOutput[i] == predictedOutput[i]: correct += 1
    return correct/len(expectedOutput)

def calculateError(expectedOutput, predictedOutput):
    return (expectedOutput-predictedOutput)**2

def displayWeights(layeredWeights):
    for layer in layeredWeights:
        print(" ".join([str(i) for i in layer]))

def train(layers, data, layeredWeights, transferFnID):
    fnDict = {1: t1, 2: t2, 3: t3, 4: t4}
    fn = fnDict[transferFnID]
    expectedOutput = [float(io[1][0]) for io in data]
    change = True
    epoch = 0
    bestWeights = layeredWeights
    minError = 100000
    while change:
        epochError = 0
        correct = 0
        change = False
        predictedOutput = []
        for ioNum, io in enumerate(data):
            inputLayer = [float(i) for i in io[0]] + [1.0]
            output = forwardProp(inputLayer, layeredWeights, fn)
            predictedOutput.append(output[-1][0])
            # if abs(predictedOutput[-1]-expectedOutput[ioNum]) <= 0.001: correct += 1
            epochError += calculateError(expectedOutput[ioNum], predictedOutput[-1])
            # print(f"Epoch {epoch} | Predicted {predictedOutput[-1]} | Expected {expectedOutput[ioNum]}", end=" | ")
            errorCells = calcErrorCells(expectedOutput[ioNum], output, layeredWeights)
            partials = calcPartials(inputLayer, output, errorCells)
            layeredWeights = updateWeights([inputLayer]+output, layeredWeights, partials, LR)
            # partialsAll.append(partials)
        # print(f"Correct: {correct}/{len(data)}\n")
        # if epochError < 0.1: 
        #     bestWeights = layeredWeights
        #     print(layeredWeights)
        # accuracy = evaluate(expectedOutput, predictedOutput[-1])
        # print(f"Epoch {epoch}: {predictedOutput[-1]}")
        # if accuracy == 1: return epoch
        # if epoch % 20000 == 0:
        #     displayWeights(layeredWeights)

        if epochError < 0.8*minError or epochError < 0.01:
            minError = epochError
            bestWeights = layeredWeights
            layers = [len(data[0][0])+1, 2, len(data[0][1]), len(data[0][1])]
            layerCountsStr = " ".join([str(i) for i in layers])
            print("Layer counts:", layerCountsStr)
            displayWeights(bestWeights)
            if epochError < 0.01: return epoch
        epoch += 1
            # if epochError > 0.1: 
            #     layeredWeights = []
            #     layeredWeights.append([random.random()-0.5 for j in range(layers[i]*layers[i+1])])
        change = True

def forwardProp(inputLayer, layeredWeights, transferFn):
    intermediaryOutputs = []
    for layerNum, layer in enumerate(layeredWeights):
        numWeightsOverInputs = len(layer) // len(inputLayer)
        if layerNum == len(layeredWeights) - 1: intermediaryOutputs.append([inputLayer[i] * layer[i] for i in range(len(inputLayer))]); return intermediaryOutputs
        dotProductsOfInputsAndWeights = [dotProduct(inputLayer, layer[i*len(inputLayer):(i+1)*len(inputLayer)]) for i in range(numWeightsOverInputs)]
        inputLayer = [transferFn(dotProductsOfInputsAndWeights[i]) for i in range(len(dotProductsOfInputsAndWeights))]
        intermediaryOutputs.append(inputLayer)
    return intermediaryOutputs
        
def main():
    # args = ['NN/weights/weights103.txt', 'T2', '2.0', '1.1']
    # print(args)
    inFile = open(args[0]).read().splitlines()
    # print(inFile)
    # inFile = open("NN/infile4.txt").read().splitlines()
    dataRaw = [line.split(" => ") for line in inFile]
    data = [[dataRaw[i][0].split(" "), dataRaw[i][1].split(" ")] for i in range(len(dataRaw))]
    layers = [len(data[0][0])+1, 2, len(data[0][1]), len(data[0][1])]
    layerCountsStr = " ".join([str(i) for i in layers])
    print("Layer counts:", layerCountsStr)
    # # weights = [[2, 1, 0, 1, 2, 3], [0.5, 0.75], [0.875]] # infile 2
    # # weights = [[0.3, -2, -1.5, 2, 0, 2], [0.3, -0.5], [-1]] # infile 3
    weights = []

    # weights = [[random.random()-0.5 for j in range(8)], [random.random()-0.5 for j in range(4)], [random.random()-0.5 for j in range(2)]] 
    for i in range(len(layers)-1):
        weights.append([random.random()-0.5 for j in range(layers[i]*layers[i+1])])
    weights[-1] = [random.random()-0.5 for j in range(layers[-1])]
    output = train(layers, data, weights, 3)

    # print(myInput)
    # layeredWeights, transferFn, inputs = open(args[0]).read().splitlines(), int(args[1][1:]), args[2:]
    # print(str(forwardProp(layeredWeights, transferFn, inputs))[1:-1])

if __name__ == '__main__': main()

# Dhruv Chandna Period 6 2025