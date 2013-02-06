#coding=gbk
'''
@author: zhengpeiyuan@baidu.com
'''


def add_path(path):
    '''添加目录到sys.path中'''
    import sys
    if path not in sys.path:
        sys.path.insert(0, path)


add_path('../bin')
