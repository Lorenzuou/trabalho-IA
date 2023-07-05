import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_csv('train.csv')

x = data['round']
y = data['best_fitness']

plt.plot(x,y, color='green', linestyle='dashed', linewidth = 3,marker='o', markerfacecolor='blue')
plt.xlabel('Round')
plt.ylabel('Pontuacao')
plt.title('Pontuacao x Round')
# x tickes shall be 0,10,20,...
plt.xticks(range(0, 200, 10))
# rotate x labels
plt.xticks(rotation=45)
# save the plot as a file
plt.savefig('Pontuacao.png')