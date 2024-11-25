import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

p = np.array([
[0.5, 0.6, 0.4],
[0.2, 0.3, 0.5],
[0.3, 0.1, 0.1]
])

cuisine = ['Chinese', 'Italian', 'Mexican']
cuisineDict = {'C': 0, 'I': 0, 'M': 0}

def getSequence(steps):
    '''
    Return a sequence of different states 
    '''
    x = np.array([1,0,0]).T
    sequence = []
    for i in range(steps):
        randomResto = np.random.choice(cuisine, p=x)
        sequence.append(randomResto[0])
        x = p@x
        
    return sequence

    

    