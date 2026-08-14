"""主操作窗口"""
import customtkinter as ctk
from tkinter import messagebox
from utils.data_manager import get_data_manager
from ui.change_password import ChangePasswordDialog
from ui.change_school import ChangeSchoolDialog


class MainWindow(ctk.CTk):
    """主操作窗口"""
    
    def __init__(self):
        super().__init__()
        
        self.title("管理中心 - 学校账号管理系统")
        self.geometry("800x650")
        self.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.data_manager = get_data_manager()
        
        self.setup_ui()
        
        # 监听窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        width = 800
        height = 650
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """设置UI布局"""
        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame,
            text="⚙️ 管理中心",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 30))
        
        # 账号信息卡片
        self.info_card = self.create_info_card(main_frame)
        self.info_card.pack(fill="x", pady=(0, 40))
        
        # 操作按钮区域
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(expand=True, fill="both")
        
        # 修改密码按钮
        change_pwd_button = ctk.CTkButton(
            action_frame,
            text="🔐 修改密码",
            width=320,
            height=100,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9",
            corner_radius=10,
            command=self.open_change_password_dialog
        )
        change_pwd_button.pack(pady=15)
        
        # 修改学校绑定按钮
        change_school_button = ctk.CTkButton(
            action_frame,
            text="🏫 修改绑定学校",
            width=320,
            height=100,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#2CC985",
            hover_color="#27AE60",
            corner_radius=10,
            command=self.open_change_school_dialog
        )
        change_school_button.pack(pady=15)
        
        # 底部按钮容器
        bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        bottom_frame.pack(pady=20)
        
        # 刷新按钮
        refresh_button = ctk.CTkButton(
            bottom_frame,
            text="🔄 刷新",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="gray40",
            hover_color="gray30",
            command=self.refresh_info
        )
        refresh_button.pack(side="left", padx=10)
        
        # 退出按钮
        exit_button = ctk.CTkButton(
            bottom_frame,
            text="退出登录",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.logout
        )
        exit_button.pack(side="left", padx=10)
    
    def create_info_card(self, parent):
        """创建账号信息卡片"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        
        # 获取管理员信息
        admin_info = self.data_manager.get_admin_info()
        username = admin_info.get('username', 'N/A')
        bound_school = admin_info.get('bound_school', '未绑定')
        
        # 卡片标题
        card_title = ctk.CTkLabel(
            card,
            text="📋 当前账号信息",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        card_title.pack(pady=(20, 15), padx=20, fill="x")
        
        # 信息容器
        info_container = ctk.CTkFrame(card, fg_color="gray20", corner_radius=5)
        info_container.pack(pady=(0, 20), padx=20, fill="x")
        
        # 用户名
        username_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        username_frame.pack(fill="x", padx=15, pady=10)
        
        username_label = ctk.CTkLabel(
            username_frame,
            text="👤 用户名：",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        username_label.pack(side="left")
        
        self.username_value = ctk.CTkLabel(
            username_frame,
            text=username,
            font=ctk.CTkFont(size=14),
            text_color="#3498db",
            anchor="w"
        )
        self.username_value.pack(side="left", padx=10)
        
        # 分隔线
        separator = ctk.CTkFrame(info_container, height=1, fg_color="gray30")
        separator.pack(fill="x", padx=15)
        
        # 绑定学校
        school_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        school_frame.pack(fill="x", padx=15, pady=10)
        
        school_label = ctk.CTkLabel(
            school_frame,
            text="🏫 绑定学校：",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        school_label.pack(side="left")
        
        self.school_value = ctk.CTkLabel(
            school_frame,
            text=bound_school,
            font=ctk.CTkFont(size=14),
            text_color="#2CC985",
            anchor="w"
        )
        self.school_value.pack(side="left", padx=10)
        
        return card
    
    def refresh_info(self):
        """刷新账号信息"""
        admin_info = self.data_manager.get_admin_info()
        username = admin_info.get('username', 'N/A')
        bound_school = admin_info.get('bound_school', '未绑定')
        
        self.username_value.configure(text=username)
        self.school_value.configure(text=bound_school)
        
        # 显示提示
        messagebox.showinfo("提示", "信息已刷新", parent=self)
    
    def open_change_password_dialog(self):
        """打开修改密码对话框"""
        dialog = ChangePasswordDialog(self)
        dialog.wait_window()
        # 对话框关闭后刷新信息
        self.refresh_info_silent()
    
    def open_change_school_dialog(self):
        """打开修改学校绑定对话框"""
        dialog = ChangeSchoolDialog(self)
        dialog.wait_window()
        # 对话框关闭后刷新信息
        self.refresh_info_silent()
    
    def refresh_info_silent(self):
        """静默刷新信息（不弹提示）"""
        admin_info = self.data_manager.get_admin_info()
        username = admin_info.get('username', 'N/A')
        bound_school = admin_info.get('bound_school', '未绑定')
        
        self.username_value.configure(text=username)
        self.school_value.configure(text=bound_school)
    
    def logout(self):
        """退出登录"""
        confirm = messagebox.askyesno(
            "确认退出",
            "确定要退出登录吗？",
            parent=self
        )
        
        if confirm:
            self.destroy()
            # 返回登录界面
            from ui.login_window import LoginWindow
            login_window = LoginWindow()
            login_window.mainloop()
    
    def on_closing(self):
        """窗口关闭事件"""
        confirm = messagebox.askyesno(
            "确认退出",
            "确定要退出系统吗？",
            parent=self
        )
        
        if confirm:
            self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

