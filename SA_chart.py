import re
import matplotlib.pyplot as plt

# 讀取檔案
file_path = 'log_SA3.txt'
with open(file_path, 'r') as file:
	lines = file.readlines()

# 提取loss後面的數字
loss_values = []
for line in lines:
	if 'loss:' in line and "best" not in line:
		a = line.split(' ')
		loss_values.append(float(a[2]))

# 畫圖
plt.plot(loss_values)
plt.xlabel('Time')
plt.ylabel('Loss')
plt.title('Loss Curve')
plt.show()