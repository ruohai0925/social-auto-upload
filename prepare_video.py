import os
import shutil
import subprocess
from pathlib import Path

def copy_files():
    # 源目录 - 使用 WSL 格式的 Windows 路径
    source_dir = Path("/mnt/c/Users/yzeng/Codes/crawl/data")
    # 目标目录
    target_dir = Path("videos")
    
    # 确保目标目录存在
    target_dir.mkdir(exist_ok=True)
    
    print(f"源目录: {source_dir}")
    print(f"目标目录: {target_dir.absolute()}")
    
    # 检查源目录是否存在
    if not source_dir.exists():
        print(f"错误: 源目录 {source_dir} 不存在!")
        return
    
    # 记录处理过的文件夹名称
    processed_folders = []
    
    # 遍历源目录下的所有子文件夹
    for subfolder in source_dir.iterdir():
        if not subfolder.is_dir():
            continue
            
        print(f"处理文件夹: {subfolder}")
        
        # 要复制的文件列表
        files_to_copy = ["final_video.mp4", "final_video.jpg", "final_video.txt"]
        
        # 检查并复制每个文件
        for filename in files_to_copy:
            source_file = subfolder / filename
            if source_file.exists():
                # 复制文件，保持原文件名
                shutil.copy2(source_file, target_dir / filename)
                print(f"已复制 {source_file} 到 {target_dir / filename}")
            else:
                print(f"警告: {source_file} 不存在")
        
        # 记录已处理的文件夹名称
        processed_folders.append(subfolder.name)
    
    # 复制完成后运行run_all.sh脚本
    print("\n文件复制完成，开始运行run_all.sh脚本...")
    run_all_script()
    
    # run_all.sh执行完成后，整理文件
    print("\n开始整理处理过的文件...")
    organize_processed_files(processed_folders)

def run_all_script():
    """运行run_all.sh脚本"""
    script_path = Path("run_all.sh")
    
    if not script_path.exists():
        print(f"错误: {script_path} 脚本不存在!")
        return
    
    try:
        print("正在执行run_all.sh脚本...")
        # 使用subprocess.Popen实时显示输出
        process = subprocess.Popen(
            ["bash", str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=Path.cwd()
        )
        
        # 实时读取并显示输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # 等待进程完成并获取返回码
        return_code = process.poll()
        
        if return_code == 0:
            print("run_all.sh脚本执行成功!")
        else:
            print(f"run_all.sh脚本执行失败，返回码: {return_code}")
            
    except Exception as e:
        print(f"执行run_all.sh脚本时发生错误: {e}")

def organize_processed_files(folder_names):
    """整理处理过的文件到对应的子文件夹"""
    target_dir = Path("videos")
    files_to_move = ["final_video.mp4", "final_video.jpg", "final_video.txt"]
    
    for folder_name in folder_names:
        # 创建子文件夹
        subfolder_path = target_dir / folder_name
        subfolder_path.mkdir(exist_ok=True)
        print(f"创建文件夹: {subfolder_path}")
        
        # 移动文件到子文件夹
        for filename in files_to_move:
            source_file = target_dir / filename
            dest_file = subfolder_path / filename
            
            if source_file.exists():
                shutil.move(str(source_file), str(dest_file))
                print(f"已移动 {filename} 到 {subfolder_path}")
            else:
                print(f"警告: {filename} 不存在，无法移动")
    
    print("文件整理完成!")

if __name__ == "__main__":
    copy_files()
