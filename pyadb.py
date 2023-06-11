import urllib.request
import zipfile
import os
import json
import re

with open('config.json', 'r') as f:
    config = json.load(f)
url = 'https://dl.google.com/android/repository/platform-tools_r34.0.3-windows.zip?hl=zh-cn'
def download_adb():
    # 检查adb目录是否存在，如果不存在则创建它
    if not os.path.exists('adb'):
        os.makedirs('adb')
    # 下载文件
    urllib.request.urlretrieve(url, 'platform-tools.zip')
    # 解压缩文件
    with zipfile.ZipFile('platform-tools.zip', 'r') as zip_ref:
        zip_ref.extractall('adb')
    # 删除zip文件
    os.remove('platform-tools.zip')
    project_path = os.path.abspath(os.path.dirname(__file__))
    adb_path = os.path.join(project_path, 'adb/platform-tools/adb.exe')
    config['adb_path'] = adb_path
    with open('config.json', 'w') as f:
        json.dump(config, f)
    print('ADB已安装完成并写入config')
    return adb_path


def get_bluestacks_adb_port():
    # 读取bluestacks.conf文件
    bluestacks_adb_port_keys = config.get('bluestacks_adb_port_keys', [])
    bluestacks_conf_path = config.get('bluestacks_conf_path', 'C:/ProgramData/BlueStacks_nxt_cn/bluestacks.conf')
    if not os.path.exists(bluestacks_conf_path):
        print(f'Error: 文件"{bluestacks_conf_path}"不存在')
    else:
        with open(bluestacks_conf_path, 'r') as f:
            conf = f.read()

    # 使用正则表达式匹配adb端口号
    for key in bluestacks_adb_port_keys:
        match = re.search(rf'{key}="(\d+)"', conf)
        if match:
            adb_port = match.group(1)
            return adb_port
    return None

def check_device_connection():
    with open('config.json', 'r') as f:
        config = json.load(f)
    adb_path = config['adb_path']
    # 检查是否已连接设备
    device = None  # 初始化device变量为None
    output = os.popen(f'{adb_path} devices').read().strip().split('\n')
    if len(output) <= 1 or output[0] != 'List of devices attached':
        print('Error: 无设备，尝试连接adb_address')
        if 'adb_address' in config and config['adb_address']:
            device = config['adb_address']
            os.system(f'{adb_path} connect {device}')
            output = os.popen(f'{adb_path} devices').read().strip().split('\n')
            if len(output) <= 1 or output[0] != 'List of devices attached':
                print('Error: 无法连接adb_address，尝试连接蓝叠')
                blurestack=connect_bluestack()
                if not blurestack:
                    return None
                else:
                    return blurestack
            else:
                print(f'已连接设备：{device}')
                device_id = device
                config['device_id'] = device_id
                return device
        else:
            print('Error:adb_address为空，尝试连接蓝叠')
            blurestack=connect_bluestack()
            if not blurestack:
                return None
            else:
                return blurestack
    else:
        for line in output[1:]:
            if not line.endswith('\tdevice'):
                continue
            elif line.endswith('\tdevice'):
                device =line.split('\t')[0]
                break
        if not device:
            print('Error: 设备未连接')
            return None
        else:
            print(f'已连接设备：{device}')
            return device

def connect_bluestack():
    adb_path = config['adb_path']
    device = '127.0.0.1:' + get_bluestacks_adb_port()
    os.system(f'{adb_path} connect {device}')
    output = os.popen(f'{adb_path} devices').read().strip().split('\n')
    if len(output) <= 1 or output[0] != 'List of devices attached':
        print('Error: 无法连接蓝叠(列表为空))')
        return None
    else:
        config['adb_address'] = device
        print(f'已连接设备：{device}')
        device_id = device
        config['device_id'] = device_id
        return device
            
def is_adb_connected():
    # 检查adb路径是否存在
    if 'adb_path' in config and os.path.exists(config['adb_path']):
        adb_path = config['adb_path']
    else:
        result = os.system('adb version')
        if result == 0:
            adb_path = 'adb'
        else:
            adb_path = download_adb()
    # 检查adb是否存在
    result = os.system(f'{adb_path} version')
    if result != 0:
        print('Error: adb不在PATH中或未安装')
    else:
        device = check_device_connection()
        return device
    