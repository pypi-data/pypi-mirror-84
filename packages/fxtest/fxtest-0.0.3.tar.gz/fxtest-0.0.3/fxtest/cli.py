import os
from fxtest.logging import log
import argparse
from fxtest import __version__
from fxtest.produce import create
from fxtest.produce import autocase
import subprocess
conftest = """
pytest_plugins = ["pytest-fxtest", "allure_pytest"]
"""

test_sample = """
import fxtest
import pytest

class Test(fxtest.TestCase):

    def test(self):
        self.get("http://192.168.2.55/web/#/login")
        self.assertText(text="登录")

if __name__ == "__main__":
    fxtest.main()

"""

pytest_ini="""
[pytest]
xfail_strict = true
"""

environment="""
Browser=Chrome
Browser.Version=86
Stand=Production
python.Version=3.6
"""

scoop_allure="""
请先按照以下步骤安装allure 
1.打开powershell 
2.输入以下命令"Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
3.然后输入 "iwr -useb get.scoop.sh | iex" (备注如果无法解析地址 可以在hosts 文件添加 199.232.68.133 raw.githubusercontent.com )
具体可以参考"https://github.com/lukesampson/scoop"
4.安装后后 输入 "scoop install allure"
allure 可以参考 "https://docs.qameta.io/allure/"
5.最后 "allure -v" 确认安装成功
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help="show version",
                        dest='version', action='store_true')
    parser.add_argument('--project', help="创建FXTEST的项目")
    parser.add_argument('-r', help="Run Test Case")
    parser.add_argument('--install_allure',action='store_true')
    parser.add_argument("-c", "--create_excel", nargs=2,
                        help="第一个参数excel路径，第二个sheet的名称")
    parser.add_argument("-g", "--generate_case", nargs=3,help="第一个参数excel路径，第二个是生成的py路径，第三个sheet的名称")
    args = parser.parse_args()

    if args.version:
        print("fxtest version {}".format(__version__))

    project_name = args.project
    if project_name:
        create_folder(project_name)
        return 0

    run_file = args.r
    if run_file:
        if verify_allure_is_exist()==1:
            command = "python " + run_file
            os.system(command)
            return 0
        else:
            return 0
    allure_path=args.install_allure
    if allure_path:
        install_allure()
            


    create_excel = args.create_excel
    if create_excel:
        # if create_excel[1] == None:
        #     create.create_excel(path=create_excel[0])
        # else:
        print(create_excel[0])
        create.create_excel(
            path=create_excel[0], sheet_name=create_excel[1])
        return 0

    generate_case = args.generate_case
    if args.generate_case:
        autocase.create_test_case(
            path=generate_case[0], py_path=generate_case[1], sheet_name=generate_case[2])
        return 0

def verify_allure_is_exist():
    allure_verify="allure --version"
    res=os.system(allure_verify)
    if res == 0:
        return 1
    else:
        log.info("allure 未安装，请先 fxtest --install-allure 安装allure")
        return 0

def install_allure():

    print(scoop_allure)

def create_folder(project_name):
    if os.path.isdir(project_name):
        log.info(
            u"Folder {} exists, please specify a new folder name.".format(project_name))
        return

    log.info("Start to create new test project: {}".format(project_name))
    log.info("CWD: {}\n".format(os.getcwd()))

    def create_folder(path):
        os.makedirs(path)
        msg = "created folder: {}".format(path)
        log.info(msg)

    def create_file(path, file_content=""):
        with open(path, 'w', encoding="utf-8") as f:
            f.write(file_content)
        msg = "created file: {}".format(path)
        log.info(msg)
    

    create_folder(project_name)
    create_folder(os.path.join(project_name, "test_case"))
    create_folder(os.path.join(project_name, "resource"))
    create_folder(os.path.join(project_name, "libs"))
    create_file(os.path.join(project_name, "conftest.py"),conftest)
    create_file(os.path.join(project_name,"pytest.ini"),pytest_ini)
    create_file(os.path.join(project_name, "test_case",
                             "test_sample.py"), file_content=test_sample)


if __name__ == "__main__":
    main()
