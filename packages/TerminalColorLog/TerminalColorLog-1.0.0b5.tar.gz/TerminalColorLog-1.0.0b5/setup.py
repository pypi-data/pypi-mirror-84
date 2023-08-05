# coding:utf-8
"""
 * @Author 20261
 * @create 2020/10/30 16:00
 * User: 20261
 * Date: 2020/10/30
 * Created by 20261 on 2020/10/30.
"""
import setuptools
import sys,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


with open('README.md') as readme:
    README = readme.read()



setuptools.setup(
      name='TerminalColorLog',
      version="1.0.0b5",
      description="Print Have Color 's Log For Terminal ",
      author='chenjj100419',
      author_email='2026159790@qq.com',
      url='https://chenjj100419.github.io/WebBlogHtml',
      packages=['terminalcolorlog_pkg'],
      long_description=README,
      long_description_content_type="text/markdown",
      license="General Public License v3",
      platforms=["any"],
      install_requires=[
            'colorama'
      ],
      python_requires='>=3.6',
     )
