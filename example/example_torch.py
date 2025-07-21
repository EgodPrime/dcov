import importlib
import importlib.util
import dcov

library_name = "json" # 假设目标测试对象是torch

"""通过importlib.util 找到目标库的源码路径"""
spec = importlib.util.find_spec(library_name)
origin = spec.origin
assert origin is not None, f"Could not find the origin of the library {library_name}"
print(f"origin of {library_name} is {origin}")

def some_test_func():
    """假设这是一个包含测试执行的函数"""
    pass

"""初始化bitmap"""
dcov.open_bitmap_py()
dcov.clear_bitmap_py()

with dcov.LoaderWrapper() as l: # 用dcov内置的上下文管理器包裹执行过程，从而自动统计覆盖率
    l.add_source(origin) # 将目标库的源码路径加入到LoaderWrapper的检测列表里

    p0 = dcov.count_bits_py() # 测试执行前第一次测覆盖率
    import json
    json.dumps(({"name":"Alice","age": 30, "city": "New York"}))
    p1 = dcov.count_bits_py() # 测试执行后再测一次
    print(p0)
    print(p1)
    if p1>p0: # 如果覆盖率增长了就做一些事情
        print(f"coverage increased to {p1}")

dcov.close_bitmap_py() # 测完了之后记得关闭bitmap


