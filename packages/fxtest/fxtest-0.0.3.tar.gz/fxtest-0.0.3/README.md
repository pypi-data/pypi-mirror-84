## fxtest 安装方式
pip install fxtest
# fxtest


fxtest -h 可以查看用法

fxtest --project project_name 创建你的测试项目

fxtest -r project_name 可以执行你的项目
备注：要确保已经安装了allure 否则只会生成普通的report 不会生成allure 报告，确保ui自动化已经安装了浏览器驱动




请先按照以下步骤安装allure 
1.打开powershell 
2.输入以下命令"Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
3.然后输入 "iwr -useb get.scoop.sh | iex" (备注如果无法解析地址 可以在hosts 文件添加 199.232.68.133 raw.githubusercontent.com )
具体可以参考"https://github.com/lukesampson/scoop"
4.安装后后 输入 "scoop install allure"
allure 可以参考 "https://docs.qameta.io/allure/"
5.最后 "allure -v" 确认安装成功


关于脚本里面，所有的test 类都必须继承 fxtest.TestCase
最好在每个测试函数下面加上对这个测试的描述，以便在结果中得知该项测试的内容
比如：

def test():
  """ test login"""
  
脚本的最后都是用fxtest.main()执行
fxtest main 包括了参数 浏览器类型，执行文件，和 cmd 
cmd 等于pytest  你想添加的参数


## fxtest 定位元素

fxtest 提供了8中定位方式，与Selenium保持一致。

* id_
* name
* class_name
* tag
* link_text
* partial_link_text
* css
* xpath

### 使用方式

```py
import fxtest
import pytest


class YouTest(fxtest.TestCase):

    def test_case(self):
        """a simple test case """
        self.open("https://www.baidu.com")
        self.type(id_="kw", text="seldom")
        self.click(css="#su")
        


```

点击`click()`和输入`type()`的时候直接使用。

__帮助信息：__

* [CSS选择器](https://www.w3school.com.cn/cssref/css_selectors.asp)
* [xpath语法](https://www.w3school.com.cn/xpath/xpath_syntax.asp)

### 定位一组元素

有时候我们通过一种定位写法不能找到单个元素，需要在一种定位方式中使用下标，在seldom中可以通过`index`指定下标。

* selenium中的写法

```py
driver.find_elements_by_tag_name("input")[7].send_keys("selenium")
```

* seldom中的写法

```py
self.type(tag="input", index=7, text="seldom")
```

在seldom中不指定`index`默认下标为`0`。


### 8种定位用法

```html
<form id="form" class="fm" action="/s" name="f">
    <span class="bg s_ipt_wr quickdelete-wrap">
        <input id="kw" class="s_ipt" name="wd">
```

定位方式：

```python
self.type(id_="kw", text="seldom")
self.type(name="wd", text="seldom")
self.type(class_name="s_ipt", text="seldom")
self.type(tag="input", text="seldom")
self.type(link_text="hao123", text="seldom")
self.type(partial_link_text="hao", text="seldom")
self.type(xpath="//input[@id='kw']", text="seldom")
self.type(css="#kw", text="seldom")

```

帮助：

* [CSS选择器](https://www.w3school.com.cn/cssref/css_selectors.asp)
* [xpath语法](https://www.w3school.com.cn/xpath/xpath_syntax.asp)
