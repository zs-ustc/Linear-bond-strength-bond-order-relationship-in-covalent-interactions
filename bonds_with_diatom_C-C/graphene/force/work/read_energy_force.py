import os


# 获取所有文件夹名称
all_folders = [folder for folder in os.listdir('.') if os.path.isdir(os.path.join(folder))]

# 提取数字开头的文件夹并排序
sorted_folders = sorted(all_folders, key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else float('inf'))

# 遍历排序后的文件夹
for folder in sorted_folders:
    try:
        # 提取距离值（文件夹名的数字部分）
        distance = (float(folder)/100)/100*1.4245   # 数字除以2
        distance_path = os.path.join('distance.dat')
        with open(distance_path, 'a') as f_dist:
            f_dist.write(f"{distance}\n")  # 追加到distance.dat

        # 读取OUTCAR文件
        outcar_path = os.path.join(folder, 'OUTCAR')
        if not os.path.isfile(outcar_path):
            print(f"OUTCAR not found in {folder}")
            continue

        with open(outcar_path, 'r') as outcar:
            lines = outcar.readlines()

        # 提取体系能量（最后一个”energy  without entropy=“后面的数字）
        energy = None
        for line in reversed(lines):
            if "energy  without entropy=" in line:
                energy = float(line.split()[-1].strip())
                break
        if energy is not None:
            energy_path = os.path.join('energy.dat')
            with open(energy_path, 'a') as f_energy:
                f_energy.write(f"{energy}\n")  # 追加到energy.dat
        else:
            print(f"No energy found in {folder}")

        # 提取z方向应力值（"in kB" 所在行的第五个字符串）
        stress = None
        for line in lines:
            if "in kB" in line:
                stress = float(line.split()[4])  # 第五个字符串
                break
        if stress is not None:
            stress_path = os.path.join('stress.dat')
            with open(stress_path, 'a') as f_stress:
                f_stress.write(f"{stress}\n")  # 追加到stress.dat
        else:
            print(f"No stress found in {folder}")

    except Exception as e:
        print(f"Error processing folder {folder}: {e}")
