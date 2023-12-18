import sys; args = sys.argv[1:]
import time
from math import log10 , floor

graph = {}
words = []
components = {}

def round_it(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)
        
def bfs(start, goal):
    parseMe = [start]
    dctSeen = {start: ""}
    for word in parseMe:
        for nbr in graph[word][0]:
            if nbr == goal:
                dctSeen[nbr] = word
                return dctSeen
            if nbr in dctSeen:
                continue
            else:
                dctSeen[nbr] = word
                parseMe.append(nbr)

    return dctSeen

def findPath(start, goal):
    if start == goal:
        return (start, 0)
    parseMe = [start]
    dctSeen = {start: ""} #list of parents visited
    # s1 = 0
    while parseMe:
        node = parseMe.pop(0)
        # s2 = 0
        for nbr in graph[node][0]:
            # print(f"{s1}.{s2}")
            # s2+=1
            if nbr == goal:
                path = (dctSeen[node] + " " + node + " " + nbr).strip()
                pathLength = len(path.split(" "))-1
                return(path, pathLength)
                
            if nbr not in dctSeen:
                dctSeen[nbr] = dctSeen[node] + " " + node
                parseMe.append(nbr)
        # s1+=1
    path = (dctSeen[node] + " " + node + " " + nbr).strip()
    pathLength = len(path.split(" "))-1
    return(path, pathLength)

def farthestDistanceFromWord(word):
    wordComponent = {}
    for component in components:
        if word in component:
            wordComponent = component
            break

    maxDistance = 0
    maxWord = word
    for word2 in wordComponent:
        path,pathLength = findPath(word, word2)
        if pathLength > maxDistance:
            maxDistance = pathLength
            maxWord = word2
    return maxWord


def word_count():
    return len(words)

def get_max_deg():
    return max([graph[word][1] for word in graph])

def get_second_max_deg():
    maxDeg = get_max_deg()
    return max([m for word in graph if (m:=graph[word][1])!=maxDeg])

def get_ex_word_2nd_max_deg():
    secondMaxDeg = get_second_max_deg()
    for word in graph: 
        if graph[word][1]==secondMaxDeg:
            return word

def degree_list():
    maxDeg = get_max_deg()
    degList = [degree_count(deg) for deg in range(maxDeg+1)]
    return degList

def degree_count(deg):
    return sum([graph[word][1]==deg for word in graph])

def edge_count():
    return sum([graph[word][1] for word in graph])//2

def check_edge(w1, w2):
    return (len(w1)==len(w2) and (sum([c1==c2 for c1, c2 in zip(w1, w2)])==len(w1)-1))

# def create_graph():
#     for word in words:
#         mySet = set()
#         for word2 in words:
#             if word != word2 and check_edge(word, word2):
#                 mySet.add(word2)
#         graph[word] = (mySet, len(mySet))
#     return graph

def create_graph():
    graph = {}
    for word in words:
        adjacent_words = {word2 for word2 in words if word != word2 and check_edge(word, word2)}
        graph[word] = (adjacent_words, len(adjacent_words))
    return graph

def get_components():
    components = []
    componentsSet = set()
    for word in graph:
        if word in componentsSet:
            continue
        component = bfs(word, "")
        componentSet = set(list(component.keys())+list(component.values()))
        componentSet.remove("")
        componentsSet.update(componentSet)
        components.append(componentSet)
    return components

def get_number_distinct_component_sizes():
    return len(set(len(component) for component in components))

def get_number_largest_component_sizes():
    return max({len(component) for component in components})

def k_count(k):
    k_comps = []
    for component in components:
        if(len(component)==k):
            k_comps.append(component)
    return sum(get_components_adjacency(k_comps))

def get_components_adjacency(components):
    return [get_component_adjacency(component) for component in components]

def get_component_adjacency(component):
    componentList = list(component)
    adj = []
    for i, node in enumerate(componentList):
        adj.append(set(componentList[:i]+componentList[i+1:])==graph[node][0])
    return(all(adj))


start = time.process_time()
if len(args) == 0: args = ["test.txt", "caring", "dining"]
file = open(args[0])

words = file.read().splitlines()
graph = create_graph()
components = get_components()

print(f"Word count: {word_count()}")
print(f"Edge count: {edge_count()}")
print(f"Degree List: {degree_list()}")
# print(time.process_time()-start)
print(f"Construction time: {str(round_it(float(time.process_time()-start), 3))}s")
print(f"Second degree word: {get_ex_word_2nd_max_deg()}")
print(f"Connected component size count: {get_number_distinct_component_sizes()}")
print(f"Largest component size: {get_number_largest_component_sizes()}")
print(f"K2 count: {k_count(2)}")
print(f"K3 count: {k_count(3)}")
print(f"K4 count: {k_count(4)}")
if(len(args)==3):
    print(f"Neighbors: {graph[args[1]][0]}")
    print(f"Farthest: {farthestDistanceFromWord(args[1])}")
    path, pathLength = findPath(args[1], args[2])
    print(f"Path: {path.split(' ')}")

#Dhruv Chandna Period 6 2025