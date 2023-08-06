#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

# setup(
#     name='gisinfo',
#     version='1.0.0',
#     packages = find_packages(),
#     # Project uses , so ensure
#     install_requires=[
#         "gdal>=3.0.4",
#         # "tensorflow>=1.12.0",
#     ],
#     description='gdal function',
#     # long_description=open("README.rst").read(),
#     long_description=None,
#     url='https://datall.cn',
#     author='YangZeyu',
#     author_email='yangzy@datall.cn',
#     license='Apache License 2.0',
#     # classifiers=[
#     #     'Development Status :: 4 - Beta',
#     #     'Intended Audience :: Developers',
#     #     'Topic :: Software Development :: Build Tools',
#     #     'License :: OSI Approved :: MIT License',
#     #     'Programming Language :: Python :: 3.6',
#     # ],
#     # package_data = {
#     #     # If any package contains *.txt or *.rst files, include them:
#     #     '': ['*.txt', '*.rst'],
#     #     # include any *.msg files found in the 'test' package, too:
#     #     'test': ['*.msg'],
#     # },
#     # The data_files option can be used to specify additional files
#     # needed by the module distribution: configuration files,
#     # message catalogs, data files
#     # data_files=[('etc/xnrpc', ['etc/xnrpc.conf']), ],
#     # cmdclass={'install': CustomInstallCommand},
#     keywords=['gdal'],
#     entry_points={
#         # "xnrpc.registered_commands": [
#         #     "upload = xnrpc.commands.upload:main",
#         #     "register = xnrpc.commands.register:main",
#         # ],
#         "console_scripts": [
#             " gisinfo = gisinfo.__main__:main",
#         ],
#     },
# )
from distutils.core import Extension
setup(name='gisinfo_c',
      version='0.0.5',
      description='Short Time Fourier Transform',
      author='yzy',
      author_email='yangzy@datall.cn',
      URL = "http://pypi.python.org/pypi/",
      requires= ['numpy'], # 定义依赖哪些模块
      packages=find_packages(),
      # ext_modules = [Extension("gisinfo_c", ['gisinfo_c.pyd'])]      cmdclass = {'build_ext': build_ext},
      # ext_modules = [Extension("./geo_info", sources=["./geo_info.c"])]
      )

# from distutils.core import setup as cysetup
# from Cython.Build import cythonize
# cysetup(ext_modules = cythonize(r"D:\yzy\SVN\Research\PackageSample\package_compile\gisinfo_c\geo_info.py",language_level=3),)

