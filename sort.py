# 定义一个模块化的程序用于排序 README.md 文件中的表格内容

def read_file(file_path: str) -> list:
    """读取文件内容并返回行列表
    Args:
        file_path (str): 文件路径
    Returns:
        list: 文件中的所有行
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

def write_file(file_path: str, lines: list) -> None:
    """将行列表写入文件
    Args:
        file_path (str): 文件路径
        lines (list): 要写入的内容
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def extract_table_indices(lines: list, table_start: str, table_end: str) -> tuple:
    """提取表格起始和结束的索引
    Args:
        lines (list): 文件内容行列表
        table_start (str): 表格起始标识
        table_end (str): 表格结束标识
    Returns:
        tuple: 表格起始和结束的索引
    """
    start_idx = lines.index(table_start)
    end_idx = lines.index(table_end)
    return start_idx, end_idx

def parse_table_content(lines: list) -> list:
    """解析表格内容，提取分类和名称
    Args:
        lines (list): 表格内容行列表
    Returns:
        list: (分类, 名称) 对的列表
    """
    find_name = lambda x: x[x.index("[") + 1 : x.index("]")].strip()
    find_cat = lambda x: x[: x.index("|")].strip()
    return [(find_cat(line), find_name(line)) for line in lines]

def sort_table_content(table_lines: list, pairs: list) -> list:
    """根据分类和名称排序表格内容
    Args:
        table_lines (list): 表格内容行列表
        pairs (list): 分类和名称的对列表
    Returns:
        list: 排序后的表格内容行列表
    """
    sorted_pairs = sorted(pairs)  # 按分类和名称排序
    return [table_lines[pairs.index(pair)] for pair in sorted_pairs]

def sort_readme(file_path: str) -> None:
    """主函数，执行README.md文件的排序
    Args:
        file_path (str): 文件路径
    """
    # 读取文件内容
    lines = read_file(file_path)

    # 定义表格的起始和结束标识
    table_start = "|Category|Company|Description|GitHub Stars|Alternative to|\n"
    table_end = "<!-- END STARTUP LIST -->\n"

    # 获取表格的起始和结束索引
    start_idx, end_idx = extract_table_indices(lines, table_start, table_end)

    # 提取表格内容和分类对
    table_lines = lines[start_idx + 2 : end_idx - 1]
    pairs = parse_table_content(table_lines)

    # 排序表格内容
    sorted_lines = sort_table_content(table_lines, pairs)

    # 更新文件内容
    lines[start_idx + 2 : end_idx - 1] = sorted_lines

    # 写入更新后的内容
    write_file(file_path, lines)

if __name__ == "__main__":
    sort_readme("README.md")
