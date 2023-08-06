from distutils.core import setup

setup(
    name='baizhanSuperMath8',  # 对外我们模块的名字
    version='8.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦',  #描述
    author='kk', # 作者
    author_email='879923435@qq.com',
    py_modules=['baizhanSuperMath8.demo1','baizhanSuperMath8.demo2',"baizhanSuperMath8.my_math.demo3","baizhanSuperMath8.my_math.demo4"] # 要发布的模块
)
