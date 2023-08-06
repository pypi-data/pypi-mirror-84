from distutils.core import setup
setup(
    name='zheng',  # 对 外 我 们 模 块 的 名 字
    version='1.0',    # 版 本 号
    description='这是第一个对外发布的模块，简单的测试哦',   # 描 述
    author='huaye',   # 作 者
    author_email='huaye@163.com',
    py_modules=['zheng.demol_A','zheng.demol_B']  # 要 发 布 的 模 块
)
