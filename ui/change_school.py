"""修改学校绑定对话框"""
import customtkinter as ctk
from tkinter import messagebox
from utils.data_manager import get_data_manager


class ChangeSchoolDialog(ctk.CTkToplevel):
    """修改学校绑定对话框"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("修改绑定学校")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # 设置为模态对话框
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.center_window()
        
        self.data_manager = get_data_manager()
        self.selected_school = None
        
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
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame,
            text="🏫 选择绑定学校",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        # 当前绑定学校
        current_school = self.data_manager.get_admin_info().get('bound_school', '未绑定')
        current_label = ctk.CTkLabel(
            main_frame,
            text=f"当前绑定：{current_school}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        current_label.pack(pady=(0, 20))
        
        # 标签页容器
        tabview = ctk.CTkTabview(main_frame, height=320)
        tabview.pack(fill="both", expand=True, pady=10)
        
        # 获取学校数据
        schools_dict = self.data_manager.get_schools()
        
        # 为每种学校类型创建标签页
        self.radio_var = ctk.StringVar(value="")
        
        for school_type, schools in schools_dict.items():
            # 添加标签页
            tab = tabview.add(school_type)
            
            # 创建滚动框
            scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # 添加学校单选按钮
            for school in schools:
                radio = ctk.CTkRadioButton(
                    scroll_frame,
                    text=school,
                    variable=self.radio_var,
                    value=school,
                    font=ctk.CTkFont(size=14),
                    command=lambda s=school: self.on_school_selected(s)
                )
                radio.pack(anchor="w", pady=8, padx=10)
        
        # 选择提示
        self.selection_label = ctk.CTkLabel(
            main_frame,
            text="请选择一个学校",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.selection_label.pack(pady=10)
        
        # 按钮容器
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # 确认按钮
        self.submit_button = ctk.CTkButton(
            button_frame,
            text="确认修改",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2CC985",
            hover_color="#27AE60",
            state="disabled",
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
    
    def on_school_selected(self, school):
        """学校选择回调"""
        self.selected_school = school
        self.selection_label.configure(
            text=f"已选择：{school}",
            text_color="#3498db"
        )
        self.submit_button.configure(state="normal")
    
    def submit(self):
        """提交修改"""
        if not self.selected_school:
            messagebox.showwarning("提示", "请先选择一个学校", parent=self)
            return
        
        # 确认对话框
        confirm = messagebox.askyesno(
            "确认修改",
            f"确定要将绑定学校修改为：\n\n{self.selected_school}\n\n吗？",
            parent=self
        )
        
        if not confirm:
            return
        
        # 禁用按钮
        self.submit_button.configure(state="disabled", text="修改中...")
        
        # 执行修改
        success, message = self.data_manager.update_school(self.selected_school)
        
        if success:
            messagebox.showinfo("成功", message, parent=self)
            self.destroy()
        else:
            messagebox.showerror("失败", message, parent=self)
            self.submit_button.configure(state="normal", text="确认修改")


if __name__ == "__main__":
    # 测试用
    root = ctk.CTk()
    root.withdraw()
    dialog = ChangeSchoolDialog(root)
    root.mainloop()


