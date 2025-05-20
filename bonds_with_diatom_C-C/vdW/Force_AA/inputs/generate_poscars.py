def modify_z_axis(input_poscar, output_folder, z_values):
    """
    修改POSCAR文件的z轴长度并生成多个文件。
    :param input_poscar: 输入POSCAR文件路径
    :param output_folder: 输出文件夹路径
    :param z_values: z轴长度的列表
    """
    # 读取原始POSCAR
    with open(input_poscar, 'r') as file:
        lines = file.readlines()

    # 确保输出文件夹存在
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 修改 z 轴长度并生成文件
    for z in z_values:
        modified_lines = lines[:]
        # 修改晶格向量第三行 (z 轴)
        lattice_vector_z = modified_lines[4].split()
        lattice_vector_z[2] = f"{z:.3f}"  # 修改 z 值
        modified_lines[4] = "   " + "   ".join(lattice_vector_z) + "\n"

        # 生成输出文件名
        output_file = os.path.join(output_folder, f"POSCAR_{z:.1f}.vasp")
        with open(output_file, 'w') as outfile:
            outfile.writelines(modified_lines)

        print(f"Generated: {output_file}")

# 定义z轴值
z_values = []

# 添加 5.0 到 10.0（步长为 0.1）
z_values += [round(z / 10, 1) for z in range(50, 101)]

# 添加 10.0 到 24.0，间隔逐步增大（10.5、11.0、...，23.0、24.0）
z_values += [z for z in range(10, 24)]
z_values += [round(z + 0.5, 1) for z in range(10, 24, 2)]  # 添加增量序列

# 调用函数
modify_z_axis(input_poscar="POSCAR", output_folder="output_poscars", z_values=z_values)
