import os


def read_dir(temp_data_path: list, file_endswith: str):
    """
    该方法是用来读入目录中的所有文件名的绝对路径 并保存在 list中
    :param temp_data_path: 目录绝对路径 构成的一个list
    :param file_endswith: 文件的拓展名后缀 
    :return:
    """
    total_file_path = []  # total_path
    for path in temp_data_path:
        file_name_list = os.listdir(path)  # 返回path指定的文件夹包含的文件或文件夹的名字的列表
        # 把每一个file_name_list的名字和path路径下的文件名拼接  路径拼接为更完整的路径
        file_path_list = [os.path.join(path, i) for i in file_name_list if i.endswith("." + file_endswith)]
        total_file_path.extend(file_path_list)
    return total_file_path
