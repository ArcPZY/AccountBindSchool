"""MAC地址验证窗口"""
import customtkinter as ctk
from utils.mac_validator import get_mac_address, validate_mac
from utils.data_manager import get_data_manager


class MACCheckWindow(ctk.CTk):
    """MAC地址验证窗口"""
    
    def __init__(self):
        super().__init__()
        
        self.title("设备验证 - 学校账号管理系统")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.data_manager = get_data_manager()
        self.current_mac = get_mac_address()
        
        self.setup_ui()
        
        # 自动验证MAC地址
        self.after(500, self.check_mac)
    
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
            text="🔒 设备身份验证",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 副标题
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="正在验证您的设备是否有权使用本系统...",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # 信息卡片
        info_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        info_frame.pack(fill="x", pady=20)
        
        # MAC地址显示
        mac_title = ctk.CTkLabel(
            info_frame,
            text="本机MAC地址",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        mac_title.pack(pady=(20, 5))
        
        self.mac_value_label = ctk.CTkLabel(
            info_frame,
            text=self.current_mac,
            font=ctk.CTkFont(size=18, family="Consolas"),
            text_color="#3498db"
        )
        self.mac_value_label.pack(pady=(0, 20))
        
        # 验证状态
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="⏳ 正在验证...",
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=30)
        
        # 进度条
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        self.progress_bar.start()
        
        # 按钮容器（初始隐藏）
        self.button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        # 继续按钮（验证通过后显示）
        self.continue_button = ctk.CTkButton(
            self.button_frame,
            text="继续登录",
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.on_continue
        )
        
        # 退出按钮
        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="退出",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.quit
        )
    
    def check_mac(self):
        """检查MAC地址"""
        mac_whitelist = self.data_manager.get_mac_whitelist()
        is_valid, current_mac = validate_mac(mac_whitelist)
        
        # 停止进度条
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        if is_valid:
            # 验证通过
            self.status_label.configure(
                text="✅ 验证通过！设备已授权",
                text_color="#2CC985"
            )
            self.continue_button.pack(pady=10)
        else:
            # 验证失败
            self.status_label.configure(
                text="❌ 验证失败！设备未授权",
                text_color="#E74C3C"
            )
            
            # 显示错误信息
            error_label = ctk.CTkLabel(
                self.button_frame,
                text=f"您的设备MAC地址不在白名单中\n请联系管理员添加授权后使用",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            error_label.pack(pady=(10, 20))
            
            # 只显示退出按钮
            self.exit_button.pack(pady=5)
    
    def on_continue(self):
        """继续到登录界面"""
        self.destroy()
        # 导入并显示登录窗口
        from ui.login_window import LoginWindow
        login_window = LoginWindow()
        login_window.mainloop()


if __name__ == "__main__":
    app = MACCheckWindow()
    app.mainloop()

