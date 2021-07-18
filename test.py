import random
from feedback import Feedback
myFeedback = Feedback()
print(myFeedback)
myInput = [random.randrange(0, 9, 1) for i in range(100000)]
output = myFeedback.run(input = myInput)
for elem in output:
    print(elem)