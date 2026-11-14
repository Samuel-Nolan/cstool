import os
import re

DOCS_DIR = "docs"

def is_bullet_item(line: str) -> bool:
    stripped = line.strip()
    # 排除 Markdown 水平分割线，如 ---, - - -, ----
    if re.match(r"^(-\s*){3,}$", stripped):
        return False
    return bool(re.match(r"^\s*-\s+", line))

def is_ordered_item(line: str) -> bool:
    return bool(re.match(r"^\s*\d+\.\s+", line))

def preprocess_content(content: str) -> str:
    lines = content.splitlines()
    new_lines = []
    
    in_code_block = False
    in_callout = False
    in_bullet_list = False
    in_frontmatter = False
    
    for index, line in enumerate(lines):
        stripped = line.strip()
        
        # 识别 YAML Frontmatter
        if index == 0 and stripped == "---":
            in_frontmatter = True
            new_lines.append(line)
            continue
            
        if in_frontmatter:
            new_lines.append(line)
            if stripped == "---":
                in_frontmatter = False
            continue

        # 忽略代码块内部的内容，防止破坏示例代码
        if stripped.startswith("```") or stripped.startswith("~~~"):
            was_in_code_block = in_code_block
            in_code_block = not in_code_block
            if in_callout:
                in_callout = False
            in_bullet_list = False
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue

        # 匹配 Obsidian Callout 语法：> [!type]+/- 标题
        callout_match = re.match(r"^>\s*\[!(\w+)\]([+-])?(?:\s*(.*))?$", line.strip())
        if callout_match:
            in_callout = True
            in_bullet_list = False
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
                line = re.sub(r"^>\s?", "    ", line)
                stripped = line.strip()
            elif stripped == "":
                in_bullet_list = False
                new_lines.append("")
                continue
            else:
                # 遇到非空且不以 > 开头的行，Callout 结束
                in_callout = False
                in_bullet_list = False
                
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
        
        # 列表状态管理与首个无序列表前置空行处理
        if is_bullet_item(line):
            if not in_bullet_list:
                # 识别到首个无序列表 - 时，若前一行非空行则插入空行
                if new_lines and new_lines[-1].strip() != "":
                    # 避免在 Callout 声明行后直接插入空行
                    if not new_lines[-1].strip().startswith(("!!!", "???")):
                        new_lines.append("")
                in_bullet_list = True
        elif is_ordered_item(line):
            # 有序列表项：设为列表态，避免其下方嵌套的无序列表被误判为独立新列表
            in_bullet_list = True
        elif stripped == "":
            in_bullet_list = False
        else:
            # 非空非列表行：若为缩进行且当前处于列表态，保留为列表项的多行延续；否则退出列表态
            if not (in_bullet_list and (line.startswith(" ") or line.startswith("\t"))):
                in_bullet_list = False

        new_lines.append(line)
        
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
