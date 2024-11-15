"""
此脚本用于将公司信息直接添加到列表中
"""

# 导入必要的模块
from typing import List


def get_repo_from_url(url: str) -> str:
    """
    根据URL获取仓库名称。

    :param url: 仓库的URL
    :return: 仓库名称
    """
    idx = url.find(".com/")
    return url[idx + len(".com/") :].strip("/")


def create_alternatives_md(names: List[str], links: List[str]) -> str:
    """
    创建一个Markdown格式的字符串，形式如下：
    [name1](link1), [name2](link2), ...

    :param names: 替代品名称列表
    :param links: 替代品链接列表
    :return: Markdown格式字符串
    """
    return ", ".join(f"[{name.strip()}]({link.strip()})" for name, link in zip(names, links))


def create_shield_link(gh_link: str) -> str:
    """
    创建GitHub星标的图片链接。

    :param gh_link: GitHub仓库链接
    :return: 星标图片的链接
    """
    return f"https://img.shields.io/github/stars/{get_repo_from_url(gh_link)}?style=social".strip()


def create_new_line(
    category: str,
    company_name: str,
    description: str,
    link: str,
    gh_link: str,
    alts_names: List[str],
    alts_links: List[str],
) -> str:
    """
    创建新的表格行。

    :param category: 类别
    :param company_name: 公司名称
    :param description: 描述
    :param link: 公司官网链接
    :param gh_link: GitHub仓库链接
    :param alts_names: 替代品名称列表
    :param alts_links: 替代品链接列表
    :return: 新的表格行
    """
    return "{}|{}|{}|{}|{}|\n".format(
        category.strip(),
        f"[{company_name.strip()}]({link.strip()})",
        description.strip(),
        f'<a href={gh_link.strip()}><img src="{create_shield_link(gh_link)}" width=150/></a>',
        create_alternatives_md(alts_names, alts_links),
    )


def read_file(filepath: str) -> List[str]:
    """
    读取文件内容。

    :param filepath: 文件路径
    :return: 文件内容列表
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()


def write_file(filepath: str, content: List[str]) -> None:
    """
    写入文件内容。

    :param filepath: 文件路径
    :param content: 文件内容列表
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(content)


def add_new_company(
    category: str,
    company_name: str,
    description: str,
    link: str,
    gh_link: str,
    alts_names: List[str],
    alts_links: List[str],
) -> str:
    """
    添加新公司到README文件。

    :param category: 类别
    :param company_name: 公司名称
    :param description: 描述
    :param link: 公司官网链接
    :param gh_link: GitHub仓库链接
    :param alts_names: 替代品名称列表
    :param alts_links: 替代品链接列表
    :return: 操作结果
    """
    all_lines = read_file("README.md")
    table_start = "|Category|Company|Description|GitHub Stars|Alternative to|\n"
    table_end = "<!-- END STARTUP LIST -->\n"

    idx = all_lines.index(table_start)
    idx_end = all_lines.index(table_end)

    # 提取现有的类别和公司名称
    find_name = lambda x: x[x.index("[") + 1 : x.index("]")].strip()
    find_cat = lambda x: x[: x.index("|")].strip()
    categories = [(find_cat(line), find_name(line)) for line in all_lines[idx + 2 : idx_end - 1]]

    search_tup = (category.strip(), company_name.strip())

    # 检查是否已存在
    for i, tup in enumerate(reversed(categories)):
        if search_tup == tup:
            return "此条目已存在"
        elif search_tup > tup:
            insert_idx = len(categories) - i
            break
    else:
        insert_idx = len(categories)

    # 添加新行
    all_lines.insert(
        insert_idx + idx + 2,
        create_new_line(category, company_name, description, link, gh_link, alts_names, alts_links),
    )
    write_file("README.md", all_lines)
    return "公司已成功添加！"


def prompt_user_input() -> dict:
    """
    从命令行获取用户输入。

    :return: 用户输入的参数字典
    """
    inputs = {
        "company_name": input("请输入公司名称（例如：Metabase）：\n").strip(),
        "category": input("请输入公司类别（例如：商业智能）：\n").strip(),
        "description": input("请输入公司描述（简短且清晰）：\n").strip(),
        "link": input("请输入公司官网链接（例如：https://www.metabase.com/）：\n").strip(),
        "gh_link": input("请输入GitHub仓库链接（例如：https://github.com/metabase/metabase）：\n").strip(),
        "alts_names": input("请输入替代品名称列表（用逗号分隔）：\n").strip().split(","),
        "alts_links": input("请输入对应的替代品链接列表（用逗号分隔）：\n").strip().split(","),
    }
    return inputs


def main():
    """
    主函数：从命令行获取输入并添加新公司。
    """
    args = prompt_user_input()
    result = add_new_company(**args)
    print(result)


if __name__ == "__main__":
    main()
