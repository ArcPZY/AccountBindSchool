# 学校账号管理工具实现方案

## 技术栈决策

- **GUI框架**：CustomTkinter（现代化UI，轻量级）
- **数据存储**：JSON文件（本地单文件，简单直接）
- **MAC验证**：uuid.getnode()（标准库，跨平台）

## 项目结构

```
AccountBindSchool/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖：customtkinter
├── config.json            # 数据文件（MAC白名单、账号、学校）
├── ui/
│   ├── __init__.py
│   ├── mac_check_window.py    # 步骤1：MAC验证界面
│   ├── login_window.py        # 步骤2：登录界面
│   ├── main_window.py         # 步骤3：主操作界面
│   ├── change_password.py     # 修改密码对话框
│   └── change_school.py       # 修改学校绑定对话框
└── utils/
    ├── __init__.py
    ├── mac_validator.py       # MAC地址验证逻辑
    └── data_manager.py        # JSON数据读写

```

## 核心数据结构 (config.json)

```json
{
  "mac_whitelist": ["AA:BB:CC:DD:EE:FF", "11:22:33:44:55:66"],
  "admin_account": {
    "username": "admin",
    "password": "change-me",
    "bound_school": "北京第一中学"
  },
  "schools": {
    "公办": ["北京第一中学", "上海实验中学", "深圳外国语学校"],
    "民办": ["枫叶国际学校", "德威国际学校", "惠立学校"],
    "高职": ["北京职业技术学院", "上海工艺美术职业学院", "深圳职业技术大学"]
  },
  "api_config": {
    "base_url": "https://api.example.com",
    "endpoints": {
      "change_password": "/admin/password",
      "change_school": "/admin/school"
    }
  }
}
```

## 向导式流程设计

**步骤1：MAC验证窗口** (`mac_check_window.py`)

- 自动获取本机MAC地址
- 对比白名单
- ✅ 通过 → 进入登录界面
- ❌ 失败 → 显示错误，禁止使用

**步骤2：登录窗口** (`login_window.py`)

- 输入用户名、密码
- 验证通过 → 进入主界面
- 显示当前绑定学校（只读）

**步骤3：主操作界面** (`main_window.py`)

- 顶部：显示当前账号信息卡片
- 中间：两个大按钮
  - "修改密码" → 打开修改密码对话框
  - "修改绑定学校" → 打开学校选择对话框
- 底部：退出按钮

**对话框组件**

- `change_password.py`：旧密码验证 + 新密码输入（二次确认）
- `change_school.py`：三个标签页（公办/民办/高职）+ 学校列表单选

## 实现细节

### 1. MAC地址验证 (`utils/mac_validator.py`)

```python
import uuid

def get_mac_address():
    """获取本机MAC地址"""
    mac = uuid.getnode()
    mac_str = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_str

def validate_mac(mac_whitelist):
    """验证MAC地址是否在白名单"""
    current_mac = get_mac_address()
    return current_mac in mac_whitelist
```

### 2. 数据管理器 (`utils/data_manager.py`)

- `load_config()`: 读取JSON
- `save_config(data)`: 写入JSON
- `verify_login(username, password)`: 验证登录
- `update_password(new_password)`: 更新密码
- `update_school(new_school)`: 更新绑定学校
- `get_api_stub()`: 返回API调用方法（预留）

### 3. UI设计要点

**配色方案**：

- 主题：深色模式（CTk默认蓝色）
- 成功：绿色 (#2CC985)
- 错误：红色 (#E74C3C)
- 卡片背景：深灰色

**布局原则**：

- 窗口固定大小 800x600
- 居中显示
- 组件间距统一（padx=20, pady=15）
- 按钮高度40px，圆角5px

**交互反馈**：

- 操作成功：绿色提示框 + 1.5秒后自动关闭
- 操作失败：红色提示框 + 需手动关闭
- 按钮点击：loading状态（禁用+文字变化）

### 4. API预留方案

```python
# 在 data_manager.py 中
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def change_password(self, username, old_pwd, new_pwd):
        # TODO: 实现HTTP请求
        # requests.post(f"{self.base_url}/admin/password", ...)
        pass
    
    def change_school(self, username, school_name):
        # TODO: 实现HTTP请求
        pass
```

当前使用 `raise NotImplementedError("API功能待实现")`

## 错误处理策略

1. **MAC验证失败**：显示当前MAC地址，提示联系管理员添加白名单
2. **登录失败**：清空密码框，焦点回到密码输入
3. **密码修改失败**：

   - 旧密码错误 → 提示重新输入
   - 新密码不一致 → 标红两个输入框

4. **JSON文件损坏**：自动创建默认配置文件
