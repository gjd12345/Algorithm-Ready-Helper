import os
import json
import shutil
import re

def categorize_ai_problems():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(BASE_DIR, "大厂笔试真题")
    target_dir = os.path.join(BASE_DIR, "按类别的AI大厂机试")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Keywords to identify AI/ML related problems
    keywords = [
        "AI", "机器学习", "深度学习", "神经网络", "卷积", "CNN", "RNN", "LSTM", 
        "Transformer", "Attention", "梯度下降", "朴素贝叶斯", "K-means", 
        "决策树", "随机森林", "SVM", "逻辑回归", "线性回归", "池化", "Pooling", 
        "激活函数", "ReLU", "Softmax", "损失函数", "Loss", "反向传播", 
        "Backpropagation", "KL 散度", "交叉熵", "Cross Entropy", "大模型", 
        "LLM", "GPT", "BERT", "ViT", "特征工程", "欠拟合", "过拟合", "正则化",
        "聚类", "分类器", "回归分析"
    ]
    
    # Compile a single regex for efficiency
    keyword_pattern = re.compile('|'.join(re.escape(k) for k in keywords), re.IGNORECASE)
    
    count = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if not file.endswith(".ipynb"):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if keyword_pattern.search(content):
                    # Found an AI problem
                    dest_path = os.path.join(target_dir, file)
                    
                    # If file with same name exists, handle it (append company name or something if needed)
                    # For now, just copy. The filenames already have company prefixes.
                    if not os.path.exists(dest_path):
                        shutil.copy2(file_path, dest_path)
                        print(f"Copied AI problem: {file}")
                        count += 1
                    else:
                        # If filename exists but it's a different file (different path)
                        # We might need to handle collisions, but since we have company prefixes, 
                        # collisions are less likely unless the same problem is under different companies.
                        pass
                        
            except Exception as e:
                print(f"Error processing {file}: {e}")
                
    print(f"Successfully categorized {count} AI-related problems into {target_dir}.")

if __name__ == "__main__":
    categorize_ai_problems()
