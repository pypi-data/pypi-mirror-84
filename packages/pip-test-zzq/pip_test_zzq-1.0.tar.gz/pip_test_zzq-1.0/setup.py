import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="pip_test_zzq",  # pip包名
    version="1.0",
    author="charycoder",
    author_email="charycoder@163.com",
    description="pip包测试",  # 模块简介
    long_descripiton=long_description,  # 模块详细介绍
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 更多描述信息
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    # 依赖模块
    install_requires=[
        'pandas'
    ],
    python_requires='>=3'
)
