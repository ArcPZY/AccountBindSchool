"""MAC地址验证模块"""
import uuid


def get_mac_address():
    """获取本机MAC地址
    
    Returns:
        str: MAC地址，格式如 'AA:BB:CC:DD:EE:FF'
    """
    mac = uuid.getnode()
    mac_str = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_str


def validate_mac(mac_whitelist):
    """验证当前MAC地址是否在白名单中
    
    Args:
        mac_whitelist (list): MAC地址白名单
        
    Returns:
        tuple: (是否通过, 当前MAC地址)
    """
    current_mac = get_mac_address()
    is_valid = current_mac in mac_whitelist
    return is_valid, current_mac
