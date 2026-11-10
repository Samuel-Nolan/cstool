import os
import re

DOCS_DIR = "docs"

def preprocess_content(content: str) -> str:
    lines = content.splitlines()
    new_lines = []
    
    in_code_block = False
    in_callout = False
    
    for index, line in enumerate(lines):
        stripped = line.strip()
        
        # 忽略代码块内部的内容，防止破坏示例代码
        if stripped.startswith("```") or stripped.startswith("~~~"):
            was_in_code_block = in_code_block
            in_code_block = not in_code_block
            if in_callout:
                in_callout = False
            new_lines.append(line)
            
            # 代码块结束后紧接无序/有序列表时补充空行，避免列表被解析为代码内容
            if was_in_code_block and index + 1 < len(lines) and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[index + 1]):
                new_lines.append("")
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue

        # 匹配 Obsidian Callout 语法：> [!type]+/- 标题
        callout_match = re.match(r"^>\s*\[!(\w+)\]([+-])?(?:\s*(.*))?$", line.strip())
        if callout_match:
            in_callout = True
            c_type = callout_match.group(1).lower()
            c_fold = callout_match.group(2)
            c_title = callout_match.group(3).strip() if callout_match.group(3) else ""
            
            # 折叠型 callout 映射为 pymdownx.details (??? 或 ???+)
            if c_fold == "-":
                prefix = "???"
            elif c_fold == "+":
                prefix = "???+"
            else:
                prefix = "!!!"
                
            if c_title:
                new_lines.append(f'{prefix} {c_type} "{c_title}"')
            else:
                new_lines.append(f'{prefix} {c_type}')
            continue

        if in_callout:
            if line.startswith(">"):
                # 去除前导引用符，替换为 4 空格缩进
                sub_content = re.sub(r"^>\s?", "    ", line)
                new_lines.append(sub_content)
                continue
            elif stripped == "":
                new_lines.append("")
                continue
            else:
                # 遇到非空且不以 > 开头的行，Callout 结束
                in_callout = False
                
        # 处理图片嵌入语法：![[path/img.png|500]] 或 ![[path/img.png]]
        def repl_img(m):
            img_path = m.group(1).strip().replace(" ", "%20")
            extra = m.group(2).strip() if m.group(2) else ""
            if extra:
                dim_match = re.match(r"^(\d+)(?:x(\d+))?$", extra)
                if dim_match:
                    width = dim_match.group(1)
                    height = dim_match.group(2)
                    if height:
                        return f'<img src="{img_path}" width="{width}" height="{height}">'
                    return f'<img src="{img_path}" width="{width}">'
                return f'<img src="{img_path}" alt="{extra}">'
            return f'<img src="{img_path}">'
            
        line = re.sub(r"!\[\[([^|\]\n]+)(?:\|([^\]\n]+))?\]\]", repl_img, line)
        
        # 处理双链语法：[[target#anchor|label]] 或 [[target]]
        def repl_link(m):
            target = m.group(1).strip()
            label = m.group(2).strip() if m.group(2) else ""
            
            if "#" in target:
                page, anchor = target.split("#", 1)
                if not page:
                    href = f"#{anchor}"
                else:
                    href = f"{page}.md#{anchor}" if not page.endswith(".md") else f"{page}#{anchor}"
            else:
                href = f"{target}.md" if not target.endswith(".md") else target
                
            text = label if label else target.split("/")[-1].replace(".md", "")
            return f"[{text}]({href})"
            
        line = re.sub(r"(?<!!)\[\[([^|\]\n]+)(?:\|([^\]\n]+))?\]\]", repl_link, line)
        
        new_lines.append(line)
        # 表格结束后紧接列表时补充空行，避免列表被解析为普通段落 (paragraph)
        if stripped.startswith("|") and stripped.endswith("|") and index + 1 < len(lines):
            if re.match(r"^\s*([-*+]|\d+\.)\s+", lines[index + 1]):
                new_lines.append("")
        
    return "\n".join(new_lines) + ("\n" if content.endswith("\n") else "")

def process_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = preprocess_content(content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Preprocessed: {filepath}")

def main():
    if not os.path.exists(DOCS_DIR):
        print(f"Directory {DOCS_DIR} not found.")
        return
        
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
