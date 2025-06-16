import numpy as np

def read_gjf(filename):
    """读取Gaussian输入文件并提取从第九行开始的分子结构坐标"""
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 提取文件头（前8行）
    header = lines[:8]
    lines[1]="%mem=8GB\n"
    lines[2]="%nprocshared=8\n"
    lines[3]="#p opt UM062X/6-311+G** nosymm int=superfine SCF=NoVarAcc\n"
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
            if f"{atom}" == "C":
                file.write(f"{atom} -1 {coord[0]: .8f} {coord[1]: .8f} {coord[2]: .8f}\n")
            else:
                file.write(f"{atom} 0 {coord[0]: .8f} {coord[1]: .8f} {coord[2]: .8f}\n")
        file.write("\n")


def modify_x_coordinates(coordinates, delta):
    """对正的x坐标加delta，负的x坐标减delta"""
    new_coordinates = []
    for atom, coord in coordinates:
        new_coord = np.copy(coord)
        if new_coord[0] > 0:  # 如果x坐标为正
            new_coord[0] += delta
        elif new_coord[0] < 0:  # 如果x坐标为负
            new_coord[0] -= delta
        new_coordinates.append((atom, new_coord))
    return new_coordinates


def main():
    input_filename = '00010.gjf'

    # 读取原始文件
    header, coordinates = read_gjf(input_filename)

    delta = 0.025  # 每次变化的增量
    iteration = 0  # 用于文件名的计数

    while True:
        # 检查第一行x坐标的绝对值是否超过2.2826
        first_atom, first_coord = coordinates[0]
        if abs(first_coord[0]) > 2.2826:
            break

        # 生成新的文件名
        output_filename = f"input/{(iteration+3)*5:05d}.gjf"

        # 保存新的文件
        write_gjf(output_filename, header, coordinates)

        # 修改x坐标
        coordinates = modify_x_coordinates(coordinates, delta)

        iteration += 1


if __name__ == "__main__":
    main()
