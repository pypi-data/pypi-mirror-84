"""
boilee v1.0.0
An easy way to create a tool to generate code boilerplates like "npm init" and "vue create" for any programming language.
url: https://github.com/vadolasi/boilee
author: Vitor Daniel
email: vitor036daniel@gmail.com
license: GNU General Public License (GPL)
"""

doc = __doc__.split("\n")[1:-1]

__title__ = doc[0].split(" v")[0]
__version__ = doc[0].split(" v")[1]
__summary__ = doc[1]
__uri__ = doc[2].split(": ")[1]
__author__ = doc[3].split(": ")[1]
__email__ = doc[4].split(": ")[1]
__license__ = doc[5].split(": ")[1]
