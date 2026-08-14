"""
学校账号管理系统 - 主程序入口

功能：
1. MAC地址白名单验证
2. 管理员登录
3. 修改密码
4. 修改学校绑定
"""
import sys
import os

# 确保能够导入项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.mac_check_window import MACCheckWindow


def main():
    """主函数：启动MAC验证窗口"""
    try:
        app = MACCheckWindow()
        app.mainloop()
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


