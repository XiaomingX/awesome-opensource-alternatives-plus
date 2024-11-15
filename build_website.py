import yaml
import os


def remove_github_com(url: str) -> str:
    """移除 GitHub URL 中的 'https://github.com/' 部分"""
    return url.replace("https://github.com/", "")


def remove_https(url: str) -> str:
    """移除 URL 中的 'https://' 或 'http://' 部分，并去除末尾的斜杠"""
    url = url.replace("https://", "").replace("http://", "")
    return url.strip("/")


def apply_special_mapping(value: str, mapping: dict) -> str:
    """根据特定映射规则替换值"""
    return mapping.get(value, value)


def load_yaml_files(directory: str, mapping: dict) -> list:
    """从指定目录加载 YAML 文件并应用映射规则"""
    companies = []
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                data = yaml.load(file, yaml.Loader)
                data["category"] = apply_special_mapping(data["category"], mapping)
                data["company_name"] = apply_special_mapping(data["company_name"], mapping)
                companies.append(data)
    return companies


def extract_categories(companies: list) -> set:
    """提取公司数据中的所有类别"""
    return {company["category"] for company in companies}


def create_directories(categories: set, base_path: str):
    """为每个类别创建对应的目录"""
    for category in categories:
        path = os.path.join(base_path, category)
        if not os.path.exists(path):
            os.makedirs(path)


def generate_alternative_md(alts_names: list, alts_links: list) -> str:
    """生成替代选项的 Markdown 文本"""
    return ", ".join(f"[{name}]({link})" for name, link in zip(alts_names, alts_links))


def generate_markdown_file(company: dict, template: str, output_dir: str):
    """根据公司数据生成 Markdown 文件"""
    file_name = "-".join(company["company_name"].split(" "))
    file_path = os.path.join(output_dir, company["category"], f"{file_name}.md")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(
            template.format(
                company_name=company["company_name"],
                category=company["category"],
                gh_link=company["gh_link"],
                clean_gh_link=remove_github_com(company["gh_link"]),
                link=company["link"],
                clean_link=remove_https(company["link"]),
                description=company["description"],
                alts=generate_alternative_md(company["alts_names"], company["alts_links"]),
            )
        )


def generate_markdown_files(companies: list, template: str, output_dir: str):
    """批量生成所有公司的 Markdown 文件"""
    for company in companies:
        generate_markdown_file(company, template, output_dir)


if __name__ == "__main__":
    # 特殊映射规则
    SPECIAL_MAPPING = {
        "ELT / ETL": "ETL",
        "Robotic Process Automation (RPA)": "Robotic Process Automation",
        "OPAL (Permit.io)": "OPAL",
    }

    # Markdown 模板
    MARKDOWN_TEMPLATE = """
    # {company_name} 

    <a href="{link}"><img src="https://icons.duckduckgo.com/ip3/{clean_link}.ico" alt="Avatar" width="30" height="30" /></a>

    [![GitHub stars](https://img.shields.io/github/stars/{clean_gh_link}.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/{clean_gh_link}/stargazers/) [![GitHub forks](https://img.shields.io/github/forks/{clean_gh_link}.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/{clean_gh_link}/network/) [![GitHub issues](https://img.shields.io/github/issues/{clean_gh_link}.svg)](https://GitHub.com/{clean_gh_link}/issues/)

    [![GitHub license](https://img.shields.io/github/license/{clean_gh_link}.svg)](https://github.com/{clean_gh_link}/blob/master/LICENSE) [![GitHub contributors](https://img.shields.io/github/contributors/{clean_gh_link}.svg)](https://GitHub.com/{clean_gh_link}/graphs/contributors/) 

    **Category**: {category}

    **Github**: [{clean_gh_link}]({gh_link})

    **Website**: [{clean_link}]({link})

    **Description**:
    {description}

    **Alternative to**: {alts}
    """

    # 加载公司数据
    companies = load_yaml_files("submissions", SPECIAL_MAPPING)

    # 提取所有类别
    categories = extract_categories(companies)

    # 创建目录
    create_directories(categories, "website/docs")

    # 生成 Markdown 文件
    generate_markdown_files(companies, MARKDOWN_TEMPLATE, "website/docs")
