#! /usr/bin/python3
from pwn import process, context
from Crypto.Cipher import ARC4
import random
import string

# 设置 pwntools 的上下文
context(os='linux', arch='amd64', log_level='debug')

# 调用 C++ RC4 程序进行加密
def run_rc4_program(key, plaintext):
    # 将明文数据写入 in.txt 文件
    with open("in.txt", "wb") as f:
        f.write(plaintext.encode())

    # 执行 C++ 编写的 RC4 程序
    io = process("./main")

    io.recvuntil(b"Input key:\n")
    # 输入密钥
    io.sendline(key.encode())

    # 等待加密完成并读取 out.txt 中的密文数据
    io.recvuntil(b"Success!\n")  # 等待成功标志
    io.close()
    with open("out.txt", "rb") as f:
        encrypted_data = f.read()

    return encrypted_data

# 使用 PyCryptodome 实现 RC4 加密
def rc4_encrypt_with_pycryptodome(key, plaintext):
    cipher = ARC4.new(key.encode())  # 创建 RC4 加密器
    return cipher.encrypt(plaintext.encode())  # 返回加密后的数据

# 生成随机可见字符数据
def generate_random_data(size=1024):
    # 生成随机可见字符作为密钥（16 字节）
    key = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))

    # 生成随机可见字符作为明文（1024 字节）
    plaintext = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=size))

    return key, plaintext

# 主验证函数
def verify_encryption(count:int):
    for i in range(count):
        # 生成随机密钥和明文
        key, plaintext = generate_random_data()

        # 使用 C++ RC4 加密
        encrypted_data_cplusplus = run_rc4_program(key, plaintext)

        # 使用 PyCryptodome RC4 加密
        encrypted_data_pycryptodome = rc4_encrypt_with_pycryptodome(key, plaintext)

        # 比较两者的加密结果是否一致
        if encrypted_data_cplusplus != encrypted_data_pycryptodome:
            print(f"The {i+1}th test failed!")
            print(f"Key: {key}")
            print(f"Plaintext:\n{plaintext}")
            print(f"C++ Encrypted:\n{encrypted_data_cplusplus.hex()}")
            print(f"PyCryptodome Encrypted:\n{encrypted_data_pycryptodome.hex()}")
            exit(1)
        else:
            print(f"The {i+1}th test passed!")

    print("All tests passed!")

# 运行验证
verify_encryption(100)
