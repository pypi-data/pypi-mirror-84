# web_texting

#### 介绍

* 实现了脚本自动化运行
* 实现了脚本数据驱动
* 实现了脚本按步骤执行

#### build
```
pip install wheel # 安装wheel模块
pip install twine

python setup.py sdist  # 源码包
python setup.py bdist_wheel  # 打包为无需build的wheel
twine upload dist/*
```
