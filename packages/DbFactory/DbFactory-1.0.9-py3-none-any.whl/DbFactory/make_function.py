# coding:utf-8
# author caturbhuja
# date   2020/9/11 11:29 上午 
# wechat chending2012 
"""
生成提示功能
"""
import os

i = '''# coding:utf-8
# author caturbhuja
# date   2020/9/11 11:22 上午 
# wechat chending2012 
import inspect

class MixInFunction:
    """"""    
    # --------------------------- 提示命令封装 -----------------------------
    def some_function(self, **kwargs):
        """未来会定义的一些抽象方法"""
        return self.client.generation_func(inspect.stack()[0][3], **kwargs)

    # ---------------------------- Mysql ---------------------------------
    # def select(self, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], **kwargs)
    #
    # def execute(self, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], **kwargs)



'''

demo_func = '''
    def some_function(self, **kwargs):
            """未来会定义的一些抽象方法"""
            return self.client.generation_func(inspect.stack()[0][3], **kwargs)
'''

import redis

print(dir(redis.StrictRedis))
# new_func = demo_func.replace('some_function', 'get')
#
# i = i + new_func
# print(i)
# path = os.path.dirname(os.path.abspath(__file__)) + '/idle_tips.py'
#
# with open(path, 'w') as f:
#     f.write(i)
