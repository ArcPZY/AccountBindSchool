"""数据管理模块 - 处理config.json的读写和业务逻辑"""
import json
import os
from typing import Dict, List, Optional, Tuple


class DataManager:
    """数据管理器"""
    
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            # 如果文件不存在，创建默认配置
            default_config = {
                "mac_whitelist": [],
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
            self._save_config(default_config)
            return default_config
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise Exception(f"配置文件加载失败: {str(e)}")
    
    def _save_config(self, config: Dict = None):
        """保存配置到文件"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise Exception(f"配置文件保存失败: {str(e)}")
    
    def get_mac_whitelist(self) -> List[str]:
        """获取MAC白名单"""
        return self.config.get('mac_whitelist', [])
    
    def add_mac_to_whitelist(self, mac_address: str):
        """添加MAC地址到白名单"""
        if mac_address not in self.config['mac_whitelist']:
            self.config['mac_whitelist'].append(mac_address)
            self._save_config()
    
    def verify_login(self, username: str, password: str) -> bool:
        """验证登录凭据
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            bool: 验证是否通过
        """
        admin = self.config.get('admin_account', {})
        return admin.get('username') == username and admin.get('password') == password
    
    def get_admin_info(self) -> Dict:
        """获取管理员信息"""
        return self.config.get('admin_account', {})
    
    def update_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """更新管理员密码
        
        Args:
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            tuple: (是否成功, 消息)
        """
        admin = self.config.get('admin_account', {})
        
        if admin.get('password') != old_password:
            return False, "旧密码错误"
        
        if len(new_password) < 6:
            return False, "新密码长度至少6位"
        
        # 本地更新
        self.config['admin_account']['password'] = new_password
        self._save_config()
        
        # TODO: 调用API更新后端
        # self._api_change_password(admin['username'], old_password, new_password)
        
        return True, "密码修改成功"
    
    def update_school(self, new_school: str) -> Tuple[bool, str]:
        """更新管理员绑定学校
        
        Args:
            new_school: 新学校名称
            
        Returns:
            tuple: (是否成功, 消息)
        """
        # 验证学校是否在列表中
        schools = self.config.get('schools', {})
        all_schools = []
        for school_list in schools.values():
            all_schools.extend(school_list)
        
        if new_school not in all_schools:
            return False, "学校不在可选列表中"
        
        # 本地更新
        old_school = self.config['admin_account'].get('bound_school', '')
        self.config['admin_account']['bound_school'] = new_school
        self._save_config()
        
        # TODO: 调用API更新后端
        # self._api_change_school(self.config['admin_account']['username'], new_school)
        
        return True, f"学校已从 {old_school} 更改为 {new_school}"
    
    def get_schools(self) -> Dict[str, List[str]]:
        """获取学校列表（按类型分组）"""
        return self.config.get('schools', {})
    
    def get_school_types(self) -> List[str]:
        """获取学校类型列表"""
        return list(self.config.get('schools', {}).keys())
    
    # API预留方法
    def _api_change_password(self, username: str, old_pwd: str, new_pwd: str):
        """调用后端API修改密码（待实现）"""
        # TODO: 实现HTTP请求
        # import requests
        # api_config = self.config.get('api_config', {})
        # base_url = api_config.get('base_url')
        # endpoint = api_config.get('endpoints', {}).get('change_password')
        # response = requests.post(f"{base_url}{endpoint}", json={
        #     'username': username,
        #     'old_password': old_pwd,
        #     'new_password': new_pwd
        # })
        # return response.json()
        pass
    
    def _api_change_school(self, username: str, school_name: str):
        """调用后端API修改学校绑定（待实现）"""
        # TODO: 实现HTTP请求
        pass


# 全局单例
_data_manager_instance = None

def get_data_manager() -> DataManager:
    """获取DataManager单例"""
    global _data_manager_instance
    if _data_manager_instance is None:
        _data_manager_instance = DataManager()
    return _data_manager_instance

