"""
serve_visualizer.py - Web Server nội bộ phục vụ giao diện Trực Quan Hóa (Visualizer).
Tự động mở trình duyệt web và chạy offline 100%.

Cách dùng:
    python serve_visualizer.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    # Cấu hình UTF-8 cho Windows console
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    url = f"http://localhost:{PORT}/index.html"
    print("=" * 70)
    print("⚡ KHỞI ĐỘNG HỆ THỐNG TRỰC QUAN HÓA DEMO CHƯƠNG 4 (PDC LAB)")
    print("=" * 70)
    print(f"  • Thư mục gốc  : {DIRECTORY}")
    print(f"  • Địa chỉ Web  : {url}")
    print(f"  • Trạng thái   : Đang lắng nghe trên cổng {PORT}...")
    print("=" * 70)
    print("💡 Đang mở trình duyệt web của bạn...")

    # Mở trình duyệt sau khi máy chủ sẵn sàng
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Không thể tự động mở trình duyệt: {e}")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Nhấn Ctrl + C để dừng máy chủ web.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng máy chủ web thành công.")

if __name__ == "__main__":
    run()
