"""修改密码对话框"""
import customtkinter as ctk
from tkinter import messagebox
from utils.data_manager import get_data_manager


class ChangePasswordDialog(ctk.CTkToplevel):
    """修改密码对话框"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("修改密码")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # 设置为模态对话框
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.center_window()
        
        self.data_manager = get_data_manager()
        
        self.setup_ui()
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        width = 500
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
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔐 修改管理员密码",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 30))
        
        # 表单容器
        form_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        form_frame.pack(fill="both", expand=True)
        
        # 旧密码
        old_pwd_label = ctk.CTkLabel(
            form_frame,
            text="旧密码",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        old_pwd_label.pack(pady=(20, 5), padx=20, fill="x")
        
        self.old_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="请输入旧密码",
            show="●",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.old_password_entry.pack(pady=(0, 15), padx=20, fill="x")
        self.old_password_entry.bind("<Return>", lambda e: self.new_password_entry.focus())
        
        # 新密码
        new_pwd_label = ctk.CTkLabel(
            form_frame,
            text="新密码",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        new_pwd_label.pack(pady=(0, 5), padx=20, fill="x")
        
        self.new_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="请输入新密码（至少6位）",
            show="●",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.new_password_entry.pack(pady=(0, 15), padx=20, fill="x")
        self.new_password_entry.bind("<Return>", lambda e: self.confirm_password_entry.focus())
        
        # 确认新密码
        confirm_pwd_label = ctk.CTkLabel(
            form_frame,
            text="确认新密码",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        confirm_pwd_label.pack(pady=(0, 5), padx=20, fill="x")
        
        self.confirm_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="请再次输入新密码",
            show="●",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.confirm_password_entry.pack(pady=(0, 20), padx=20, fill="x")
        self.confirm_password_entry.bind("<Return>", lambda e: self.submit())
        
        # 按钮容器
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # 确认按钮
        self.submit_button = ctk.CTkButton(
            button_frame,
            text="确认修改",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2CC985",
            hover_color="#27AE60",
            command=self.submit
        )
        self.submit_button.pack(side="left", padx=10)
        
        # 取消按钮
        cancel_button = ctk.CTkButton(
            button_frame,
            text="取消",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="gray40",
            hover_color="gray30",
            command=self.destroy
        )
        cancel_button.pack(side="left", padx=10)
        
        # 设置焦点
        self.old_password_entry.focus()
    
    def submit(self):
        """提交修改"""
        old_pwd = self.old_password_entry.get().strip()
        new_pwd = self.new_password_entry.get().strip()
        confirm_pwd = self.confirm_password_entry.get().strip()
        
        # 验证输入
        if not old_pwd:
            messagebox.showerror("错误", "请输入旧密码", parent=self)
            self.old_password_entry.focus()
            return
        
        if not new_pwd:
            messagebox.showerror("错误", "请输入新密码", parent=self)
            self.new_password_entry.focus()
            return
        
        if len(new_pwd) < 6:
            messagebox.showerror("错误", "新密码长度至少6位", parent=self)
            self.new_password_entry.focus()
            return
        
        if new_pwd != confirm_pwd:
            messagebox.showerror("错误", "两次输入的新密码不一致", parent=self)
            self.confirm_password_entry.delete(0, "end")
            self.confirm_password_entry.focus()
            return
        
        # 禁用按钮
        self.submit_button.configure(state="disabled", text="修改中...")
        
        # 执行修改
        success, message = self.data_manager.update_password(old_pwd, new_pwd)
        
        if success:
            messagebox.showinfo("成功", message, parent=self)
            self.destroy()
        else:
            messagebox.showerror("失败", message, parent=self)
            self.old_password_entry.delete(0, "end")
            self.old_password_entry.focus()
            self.submit_button.configure(state="normal", text="确认修改")


if __name__ == "__main__":
    # 测试用
    root = ctk.CTk()
    root.withdraw()
    dialog = ChangePasswordDialog(root)
    root.mainloop()


