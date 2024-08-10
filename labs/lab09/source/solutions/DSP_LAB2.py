import numpy as np
import matplotlib.pyplot as plt
lowerBound = -10
upperBound = 10
shift = -1 

def Ui(lowerBound, upperBound, shift) :
        time_step = np.arange(lowerBound, upperBound, 1)
        imp_sig = np.zeros_like(time_step)

        for i in range(len(time_step)) :
            if time_step[i] == -shift :
                imp_sig[i] = 1
        return time_step, imp_sig
    
def Us(lowerBound, upperBound, shift) :
        time_step = np.arange(lowerBound, upperBound, 1)
        imp_sig = np.zeros_like(time_step)

        for i in range(len(time_step)) :
            if time_step[i] >= -shift :
                imp_sig[i] = 1
        return time_step, imp_sig

def Ur(lowerBound, upperBound, shift) :
        time_step = np.arange(lowerBound, upperBound, 1)
        imp_sig = np.zeros_like(time_step)

        for i in range(len(time_step)) :
            if time_step[i] >= -shift :
                imp_sig[i] = time_step[i] + shift
        return time_step, imp_sig

n, imp1 = Ui(lowerBound, upperBound, 0)
_, imp2 = Ui(lowerBound, upperBound, 1)
_, imp3 = Ui(lowerBound, upperBound, -1)
ex2a = imp1 - imp2 - imp3

ex2b = 2 * np.sin( np.pi/ 20 * n)


_, stp1 = Us(lowerBound, upperBound, 0)
ex3 = stp1

_, stp1 = Us(lowerBound, upperBound, 0)
_, stp2 = Us(lowerBound, upperBound, -1)
_, stp3 = Us(lowerBound, upperBound, -4)
ex4a = stp1 - 2*stp2 + stp3

_, imp1 = Ui(lowerBound, upperBound, +1)
_, imp2 = Ui(lowerBound, upperBound, 0)
_, stp3 = Us(lowerBound, upperBound, +1)
_, stp4 = Us(lowerBound, upperBound, -2)

ex4b = imp1 -imp2 + stp3 -stp4

plt.stem(n,ex4b)
plt.show()