import os
import json
import re

def rename_notebooks():
    base_dir = r"c:\Users\24294\.trae\leetcode-hot100-ACM\大厂笔试真题"
    
    # 遍历所有子目录
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".ipynb") and ("_P" in file or file.count("P") >= 2):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        nb_content = json.load(f)
                    
                    # 从第一个 cell (markdown) 中提取标题
                    title = ""
                    if nb_content.get("cells") and nb_content["cells"][0].get("cell_type") == "markdown":
                        source = nb_content["cells"][0].get("source", [])
                        if source:
                            first_line = source[0].strip()
                            # 提取 # 标题 (PID) 中的标题部分
                            # 格式可能是 "# Title (PID)" 或 "# #PID. Title (PID)"
                            match = re.search(r'#\s*(?:#P\d+\.\s*)?(.*?)\s*\((P\d+)\)', first_line)
                            if match:
                                title = match.group(1).strip()
                                pid = match.group(2).strip()
                            else:
                                # 备选方案：直接取第一行去掉 # 
                                title = first_line.lstrip('#').strip()
                                pid = re.search(r'P\d+', file).group(0) if re.search(r'P\d+', file) else ""

                    if title:
                        # 清理标题中的非法字符
                        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
                        # 保持原始的前缀，例如 【华为OD】
                        prefix_match = re.match(r'(【.*?】)', file)
                        prefix = prefix_match.group(1) if prefix_match else ""
                        
                        # 获取 PID
                        pid_match = re.search(r'P\d+', file)
                        pid = pid_match.group(0) if pid_match else ""
                        
                        new_name = f"{prefix}{pid}_{safe_title}.ipynb"
                        new_path = os.path.join(root, new_name)
                        
                        if file_path != new_path:
                            print(f"Renaming: {file} -> {new_name}")
                            # 如果目标文件已存在，先删除（或者是同一个文件只是大小写不同）
                            if os.path.exists(new_path) and file.lower() != new_name.lower():
                                os.remove(new_path)
                            os.rename(file_path, new_path)
                            
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    rename_notebooks()
