"""Encrypted team handoff; plaintext credentials exist only in memory / OS Keychain."""
import argparse, base64, ctypes, ctypes.util, getpass, json, os, subprocess, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
SERVICE = 'com.sevens.nox-creator-team'
ACCOUNT = 'authorized-api-keys'
PASSWORD_SERVICE = 'com.sevens.nox-creator-team.release-v1.0.0'
PASSWORD_ACCOUNT = 'decryption-password'

def keychain_library():
    if sys.platform != 'darwin':
        raise RuntimeError('此功能使用macOS钥匙串；其他系统请设置运行时NOX_API_KEYS或每次解密。')
    lib = ctypes.CDLL(ctypes.util.find_library('Security'))
    lib.SecKeychainAddGenericPassword.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p]
    lib.SecKeychainFindGenericPassword.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p]
    lib.SecKeychainItemModifyAttributesAndData.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p]
    lib.SecKeychainItemFreeContent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    return lib

def keychain_get(service=SERVICE, account=ACCOUNT):
    lib = keychain_library(); s, a = service.encode(), account.encode()
    size, ptr = ctypes.c_uint32(), ctypes.c_void_p()
    status = lib.SecKeychainFindGenericPassword(None,len(s),s,len(a),a,ctypes.byref(size),ctypes.byref(ptr),None)
    if status != 0: raise RuntimeError(f'钥匙串读取失败({status})，先导入凭证或解锁钥匙串。')
    try: return ctypes.string_at(ptr,size.value)
    finally: lib.SecKeychainItemFreeContent(None,ptr)

def keychain_set(value, service=SERVICE, account=ACCOUNT):
    lib = keychain_library(); s, a = service.encode(), account.encode()
    status = lib.SecKeychainAddGenericPassword(None,len(s),s,len(a),a,len(value),value,None)
    if status == -25299:
        item = ctypes.c_void_p()
        status = lib.SecKeychainFindGenericPassword(None,len(s),s,len(a),a,None,None,ctypes.byref(item))
        if status == 0: status = lib.SecKeychainItemModifyAttributesAndData(item,None,len(value),value)
        ctypes.CDLL(ctypes.util.find_library('CoreFoundation')).CFRelease(ctypes.c_void_p(item.value))
    if status != 0: raise RuntimeError(f'钥匙串写入失败({status})。')

def derive(password, salt):
    return Scrypt(salt=salt,length=32,n=32768,r=8,p=1).derive(password.encode())

def encrypt(keys, password):
    salt, nonce = os.urandom(16), os.urandom(12)
    aad = b'sevens-nox-credentials-v1'
    blob = AESGCM(derive(password,salt)).encrypt(nonce,json.dumps({'keys':keys}).encode(),aad)
    return {'format':'sevens-nox-credentials-v1','kdf':'scrypt-n32768-r8-p1','cipher':'AES-256-GCM',
            'salt':base64.b64encode(salt).decode(),'nonce':base64.b64encode(nonce).decode(),'ciphertext':base64.b64encode(blob).decode()}

def decrypt(payload, password):
    if payload.get('format') != 'sevens-nox-credentials-v1': raise RuntimeError('不支持的凭证包格式。')
    dec = lambda k: base64.b64decode(payload[k],validate=True)
    raw = AESGCM(derive(password,dec('salt'))).decrypt(dec('nonce'),dec('ciphertext'),b'sevens-nox-credentials-v1')
    keys = json.loads(raw)['keys']
    if not isinstance(keys,list) or not keys or not all(isinstance(k,str) and k.startswith('nox_') for k in keys):
        raise RuntimeError('无有效授权凭证。')
    return list(dict.fromkeys(keys))

def load_keys():
    raw = os.environ.get('NOX_API_KEYS') or os.environ.get('NOXINFLUENCER_API_KEY')
    if raw:
        keys = [x.strip() for x in raw.replace(';',',').replace('\n',',').split(',') if x.strip()]
    elif os.environ.get('NOX_CREDENTIALS_FILE'):
        payload = json.loads(Path(os.environ['NOX_CREDENTIALS_FILE']).read_text())
        keys = decrypt(payload,getpass.getpass('凭证包解密口令（不回显）：'))
    else: keys = json.loads(keychain_get())['keys']
    if not keys or not all(k.startswith('nox_') for k in keys): raise RuntimeError('运行时凭证不可用。')
    return list(dict.fromkeys(keys))

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True)
    i=sub.add_parser('import');i.add_argument('encrypted_file')
    sub.add_parser('copy-release-password')
    a=p.parse_args()
    if a.command=='copy-release-password':
        value=keychain_get(PASSWORD_SERVICE,PASSWORD_ACCOUNT)
        subprocess.run(['pbcopy'],input=value,check=True)
        print('解密口令已复制到剪贴板。请通过单独渠道交接；勿粘贴到群聊、NAS说明或Agent提示词。')
    else:
        password=getpass.getpass('凭证包解密口令（不回显）：')
        keys=decrypt(json.loads(Path(a.encrypted_file).read_text()),password)
        keychain_set(json.dumps({'keys':keys}).encode())
        print(f'已将{len(keys)}个授权key导入本机钥匙串，未生成明文文件。')
if __name__=='__main__':
    try: main()
    except Exception: print('凭证操作失败：请检查口令、凭证包和钥匙串权限；敏感细节不输出。',file=sys.stderr);sys.exit(1)
