import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(name='cdmaoapi',
                 version='2.0.0',
                 description='获取/提交编程猫官方数据',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='冷鱼闲风',
                 author_email='2991883280@qq.com',
                 url='http://doc.viyrs.com/cdmaoapi.html',
                 packages=setuptools.find_packages(),
                 install_requires=['requests', ],
                 classifiers=(
                     "Programming Language :: Python",
                     "Operating System :: OS Independent",
                     "License :: OSI Approved :: Apache Software License",
                 ))
