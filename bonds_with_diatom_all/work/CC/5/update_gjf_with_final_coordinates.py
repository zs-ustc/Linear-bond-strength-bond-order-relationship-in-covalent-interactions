import re

def extract_last_coordinates(log_file):
    # Step 1: 读取Gaussian的输出文件，并寻找最后一个"Input orientation"所在的行号
    with open(log_file, 'r') as file:
        lines = file.readlines()

    last_input_orientation_line = None
    for i, line in enumerate(lines):
        if "Input orientation" in line:
            last_input_orientation_line = i

    # 如果没有找到 "Input orientation"，返回空列表
    if last_input_orientation_line is None:
        return []
    print("line:",i)
    # Step 2: 从最后一个 "Input orientation" 行号 + 5 开始读取坐标
    coordinates_block = []
    start_line = last_input_orientation_line + 5

    for line in lines[start_line:]:
        # Step 3: 如果行包含 "-----"，则结束读取
        if "-----" in line:
            break

        # 提取原子编号和坐标 (行格式：Center Number, Atomic Number, X, Y, Z)
        parts = line.split()
        if len(parts) >= 6:
            atom_number = int(parts[1])
            x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
            coordinates_block.append((atom_number, x, y, z))

    return coordinates_block

def update_gjf(input_gjf, output_gjf, coordinates):
    # Step 2: 读取输入GJF文件的头部信息，跳过坐标部分
    with open(input_gjf, 'r') as file:
        lines = file.readlines()

    lines[3] = "#p UM062X/6-311+G** force int=superfine \n"
    gjf_header = lines[:8]
    coords_start = False

    # Step 3: 将提取的坐标更新到GJF文件格式中
    with open(output_gjf, 'w') as file:
        file.writelines(gjf_header)  # 写入头部信息

        for atom_number, x, y, z in coordinates:
            atom_species = "H"
            if atom_number == 6:
                atom_species = "C"
            file.write(f"{atom_species}   {x:.6f}   {y:.6f}   {z:.6f}\n")  # 写入坐标

        file.write("\n")  # 结束坐标部分
        file.writelines(lines[len(gjf_header) + len(coordinates) + 1:])  # 写入剩余内容

for i in range(-40,47):
    factor = 1 + i / 100  # 计算系数 (1 + i/100)
    log_file = "opt/"+f"{(i + 100) * 100:05d}"+"/"+f"opt.log"
    input_gjf = "opt/"+f"{(i + 100) * 100:05d}"+"/"+f"{(i + 100) * 100:05d}.gjf"
    output_gjf  = "force/input/"+f"{(i + 100) * 100:05d}.gjf"

    # 提取最后一帧坐标
    last_coordinates = extract_last_coordinates(log_file)

    # 更新GJF文件
    update_gjf(input_gjf, output_gjf, last_coordinates)

    print("GJF文件已更新完成：",output_gjf)
