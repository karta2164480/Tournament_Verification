import os
import re
import matplotlib.pyplot as plt
from natsort import natsorted

def extract_loss_values(folder_path, file_pattern):
    loss_values = []
    file_indices = []
    
    # 遍歷資料夾中的所有檔案
    for file_name in os.listdir(folder_path):
        if file_pattern.match(file_name):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                # 使用正則表達式找到loss值
                match = re.search(r'loss:\s+([\d.e+-]+)', content)
                if match:
                    loss = float(match.group(1))
                    loss_values.append(loss)
                    # 提取檔案名稱中的數字
                    index = int(re.search(r'2023_..._(\d{2,3})', file_name).group(1))
                    file_indices.append(index)
    
    # 使用自然排序來排序檔案索引和對應的loss值
    file_indices, loss_values = zip(*natsorted(zip(file_indices, loss_values)))
    
    return file_indices, loss_values

# 設定資料夾路徑
folder_path = 'result'

# 檔案名稱模式
old_file_pattern = re.compile(r'2023_old_\d{2,3}')
new_file_pattern = re.compile(r'2023_new_\d{2,3}')

# 提取兩組數據
old_file_indices, old_loss_values = extract_loss_values(folder_path, old_file_pattern)
new_file_indices, new_loss_values = extract_loss_values(folder_path, new_file_pattern)

# 繪製趨勢圖
plt.figure(figsize=(10, 5))

# 繪製舊的數據
plt.semilogy(old_file_indices, old_loss_values, marker='o', label='2023_old')  # 使用對數Y軸

# 繪製新的數據
plt.semilogy(new_file_indices, new_loss_values, marker='x', label='2023_new')  # 使用對數Y軸

plt.xticks(rotation=90)
plt.xlabel('File Index')
plt.ylabel('Loss (log scale)')
plt.title('Loss Trend Over Files')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()  # 添加圖例
plt.tight_layout()
plt.show()