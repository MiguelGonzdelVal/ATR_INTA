import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(r'Resultados/2023_03_07_12_12_25.txt')
df.plot(x='timestamp')
plt.show()
