words = open('dict3.txt', 'r').read().split()
sortedWords = sorted(words, key=lambda x: len(x))
print(len(sortedWords[-1]))