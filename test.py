import random
from analyzer import Analyzer
myAnalyzer = Analyzer()
print(myAnalyzer)
myInput = [random.randrange(0, 9, 1) for i in range(100000)]
output = myAnalyzer.run(myInput)
for elem in output:
    print(elem)