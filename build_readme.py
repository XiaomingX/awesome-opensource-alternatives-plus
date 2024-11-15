"""
此文件从 YAML 文件构建 README
"""
import yaml
import os
from add_company import add_new_company


def load_yaml_file(file_path):
    """
    加载单个 YAML 文件并返回其内容
    :param file_path: YAML 文件路径
    :return: 文件内容解析后的 Python 对象
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.load(file, yaml.Loader)


def parse_all_yamls(directory):
    """
    解析指定目录下所有 YAML 文件
    :param directory: 存放 YAML 文件的目录
    :return: 包含所有文件内容的列表
    """
    yamls_content = []
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            yamls_content.append(load_yaml_file(file_path))
    return yamls_content


def process_companies(directory):
    """
    加载所有 YAML 文件并调用添加公司函数
    :param directory: 存放 YAML 文件的目录
    """
    yaml_data = parse_all_yamls(directory)
    for company_data in yaml_data:
        add_new_company(**company_data)


if __name__ == "__main__":
    # 设置存放 YAML 文件的目录
    yaml_directory = "submissions"
    # 构建公司列表
    process_companies(yaml_directory)
