import tkinter as tk
from tkinter import messagebox, ttk
import os
import winreg
import subprocess

class LDPlayerProxyTool:
    def __init__(self, master):
        self.master = master
        master.title("LDPlayer Proxy Configurator")
        master.geometry("400x500")
        master.resizable(False, False)

        # Style
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))

        # Proxy Type
        self.proxy_type_label = ttk.Label(master, text="Loại Proxy:")
        self.proxy_type_label.pack(pady=(10,5))
        self.proxy_types = ["HTTP", "HTTPS", "SOCKS4", "SOCKS5"]
        self.proxy_type_var = tk.StringVar(value=self.proxy_types[0])
        self.proxy_type_dropdown = ttk.Combobox(master, textvariable=self.proxy_type_var, values=self.proxy_types, state="readonly")
        self.proxy_type_dropdown.pack(pady=(0,10))

        # Proxy Host
        self.host_label = ttk.Label(master, text="Địa chỉ Proxy:")
        self.host_label.pack(pady=(5,5))
        self.host_entry = ttk.Entry(master, width=50)
        self.host_entry.pack(pady=(0,10))

        # Proxy Port
        self.port_label = ttk.Label(master, text="Cổng Proxy:")
        self.port_label.pack(pady=(5,5))
        self.port_entry = ttk.Entry(master, width=50)
        self.port_entry.pack(pady=(0,10))

        # Authentication Frame
        self.auth_frame = ttk.LabelFrame(master, text="Xác Thực (Tùy Chọn)")
        self.auth_frame.pack(pady=10, padx=20, fill="x")

        # Username
        self.username_label = ttk.Label(self.auth_frame, text="Tên Đăng Nhập:")
        self.username_label.pack(pady=(5,5))
        self.username_entry = ttk.Entry(self.auth_frame, width=50)
        self.username_entry.pack(pady=(0,10))

        # Password
        self.password_label = ttk.Label(self.auth_frame, text="Mật Khẩu:")
        self.password_label.pack(pady=(5,5))
        self.password_entry = ttk.Entry(self.auth_frame, show="*", width=50)
        self.password_entry.pack(pady=(0,10))

        # Configure Button
        self.configure_button = ttk.Button(master, text="Cấu Hình Proxy", command=self.configure_proxy)
        self.configure_button.pack(pady=20)

        # Status Label
        self.status_label = ttk.Label(master, text="", foreground="green")
        self.status_label.pack(pady=10)

    def find_ldplayer_path(self):
        """Tìm đường dẫn LDPlayer"""
        possible_paths = [
            r"C:\LDPlayer\LDPlayer9\ldconsole.exe",
            r"D:\LDPlayer\LDPlayer9\ldconsole.exe",
            r"C:\Program Files\LDPlayer\LDPlayer9\ldconsole.exe",
            r"D:\Program Files\LDPlayer\LDPlayer9\ldconsole.exe"
        ]
        
        try:
            # Tìm kiếm trong registry
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, 
                r"SOFTWARE\WOW6432Node\LDPlayer"
            )
            install_path = winreg.QueryValueEx(key, "InstallPath")[0]
            registry_path = os.path.join(install_path, "ldconsole.exe")
            possible_paths.append(registry_path)
        except Exception:
            pass
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None

    def configure_proxy(self):
        # Lấy thông tin từ form
        proxy_type = self.proxy_type_var.get()
        proxy_host = self.host_entry.get().strip()
        proxy_port = self.port_entry.get().strip()
        username = self.username_entry.get().strip() or None
        password = self.password_entry.get().strip() or None

        # Kiểm tra thông tin bắt buộc
        if not proxy_host or not proxy_port:
            messagebox.showerror("Lỗi", "Vui lòng nhập địa chỉ và cổng proxy")
            return

        # Tìm đường dẫn LDPlayer
        ldplayer_path = self.find_ldplayer_path()
        if not ldplayer_path:
            messagebox.showerror("Lỗi", "Không tìm thấy LDPlayer. Vui lòng kiểm tra cài đặt.")
            return

        try:
            # Tạo chuỗi proxy
            proxy_string = f"{proxy_host}:{proxy_port}"
            if username and password:
                proxy_string = f"{username}:{password}@{proxy_string}"

            # Lệnh cấu hình
            config_cmd = f'"{ldplayer_path}" setproxy --index all --proxy {proxy_string}'
            
            # Thực thi lệnh
            result = subprocess.run(config_cmd, shell=True, capture_output=True, text=True)
            
            # Kiểm tra kết quả
            if result.returncode == 0:
                messagebox.showinfo("Thành Công", f"Đã cấu hình proxy {proxy_type} thành công!")
                self.status_label.config(text=f"Proxy: {proxy_string}", foreground="green")
            else:
                messagebox.showerror("Lỗi", f"Không thể cấu hình proxy.\n{result.stderr}")
                self.status_label.config(text="Cấu hình proxy thất bại", foreground="red")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            self.status_label.config(text="Có lỗi xảy ra", foreground="red")

def main():
    root = tk.Tk()
    app = LDPlayerProxyTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
