import os
import hashlib
from pathlib import Path
import shutil

def get_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_base_name(file_path):
    """获取不带扩展名的文件名"""
    return Path(file_path).stem

def compare_directories(dir1, dir2):
    """比较两个目录中的文件，返回比较结果和统计信息"""
    # 获取两个目录中的所有文件
    files1 = {get_base_name(f): f for f in Path(dir1).rglob('*') if f.is_file()}
    files2 = {get_base_name(f): f for f in Path(dir2).rglob('*') if f.is_file()}
    
    # 计算统计信息
    same_name_count = len(set(files1.keys()) & set(files2.keys()))
    diff_name_count = len(files1) + len(files2) - 2 * same_name_count
    
    # 初始化结果字典
    comparison_results = {
        'unique_to_dir1': [],
        'unique_to_dir2': [],
        'different_content': [],
        'stats': {
            'same_name_count': same_name_count,
            'diff_name_count': diff_name_count
        }
    }
    
    # 查找仅在dir1中存在的文件
    for base_name in files1.keys() - files2.keys():
        comparison_results['unique_to_dir1'].append(files1[base_name])
    
    # 查找仅在dir2中存在的文件
    for base_name in files2.keys() - files1.keys():
        comparison_results['unique_to_dir2'].append(files2[base_name])
    
    # 比较内容相同的文件
    for base_name in files1.keys() & files2.keys():
        if get_file_hash(files1[base_name]) != get_file_hash(files2[base_name]):
            comparison_results['different_content'].append((files1[base_name], files2[base_name]))
    
    return comparison_results

def delete_files(files):
    """批量删除文件列表中的所有文件"""
    if not files:
        return
    
    print(f"\n即将删除 {len(files)} 个文件...")
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"删除文件 {file_path} 时出错: {e}")

def main():
    # 获取用户输入
    dir1 = input("请输入第一个目录路径: ").strip()
    dir2 = input("请输入第二个目录路径: ").strip()
    
    # 验证目录是否存在
    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        print("错误：请确保输入的都是有效的目录路径")
        return
    
    # 比较目录
    print("\n正在比较目录...")
    results = compare_directories(dir1, dir2)
    
    # 显示统计信息
    print("\n文件统计:")
    print(f"同名文件数量: {results['stats']['same_name_count']} 个")
    print(f"不同名文件数量: {results['stats']['diff_name_count']} 个")
    
    # 显示详细结果
    print("\n详细比较结果:")
    print(f"\n仅在目录1 ({dir1}) 中存在的文件:")
    for f in results['unique_to_dir1']:
        print(f"  - {f}")
    
    print(f"\n仅在目录2 ({dir2}) 中存在的文件:")
    for f in results['unique_to_dir2']:
        print(f"  - {f}")
    
    print("\n内容不同的文件:")
    for f1, f2 in results['different_content']:
        print(f"  - {f1} <-> {f2}")
    
    # 询问用户是否要删除文件
    if any(results[key] for key in ['unique_to_dir1', 'unique_to_dir2', 'different_content']):
        print("\n清理选项:")
        print("1. 删除仅在目录1中存在的文件")
        print("2. 删除仅在目录2中存在的文件")
        print("3. 不删除任何文件")
        
        choice = input("\n请选择操作 (1/2/3): ").strip()
        
        if choice == '1':
            delete_files(results['unique_to_dir1'])
            print("\n已完成目录1独有文件的删除")
        elif choice == '2':
            delete_files(results['unique_to_dir2'])
            print("\n已完成目录2独有文件的删除")
        else:
            print("不执行删除操作")
    else:
        print("\n两个目录的文件完全相同")

if __name__ == "__main__":
    main()