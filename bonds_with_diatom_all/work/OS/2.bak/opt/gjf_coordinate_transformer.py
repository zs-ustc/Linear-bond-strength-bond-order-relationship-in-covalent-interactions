import numpy as np


def read_gjf(filename):
    """读取Gaussian输入文件并提取从第九行开始的分子结构坐标"""
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 提取文件头（前8行）
    header = lines[:8]

    # 提取从第9行开始的原子坐标
    coordinates = []
    for line in lines[8:]:
        parts = line.split()
        if len(parts) == 4:  # 假定原子坐标部分为4列，原子符号+坐标
            atom = parts[0]
            coord = np.array([float(x) for x in parts[1:4]])
            coordinates.append((atom, coord))
        if len(parts) == 5:  # 假定原子坐标部分为4列，原子符号+坐标
            atom = parts[0]
            coord = np.array([float(x) for x in parts[2:5]])
            coordinates.append((atom, coord))
    return header, coordinates


def write_gjf(filename, header, coordinates):
    """写入新的Gaussian输入文件"""
    with open(filename, 'w') as file:
        for line in header:
            file.write(line)
        for atom, coord in coordinates:
            file.write(f"{atom} {coord[0]: .8f} {coord[1]: .8f} {coord[2]: .8f}\n")
        file.write("\n")


def transform_coordinates(coordinates):
    """进行坐标系的平移和旋转"""
    # 获取前三个原子的坐标
    coord1 = coordinates[0][1]  # 第一行原子坐标
    coord2 = coordinates[1][1]  # 第二行原子坐标
    coord3 = coordinates[2][1]  # 第三行原子坐标

    # 计算平移向量（第一和第二个原子的中点）
    translation_vector = (coord1 + coord2) / 2

    # 计算新x轴方向向量（第一和第二个原子构成的向量）
    x_axis = coord2 - coord1
    x_axis /= np.linalg.norm(x_axis)  # 单位化

    # 计算新y轴方向向量（在xy平面上，法向量为新z轴）
    normal_vector = np.cross(coord2 - coord1, coord3 - coord1)
    z_axis = normal_vector / np.linalg.norm(normal_vector)  # 单位化新z轴

    # 新y轴是z轴和x轴的叉乘结果
    y_axis = np.cross(z_axis, x_axis)*-1
    y_axis /= np.linalg.norm(y_axis)  # 单位化

    # 构建旋转矩阵（新坐标系基向量）
    rotation_matrix = np.array([x_axis, y_axis, z_axis])

    # 对所有原子进行平移和旋转
    new_coordinates = []
    for atom, coord in coordinates:
        # 平移
        translated_coord = coord - translation_vector
        # 旋转
        rotated_coord = np.dot(rotation_matrix, translated_coord)
        new_coordinates.append((atom, rotated_coord))

    return new_coordinates


def main():
    input_filename = '10000_updated.gjf'
    output_filename = '10000.gjf'
    # 读取原始文件
    header, coordinates = read_gjf(input_filename)
    # 对坐标进行平移和旋转
    new_coordinates = transform_coordinates(coordinates)
    # 保存新的文件
    write_gjf(output_filename, header, new_coordinates)


if __name__ == "__main__":
    main()
