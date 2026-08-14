"""管理员登录窗口"""
import customtkinter as ctk
from utils.data_manager import get_data_manager


class LoginWindow(ctk.CTk):
    """登录窗口"""
    
    def __init__(self):
        super().__init__()
        
        self.title("管理员登录 - 学校账号管理系统")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.data_manager = get_data_manager()
        
        self.setup_ui()
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        width = 600
        height = 600
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
            text="👤 管理员登录",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        # 副标题
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="请输入您的管理员凭据",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # 登录表单卡片
        form_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        form_frame.pack(fill="x", pady=20)
        
        # 用户名
        username_label = ctk.CTkLabel(
            form_frame,
            text="用户名",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        username_label.pack(pady=(30, 5), padx=40, fill="x")
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="请输入用户名",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=(0, 20), padx=40, fill="x")
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # 密码
        password_label = ctk.CTkLabel(
            form_frame,
            text="密码",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        password_label.pack(pady=(0, 5), padx=40, fill="x")
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="请输入密码",
            show="●",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=(0, 20), padx=40, fill="x")
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # 按钮容器（移到表单内部）
        button_frame_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame_inner.pack(pady=(10, 30), padx=40)
        
        # 登录按钮
        self.login_button = ctk.CTkButton(
            button_frame_inner,
            text="登录",
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.login
        )
        self.login_button.pack(side="left", padx=10)
        
        # 退出按钮
        exit_button = ctk.CTkButton(
            button_frame_inner,
            text="退出",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="gray40",
            hover_color="gray30",
            command=self.quit
        )
        exit_button.pack(side="left", padx=10)
        
        # 错误提示标签
        self.error_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#E74C3C"
        )
        self.error_label.pack(pady=(10, 0))
        
        # 设置焦点
        self.username_entry.focus()
    
    def login(self):
        """执行登录"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # 验证输入
        if not username:
            self.show_error("请输入用户名")
            self.username_entry.focus()
            return
        
        if not password:
            self.show_error("请输入密码")
            self.password_entry.focus()
            return
        
        # 禁用登录按钮
        self.login_button.configure(state="disabled", text="登录中...")
        
        # 验证凭据
        if self.data_manager.verify_login(username, password):
            # 登录成功
            self.show_success("登录成功！正在进入系统...")
            self.after(800, self.open_main_window)
        else:
            # 登录失败
            self.show_error("用户名或密码错误")
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
            self.login_button.configure(state="normal", text="登录")
    
    def show_error(self, message):
        """显示错误信息"""
        self.error_label.configure(text=f"❌ {message}", text_color="#E74C3C")
    
    def show_success(self, message):
        """显示成功信息"""
        self.error_label.configure(text=f"✅ {message}", text_color="#2CC985")
    
    def open_main_window(self):
        """打开主窗口"""
        self.destroy()
        # 导入并显示主窗口
        from ui.main_window import MainWindow
        main_window = MainWindow()
        main_window.mainloop()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

