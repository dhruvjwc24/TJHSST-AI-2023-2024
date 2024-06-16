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
def calculateLoss(trueValues, predictedValues):
    return sum([calculateError(trueValues[i], predictedValues[i]) for i in range(len(trueValues))])/len(trueValues)
def calculateAccuracy(trueValues, predictedValues):
    runningTotal = 0
    for i in range(len(trueValues)):
        predictedValueRounded = 1 if predictedValues[i] > 0.5 else 0
        if predictedValueRounded == trueValues[i]: runningTotal += 1
    return runningTotal/len(trueValues)
def calculateMetrics(trueValues, predictedValues):
    loss = calculateLoss(trueValues, predictedValues)
    accuracy = calculateAccuracy(trueValues, predictedValues)
    return loss, accuracy


    # runningTotal = 0
    # for io in testingSet:
    #     trueOutput = io[1]
    #     inputLayer = io[0]
    #     predOutput = forwardProp(inputLayer, layeredWeights, fn)[-1][0]
    #     runningTotal += calculateError(trueOutput, predOutput)
    # return runningTotal/len(testingSet)
def displayWeights(layeredWeights):
    for layer in layeredWeights:
        print(" ".join([str(i) for i in layer]))
def train(layeredWeights, transferFnID, value, operator, displayWeightsBool, testingSet=None, epochs=None):
    fnDict = {1: t1, 2: t2, 3: t3, 4: t4}
    fn = fnDict[transferFnID]
    value = float(value)
    if not epochs: epochs = 150
    # bestWeights = layeredWeights
    # bestLoss = calculateLoss(layeredWeights, testingSet, fn)
    for epoch in range(epochs):
        trainingSet = makeDataset(value, operator, 25000, True)
        trueValues = []
        predictedValues = []
        for ioNum, io in enumerate(trainingSet):
            inputLayer = io[0]
            output = forwardProp(inputLayer, layeredWeights, fn)
            errorCells = calcErrorCells(io[1], output, layeredWeights)
            partials = calcPartials(inputLayer, output, errorCells)
            layeredWeights = updateWeights([inputLayer]+output, layeredWeights, partials, LR)
            trueValues.append(io[1])
            predictedValues.append(output[-1][0])
        currentLoss, currentAccuracy = calculateMetrics(trueValues, predictedValues)
        # if currentLoss < bestLoss:
        #     bestLoss = currentLoss
        #     bestWeights = layeredWeights
        #     print(f"Epoch {epoch}: {currentLoss}")
        #     displayWeights(bestWeights)
        print(f"Epoch: {epoch} | Loss: {currentLoss} | Accuracy: {currentAccuracy}")
        if displayWeightsBool: displayWeights(layeredWeights)
    return layeredWeights
def forwardProp(inputLayer, layeredWeights, transferFn):
    intermediaryOutputs = []
    for layerNum, layer in enumerate(layeredWeights):
        numWeightsOverInputs = len(layer) // len(inputLayer)
        if layerNum == len(layeredWeights) - 1: intermediaryOutputs.append([inputLayer[i] * layer[i] for i in range(len(inputLayer))]); return intermediaryOutputs
        dotProductsOfInputsAndWeights = [dotProduct(inputLayer, layer[i*len(inputLayer):(i+1)*len(inputLayer)]) for i in range(numWeightsOverInputs)]
        inputLayer = [transferFn(dotProductsOfInputsAndWeights[i]) for i in range(len(dotProductsOfInputsAndWeights))]
        intermediaryOutputs.append(inputLayer)
    return intermediaryOutputs
def parseInequality(ineq):
    if "<=" in ineq:
        val = ineq.split("<=")[1]
        operator = "<="
    elif ">=" in ineq:
        val = ineq.split(">=")[1]
        operator = ">="
    elif "<" in ineq:
        val = ineq.split("<")[1]
        operator = "<"
    elif ">" in ineq:
        val = ineq.split(">")[1]
        operator = ">"
    else:
        return None
    return val, operator
def makeDataset(value, operator, size, hard=False):
    testingSet = []
    halfSize = int(size/2)
    for i in range(halfSize):
        inputLayer = [3*random.random()-1.5, 3*random.random()-1.5, 1]
        radius = inputLayer[0]**2 + inputLayer[1]**2
        if operator == "<=": t = 1 if radius <= value else 0
        elif operator == ">=": t = 1 if radius >= value else 0
        elif operator == "<": t = 1 if radius < value else 0
        elif operator == ">": t = 1 if radius > value else 0
        else: return None
        testingSet.append((inputLayer, t))
    i = 0

    while i < halfSize:
        inputLayer = [3*random.random()-1.5, 3*random.random()-1.5, 1]
        radius = inputLayer[0]**2 + inputLayer[1]**2
        if abs(radius-value) > 0.1 and hard: continue
        if operator == "<=": t = 1 if radius <= value else 0
        elif operator == ">=": t = 1 if radius >= value else 0
        elif operator == "<": t = 1 if radius < value else 0
        elif operator == ">": t = 1 if radius > value else 0
        else: return None
        testingSet.append((inputLayer, t))
        i += 1
    return testingSet       
def main():
    try: displayWeightsBool = True if args else False
    except: displayWeightsBool = False
    # args = ["x*x+y*y>1.0720066875842724"] #Transferred weights from this
    # args = ["x*x+y*y<1.0949311491067082"]
    ineq = args[0]
    value, operator = parseInequality(ineq)
    layers = [3, 10, 10, 1, 1] # 0.9766
    # layers = [3, 10, 10, 1, 1]
    # layers = [3, 5, 5, 5, 1, 1]
    # weights = [[random.random()-0.5 for j in range(layers[i]*layers[i+1])] for i in range(len(layers)-1)]
    weights = [[-6.909138721599471, -9.36191904436256, 8.670323988630152, -6.652942744096723, 11.181857597534528, -11.691572272871188, -4.555136414935972, -12.686302168620495, -8.448486199845537, -11.125077184610417, -4.291770867588248, -8.806731875060233, 1.76251326788041, -12.602201169419164, -11.35809591318666, 6.6336131080306195, -8.331529752036435, -5.897293274960242, -7.558905628615231, -6.422015208807245, -9.2113986817871, -10.444410000821238, 6.349720406599028, -9.22016618857465, 5.099797190814487, 5.895709563848975, -7.786392772984931, 12.782912312342644, -4.3505798488523295, -11.743371309596483], [24.621670892480704, -14.350645403810885, -8.651904516878805, -13.08057971956719, -9.778484252712449, -8.697315153498321, -6.5320259374195215, -13.739226723457369, -2.7527835968949397, -18.76308780332026, -5.738339945050807, -1.5162668368409284, -1.1970908510715226, -2.1106287218196687, -8.084627549622244, -3.4946003494985725, -2.3834627048768535, -4.974671305562494, 4.488031474972479, -2.69440139030594, 0.42597335351295224, -0.6434598413138948, -5.1437206574557734, -3.558192799646889, -0.3870395287026148, -2.2209107302441393, 0.9156063349359369, -2.8754842465083237, -1.8127214550820159, -0.49370560686002146, -0.42247076911979825, -0.6861434107448947, -2.9789342623089294, -2.0632677413619773, -0.905486868630624, -1.0755128525043571, 0.4858636051567557, -1.7036862561438022, -0.9585296830744279, -0.7530935784430375, 0.17049565851005336, 1.2447169105129123, -2.7980156976867745, -2.1712358280864166, -0.9425963601748016, 0.1509420132681204, 0.9844201050133058, -0.3150591179027949, 0.1789887377604816, 0.7187927647335173, 0.3395326775703728, -0.9135282459177091, -4.714184427876274, -3.5431773120261396, -0.1901011732987506, -2.0183241939830765, 0.6544059267352644, -2.508876929848848, -1.4007840976441641, -0.6113991358934032, -0.27572379859177615, -0.6460836949542359, -3.247643002043223, -2.3171167607021768, -0.7278659264091929, -1.2295321637010754, 0.49623148784068005, -1.9102399426326238, -1.3457951148857035, -0.7578420629759256, 0.11762562208173791, -0.5921142883539326, -3.846070839242961, -2.309303014537576, -0.872290905478454, -1.338083891491758, -0.06468888518103451, -2.1833865869106166, -1.7686257705438762, -0.877508161941943, -0.6011604929898288, -0.6183431393526102, -3.055801472002349, -1.9099202037775265, -0.37444560864337956, -1.353142270933184, 0.14918276695715846, -1.7401397128236686, -1.2646789248994357, -0.3449350054555795, 1.0600766050339518, 0.9518039468556673, -0.792864233616019, -0.5250465324526611, 0.9876134811752566, 1.2788249802248564, 3.140414167111146, 0.7155797056851609, 1.9156583133710945, -0.07981886166473826], [-20.481148332812552, 8.004962044032546, -3.967400771977409, -2.0526123869064943, 1.4871501779734702, -3.5250438833131037, -2.4552002691504065, -2.847071176042644, -2.325352381313645, 5.886020265453519], [1.0098087188182348]]
    layerCountsStr = " ".join([str(i) for i in layers])
    print("Layer counts:", layerCountsStr)
    finalWeights = train(weights, 3, value, operator, displayWeightsBool, None, 100)
    return


if __name__ == '__main__': main()

# Dhruv Chandna Period 6 2025