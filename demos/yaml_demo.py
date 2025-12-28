
import yaml

def demo_1():
    data = {
        "simple_list": [1, 2, 3],
        "nested": {
            "items": ["a", "b", "c"]
        }
    }

    # data = {"name": "John", "age": 30, "city": "New York"}
    # 列表也使用流式风格
    yaml_str = yaml.dump(
        data,
        default_flow_style=None,  # None 表示列表使用流式
        width=float('inf'),
        indent=0
    )

    print(yaml_str)


def demo_2():
    data = {"name": "John", "age": 30, "city": "New York"}

    # 最小化输出 - 单行格式
    yaml_str = yaml.dump(
        data,
        default_flow_style=False,  # 使用流式风格（紧凑）
        width=float('inf'),  # 禁用自动换行
        indent=2,
        allow_unicode=True,
        sort_keys=False,
        explicit_start=False,      # 不添加文档开始标记
        explicit_end=False         # 不添加文档结束标记
        # 保持原始键顺序
    )

    print(yaml_str)

def demo_3():
    data = {
        "name": "John Doe",
        "address": {  # 这个字典应该用流式
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001"
        },
        "hobbies": ["reading", "gaming", "hiking"],  # 这个列表应该用流式
        "projects": [  # 这个列表中的字典也应该用流式
            {"name": "Project A", "status": "active"},
            {"name": "Project B", "status": "completed"}
        ],
        "settings": {  # 深层嵌套用块式
            "server": {
                "host": "localhost",
                "port": 8080
            }
        }
    }

    # 使用 None 让 PyYAML 自动选择
    # 简单结构（单层字典、列表）会用流式
    # 复杂嵌套结构会用块式
    yaml_str = yaml.dump(
        data,
        default_flow_style=None,  # 关键参数：None 表示智能选择
        indent=2,
        width=80,
        allow_unicode=True,
        sort_keys=False
    )

    print(yaml_str)
if __name__ == '__main__':
    demo_1()
    demo_2()
    demo_3()