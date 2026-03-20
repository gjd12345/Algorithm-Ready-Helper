import os
import re

def remove_pid_prefix(directory):
    # This regex will find:
    # 1. (【.*?】) - The company prefix like 【华为OD】
    # 2. P\d+ - The PID part like P2977
    # 3. [ _]? - Optional space or underscore
    # 4. (.*\.ipynb) - The rest of the filename (the title)
    # We want to keep 1 and 4.
    
    pattern = re.compile(r'(【.*?】)P\d+[ _]+(.*\.ipynb)')
    
    # Also handle cases without prefix if any
    pattern_no_prefix = re.compile(r'^P\d+[ _]+(.*\.ipynb)')

    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".ipynb"):
                continue
                
            new_name = None
            
            # Match with prefix
            match = pattern.match(file)
            if match:
                prefix = match.group(1)
                title = match.group(2)
                new_name = f"{prefix}{title}"
            else:
                # Match without prefix
                match_no_prefix = pattern_no_prefix.match(file)
                if match_no_prefix:
                    new_name = match_no_prefix.group(1)
            
            if new_name:
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                
                # Check if file already exists with new name
                if os.path.exists(new_path) and old_path != new_path:
                    print(f"Skipping (target exists): {file} -> {new_name}")
                else:
                    print(f"Renaming: {file} -> {new_name}")
                    try:
                        os.rename(old_path, new_path)
                        count += 1
                    except Exception as e:
                        print(f"Error renaming {file}: {e}")
    
    print(f"Successfully renamed {count} files.")

if __name__ == "__main__":
    base_dir = r"c:\Users\24294\.trae\leetcode-hot100-ACM\大厂笔试真题"
    remove_pid_prefix(base_dir)
