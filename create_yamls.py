"""
此脚本用于从 README.md 中提取信息并生成对应的 YAML 文件
"""

import yaml
import os

def read_readme(file_path="README.md"):
    """
    读取 README.md 文件并提取表格内容行
    :param file_path: README 文件路径
    :return: 包含表格内容的行列表
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 定义表格的起始和结束标记
    table_start_marker = "|Category|Company|Description|GitHub Stars|Alternative to|\n"
    table_end_marker = "<!-- END STARTUP LIST -->\n"

    # 找到起始和结束标记的索引
    try:
        start_index = lines.index(table_start_marker)
        end_index = lines.index(table_end_marker)
    except ValueError:
        raise ValueError("未找到表格的起始或结束标记，请检查 README.md 格式是否正确")

    # 提取表格内容行（去掉标题行和结束标记）
    return lines[start_index + 2 : end_index - 1]


def parse_line(line):
    """
    解析表格中的一行，提取所需信息
    :param line: 表格中的一行字符串
    :return: 包含解析信息的字典
    """
    columns = line.split("|")
    category = columns[0].strip()
    company_name = columns[1].split("]")[0][1:]
    website = columns[1].split("]")[1][1:-1]
    description = columns[2].strip()
    github_link = columns[3].split(">")[0].split("href=")[1].strip()
    alternative_names = [x.strip().split("]")[0][1:] for x in columns[4].split(",")]
    alternative_links = [x.strip().split("](")[1][:-1] for x in columns[4].split(",")]

    return {
        "category": category,
        "company_name": company_name,
        "link": website,
        "description": description,
        "gh_link": github_link,
        "alts_names": alternative_names,
        "alts_links": alternative_links,
    }


def save_to_yaml(data, output_dir="submissions"):
    """
    将解析后的数据保存为 YAML 文件
    :param data: 解析后的数据字典
    :param output_dir: 输出文件夹路径
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 生成文件名
    file_name = "_".join(data["company_name"].split(" "))
    output_path = os.path.join(output_dir, f"{file_name}.yaml")

    # 保存为 YAML 文件
    with open(output_path, "w", encoding="utf-8") as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def main():
    """
    主函数：读取 README，解析内容并保存为 YAML 文件
    """
    try:
        lines = read_readme()
        for line in lines:
            parsed_data = parse_line(line)
            save_to_yaml(parsed_data)
        print("YAML 文件生成成功！")
    except Exception as e:
        print(f"处理时出错：{e}")


if __name__ == "__main__":
    main()
