import matplotlib.pyplot as plt
import math

angles= ['O', 'C', 'E', 'A', 'N']
data= [60, 4, 24, 28, 32]
angles+=angles[:1]
data+= data[:1]
plt.polar(angles, data)
plt.show()
