import shutil
import os

code = 'pyinstaller -F -w -i main.ico --add-data "src/gif.gif;src/" --add-data "src/bgm.ogg;src/" --add-data "src/bg2.jpg;src/" --add-data "src/ico/advanced.png;src/ico/" --add-data "src/tps/c4.xlsx;src/tps" --add-data "src/tps/c5.xlsx;src/tps" --add-data "src/tps/c6.xlsx;src/tps" --add-data "src/tps/c7.xlsx;src/tps" --add-data "src/tps/c8.xlsx;src/tps" --add-data "src/tps/c9.xlsx;src/tps" --add-data "src/tps/c10.xlsx;src/tps" --add-data "src/tps/c11.xlsx;src/tps" --add-data "src/tps/c12.xlsx;src/tps" main.pyw'

# 假设这是你现有的代码
os.system(code)
os.remove('main.spec')

# 补写的代码：删除 build 文件夹
build_folder = 'build'
if os.path.exists(build_folder) and os.path.isdir(build_folder):
    shutil.rmtree(build_folder)
    print(f"文件夹 {build_folder} 已删除")
else:
    print(f"文件夹 {build_folder} 不存在")

dist_folder = 'dist'
if os.path.exists(dist_folder) and os.path.isdir(dist_folder):
    for filename in os.listdir(dist_folder):
        if filename.endswith('.exe'):
            src_file = os.path.join(dist_folder, filename)
            dst_file = os.path.join(os.getcwd(), filename)
            shutil.copy(src_file, dst_file)
            print(f"文件 {filename} 已拷贝到当前目录")
    shutil.rmtree(dist_folder)
    print(f"文件夹 {dist_folder} 已删除")
