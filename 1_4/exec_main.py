###读入所需包
###注意，需要保证该测试用例代码与xml_to_excel及xml_function代码在同一文件夹
###或将xml_to_excel及xml_function代码放入C盘当前用户文件夹中
import os
import shutil
import sys
import traceback

import xml_to_excel as xtl

# 征信报告所在目录
#path=r'C:\Users\tobfe\Documents\codespace\parseZx\xml'

path = sys.argv[1]

a = 0
for j in [i for i in os.listdir(path) if i.split('.')[1]=='xml']:
    xtl.xml_to_json(path=path,file_name=j)

    a = a+1
    try:
        if a<2:
            xtl.json_to_df(path=path,file_name='sample.txt',write_mode='w',header=True)
            print(a,j,"成功","overwrite")
        else:
            xtl.json_to_df(path=path,file_name='sample.txt',write_mode='a',header=False)
            print(a,j,"成功","append")
    except Exception as e:
        print(a,j,"失败")
        print("异常：", str(e))
        traceback.print_exc()
        src_file = os.path.join(path, j)
        tar_path = './失败xml'
        shutil.copy(src_file, tar_path)
    os.remove(os.path.join(path, j))
    os.remove(os.path.join(path, 'sample.txt'))


