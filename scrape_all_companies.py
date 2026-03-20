import requests
from bs4 import BeautifulSoup
import re
import os
import json
import nbformat as nbf
import time
import sys

# 设置标准输出编码为 UTF-8，防止打印乱码
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 根据图片提取的公司及其在 codefun2000 上的 ID
# 注意：有些 ID 需要通过测试或分析页面获取
COMPANIES = [
    ('hw', '华为'),
    ('hwmj', '华为面经'),
    ('meituan', '美团'),
    ('jd', '京东'),
    ('ali', '阿里'),
    ('xhs', '小红书'),
    ('kdxf', '科大讯飞'),
    ('rongyao', '荣耀'),
    ('dd', '滴滴'),
    ('xiaomi', '小米'),
    ('zjtd', '字节跳动'),
    ('xiapi', '虾皮'),
    ('elm', '饿了么'),
    ('mayi', '蚂蚁'),
    ('zgdx', '中国电信'),
    ('xkl', '新凯来'),
    ('tx', '腾讯'),
    ('pdd', '拼多多'),
    ('mhy', '米哈游'),
    ('bd', '百度'),
    ('txyy', '腾讯音乐'),
    ('dewu', '得物'),
    ('xiecheng', '携程'),
    ('dajiang', '大疆'),
    ('wangyi', '网易'),
    ('dingding', '钉钉'),
    ('bizhan', 'b站'),
    ('vivo', 'vivo'),
    ('oppo', 'oppo'),
    ('hwod', '华为OD')
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_pids_for_pset(pset_id):
    url = f"https://codefun2000.com/problemset/{pset_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        # 匹配 window.UiContextNew 或 window.ProblemContextNew
        for match in re.finditer(r"window\.[a-zA-Z]*ContextNew\s*=\s*'(.*?)';", r.text, re.S):
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                if 'groups' in data:
                    problems = []
                    for group in data['groups']:
                        for p in group.get('problems', []):
                            problems.append({
                                'pid': p['pid'],
                                'title': p['title']
                            })
                    if problems:
                        return problems
            except:
                continue
        # 备选：正则直接匹配 pid
        pids = re.findall(r'pid":"(P[0-9]*)"', r.text)
        if pids:
            return [{'pid': pid, 'title': pid} for pid in set(pids)]
    except Exception as e:
        print(f"Error fetching pset {pset_id}: {e}")
    return []

def scrape_problem_detail(pid):
    # 如果 pid 看起来像一个完整的 URL，则直接使用它
    if pid.startswith('http'):
        url = pid
    else:
        url = f"https://codefun2000.com/p/{pid}"
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 1. 标题
        title = pid.split('/')[-1] if pid.startswith('http') else pid
        title_tag = soup.find('h1', class_='section__title') or soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # 2. 内容区域
        content_div = soup.find('div', id='content-ZhContent') or \
                      soup.find('div', class_='problem_content', id=False) or \
                      soup.find('div', class_='markdown-body')
        if not content_div:
            return None

        # 3. 处理 LaTeX (Katex)
        for katex in content_div.find_all('span', class_='katex'):
            tex_tag = katex.find('annotation', encoding='application/x-tex')
            if tex_tag:
                tex = tex_tag.get_text()
                is_display = 'display' in str(katex.get('class', [])) or katex.find('div', class_='katex-display')
                if is_display:
                    katex.replace_with(f"\n$$\n{tex}\n$$\n")
                else:
                    katex.replace_with(f"${tex}$")
            else:
                # 尝试从 mathml 获取
                math_tag = katex.find('math')
                if math_tag and math_tag.get('alttext'):
                    katex.replace_with(f"${math_tag.get('alttext')}$")

        # 清理干扰元素
        for s in content_div(['script', 'style', 'button']):
            s.decompose()
        for hidden in content_div.find_all(style=re.compile(r'display:\s*none')):
            hidden.decompose()

        sections = {'description': '', 'input_desc': '', 'output_desc': '', 'samples': [], 'hint': ''}
        markers = {'题目描述': 'description', '输入描述': 'input_desc', '输出描述': 'output_desc', '样例': 'samples', '说明': 'hint', '提示': 'hint'}
        
        current_section = 'description'
        
        for element in content_div.children:
            if not element.name:
                text = str(element).strip()
                if text: sections[current_section] += text + " "
                continue
                
            text = element.get_text(strip=True)
            if element.name in ['h2', 'h3', 'h4', 'strong']:
                found = False
                for m, s in markers.items():
                    if m in text:
                        current_section = s
                        found = True
                        break
                if found: continue

            if current_section == 'samples':
                if element.name == 'pre' or 'Copy' in text:
                    sample_text = element.get_text(strip=True).replace('Copy', '')
                    if sample_text: sections['samples'].append(sample_text)
            else:
                if element.name == 'pre':
                    sections[current_section] += f"\n```\n{element.get_text(strip=True)}\n```\n\n"
                elif element.name in ['ul', 'ol']:
                    for li in element.find_all('li'):
                        sections[current_section] += f"- {li.get_text(strip=True)}\n"
                    sections[current_section] += "\n"
                elif element.name == 'p':
                    sections[current_section] += element.get_text(strip=True) + "\n\n"
                else:
                    # 处理可能包含 LaTeX 的 div
                    sections[current_section] += element.get_text("\n", strip=True) + "\n\n"

        # 最终清理空白
        for k in sections:
            if isinstance(sections[k], str):
                sections[k] = re.sub(r'\n{3,}', '\n\n', sections[k]).strip()

        return {'title': title, 'sections': sections}
    except Exception as e:
        print(f"Error scraping {pid}: {e}")
        return None

def create_notebook(problem_data, output_path):
    pid = problem_data.get('pid', 'Unknown')
    title = problem_data.get('title', pid)
    detail = problem_data.get('sections', {})
    
    nb = nbf.v4.new_notebook()
    md_parts = [f"# {title} ({pid})"]
    if detail.get('description'): md_parts.append(f"## 题目描述\n\n{detail['description']}")
    if detail.get('input_desc'): md_parts.append(f"## 输入描述\n\n{detail['input_desc']}")
    if detail.get('output_desc'): md_parts.append(f"## 输出描述\n\n{detail['output_desc']}")
    
    samples = detail.get('samples', [])
    if samples:
        md_parts.append("## 样例")
        for i in range(0, len(samples), 2):
            if i + 1 < len(samples):
                md_parts.append(f"### 样例输入 {i//2 + 1}\n\n```\n{samples[i]}\n```")
                md_parts.append(f"### 样例输出 {i//2 + 1}\n\n```\n{samples[i+1]}\n```")
            else:
                md_parts.append(f"### 样例 {i//2 + 1}\n\n```\n{samples[i]}\n```")
                
    if detail.get('hint'): md_parts.append(f"## 说明/提示\n\n{detail['hint']}")
    
    nb.cells.append(nbf.v4.new_markdown_cell("\n\n---\n\n".join(md_parts)))
    nb.cells.append(nbf.v4.new_code_cell("import sys\n\ndef solve():\n    # 在这里编写解题逻辑\n    pass\n\nif __name__ == '__main__':\n    solve()"))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(BASE_DIR, "大厂笔试真题")
    
    # 首先处理用户额外指定的题目
    extra_problems = [
        ('https://codefun2000.com/codenote/coding/P4499', '算法课')
    ]
    for url, cat in extra_problems:
        output_dir = os.path.join(base_dir, cat)
        os.makedirs(output_dir, exist_ok=True)
        res = scrape_problem_detail(url)
        if res:
            pid = url.split('/')[-1]
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', res['title'])
            filename = f"【{cat}】{pid}_{safe_title}.ipynb"
            create_notebook({'pid': pid, 'title': res['title'], 'sections': res['sections']}, os.path.join(output_dir, filename))
            print(f"已抓取额外题目: {filename}")

    for pset_id, company_name in COMPANIES:
        output_dir = os.path.join(base_dir, company_name)
        os.makedirs(output_dir, exist_ok=True)
        print(f"--- 正在处理 {company_name} ---")
        problems = get_pids_for_pset(pset_id)
        if not problems:
            print(f"警告: 未能获取 {company_name} 的题目列表")
            continue
        print(f"找到 {len(problems)} 道题目")
        
        # 爬取该公司的所有题目
        for p in problems:
            pid = p['pid']
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', p['title'])
            safe_title = "".join(c for c in safe_title if ord(c) < 0xD800 or ord(c) > 0xDFFF)
            filename = f"【{company_name}】{pid}_{safe_title}.ipynb"
            output_path = os.path.join(output_dir, filename)
            
            if os.path.exists(output_path):
                continue
                
            print(f"正在爬取 {pid} - {p['title']}...")
            res = scrape_problem_detail(pid)
            if not res: continue
            
            create_notebook({'pid': pid, 'title': res['title'], 'sections': res['sections']}, output_path)
            time.sleep(0.5) # 稍微加快一点速度

if __name__ == "__main__":
    main()
