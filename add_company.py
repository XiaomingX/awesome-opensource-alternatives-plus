"""
本脚本用于将公司信息直接添加到列表中
"""
import os

# 工具函数模块
def get_repo_from_url(url):
    """
    根据 GitHub 地址提取仓库名称。

    :param url: GitHub 仓库地址
    :return: 仓库名称
    """
    idx = url.find(".com/")
    return url[idx + len(".com/") :].strip("/")


def create_alternatives_md(names, links):
    """
    生成替代产品的 Markdown 字符串。

    :param names: 替代产品的名称列表
    :param links: 替代产品的链接列表
    :return: Markdown 格式的字符串
    """
    return ", ".join(
        (f"""[{name.strip()}]({link.strip()})""" for name, link in zip(names, links))
    )


def create_shield_link(gh_link):
    """
    根据 GitHub 地址生成显示星标数量的徽章链接。

    :param gh_link: GitHub 仓库地址
    :return: 徽章链接
    """
    return f"https://img.shields.io/github/stars/{get_repo_from_url(gh_link)}?style=social"


def create_new_line(category, company_name, description, link, gh_link, alts_names, alts_links):
    """
    创建表格中的新行。

    :return: Markdown 格式的新行字符串
    """
    return "{}|{}|{}|{}|{}|\n".format(
        category.strip(),
        f"[{company_name.strip()}]({link.strip()})",
        description.strip(),
        f'<a href={gh_link.strip()}><img src="{create_shield_link(gh_link)}" width=150/></a>',
        create_alternatives_md(alts_names, alts_links),
    )

# 数据处理模块
def add_new_company(category, company_name, description, link, gh_link, alts_names, alts_links):
    """
    将新公司信息添加到 README 文件的表格中。

    :return: 操作结果字符串
    """
    readme_path = "README.md"

    if not os.path.exists(readme_path):
        return f"错误: {readme_path} 文件不存在。"

    with open(readme_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    table_start = "|Category|Company|Description|GitHub Stars|Alternative to|\n"
    table_end = "<!-- END STARTUP LIST -->\n"

    try:
        idx = all_lines.index(table_start)
        idx_end = all_lines.index(table_end)
    except ValueError:
        return "表格结构不完整，请检查 README 文件。"

    # 提取现有分类和公司名
    find_name = lambda x: x[x.index("[") + 1 : x.index("]")].strip()
    find_cat = lambda x: x[: x.index("|")].strip()
    categories = [(find_cat(line), find_name(line)) for line in all_lines[idx + 2 : idx_end - 1]]

    # 检查是否已存在
    search_tup = (category.strip(), company_name.strip())
    if search_tup in categories:
        return "该条目已存在。"

    # 找到插入位置
    insert_idx = next(
        (i for i, tup in enumerate(reversed(categories)) if search_tup > tup),
        len(categories),
    )
    all_lines.insert(
        insert_idx + idx + 2,
        create_new_line(category, company_name, description, link, gh_link, alts_names, alts_links),
    )

    # 写回文件
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(all_lines)

    return "成功添加新公司信息！"

# 交互模块
def get_user_input(prompt, split=False):
    """
    获取用户输入。

    :param prompt: 输入提示文字
    :param split: 是否以逗号分隔输入
    :return: 用户输入的字符串或列表
    """
    response = input(prompt)
    return response.split(",") if split else response.strip()


def collect_company_info():
    """
    从用户输入中收集公司信息。

    :return: 公司信息字典
    """
    print("请依次输入以下公司信息：")
    company_info = {
        "company_name": get_user_input("1. 公司名称 (如 Metabase): "),
        "category": get_user_input("2. 公司类别 (如 Business Intelligence): "),
        "description": get_user_input("3. 公司简介 (一行简单描述): "),
        "link": get_user_input("4. 公司官网链接 (如 https://www.metabase.com/): "),
        "gh_link": get_user_input("5. GitHub 仓库链接 (如 https://github.com/metabase/metabase): "),
        "alts_names": get_user_input("6. 替代产品名称 (以逗号分隔): ", split=True),
        "alts_links": get_user_input("7. 替代产品链接 (以逗号分隔): ", split=True),
    }
    return company_info


def add_company_from_command_line():
    """
    从命令行获取信息并添加公司。
    """
    company_info = collect_company_info()
    result = add_new_company(**company_info)
    print(result)


if __name__ == "__main__":
    add_company_from_command_line()
