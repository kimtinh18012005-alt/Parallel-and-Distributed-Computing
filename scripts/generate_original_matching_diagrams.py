# -*- coding: utf-8 -*-
"""
generate_original_matching_diagrams.py
Sinh bộ 6 sơ đồ minh họa CHUẨN XÁC THEO ĐÚNG TỪNG SLIDE CỦA FILE GỐC C4 (Trang 1 đến 8):
1. diag_orig_sequential.png: Xử lý tuần tự theo thứ tự (Trang 2 slide gốc).
2. diag_orig_concurrency_pid.png: HĐH quản lý PID, chia nhỏ task xen kẽ tận dụng thời gian rảnh trên 1 core (Trang 3 & 4 slide gốc).
3. diag_orig_parallel_multicore.png: Xử lý song song trên đa nhân CPU độc lập (Trang 5 & 6 slide gốc).
4. diag_orig_compare_3_models.png: Bảng so sánh trực quan Tuần tự vs Đồng thời vs Song song.
5. diag_orig_async_parking_exam.png: Minh họa 2 ví dụ đời sống trong slide gốc: Đi thi & Bãi giữ xe (Trang 7 slide gốc).
6. diag_orig_async_single_thread.png: Mô hình bất đồng bộ thực thi đồng thời trên 1 luồng duy nhất, tạm dừng và tiếp tục lại (Trang 8 slide gốc).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = "slide_images"
os.makedirs(IMG_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Tuần tự (Sequential - Trang 2 slide gốc)
# -----------------------------------------------------------------------------
def make_diag_sequential():
    fig, ax = plt.subplots(figsize=(8.5, 2.5), dpi=180)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    tasks = [('Task 1', '#2980B9', 0, 2), ('Task 2', '#27AE60', 2.2, 2), ('Task 3', '#8E44AD', 4.4, 2), ('Task 4', '#D35400', 6.6, 2)]
    for name, col, start, dur in tasks:
        ax.broken_barh([(start, dur)], (0.25, 0.5), facecolors=col, edgecolors='#2C3E50', linewidth=1.2)
        ax.text(start + dur/2, 0.5, f"{name}\n(Thực thi theo thứ tự)", ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)
        if start > 0:
            ax.annotate("", xy=(start, 0.5), xytext=(start - 0.2, 0.5), arrowprops=dict(arrowstyle="->", color='#34495E', lw=1.5))

    ax.set_xlim(-0.2, 8.8)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Trục thời gian thực thi (Time) ➔ T_total = T1 + T2 + T3 + T4", fontsize=8.5, fontweight='bold', color='#2C3E50')
    ax.set_title("XỬ LÝ TUẦN TỰ (SEQUENTIAL COMPUTING): 1 TÁC VỤ TẠI MỘT THỜI ĐIỂM, NỐI TIẾP NHAU", fontsize=9.5, fontweight='bold', color='#C0392B', pad=10)

    plt.tight_layout()
    out = os.path.join(IMG_DIR, "diag_orig_sequential.png")
    plt.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out}")

# -----------------------------------------------------------------------------
# 2. Đồng thời (Concurrency - Trang 3 & 4 slide gốc: PID, xen kẽ trên 1 core)
# -----------------------------------------------------------------------------
def make_diag_concurrency_pid():
    fig, ax = plt.subplots(figsize=(8.5, 2.7), dpi=180)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Box OS / Process PID
    os_box = patches.FancyBboxPatch((0.02, 0.1), 0.28, 0.8, boxstyle="round,pad=0.02", facecolor='#EBF5FB', edgecolor='#2980B9', linewidth=1.5)
    ax.add_patch(os_box)
    ax.text(0.16, 0.78, "HỆ ĐIỀU HÀNH (OS)", ha='center', va='center', fontweight='bold', color='#1B4F72', fontsize=8.5)
    ax.text(0.16, 0.45, "Quản lý chương trình:\n- Cấp Process ID (PID)\n- Phân phối tài nguyên\n- Điều phối nhiều tác vụ", ha='center', va='center', color='#2C3E50', fontsize=7.5)

    # Box 1 CPU Core Interleaving
    core_box = patches.FancyBboxPatch((0.35, 0.1), 0.62, 0.8, boxstyle="round,pad=0.02", facecolor='#FEF9E7', edgecolor='#F39C12', linewidth=1.5)
    ax.add_patch(core_box)
    ax.text(0.66, 0.78, "1 NHÂN CPU DUY NHẤT (SINGLE CPU CORE)", ha='center', va='center', fontweight='bold', color='#7D6608', fontsize=8.5)

    # Slices
    slices = [
        (0.38, 0.10, 'Task 1.1', '#2980B9'), (0.49, 0.10, 'Task 2.1', '#27AE60'),
        (0.60, 0.10, 'Task 1.2', '#2980B9'), (0.71, 0.10, 'Task 3.1', '#8E44AD'),
        (0.82, 0.10, 'Task 2.2', '#27AE60')
    ]
    for x, w, lbl, col in slices:
        b = patches.Rectangle((x, 0.35), w, 0.30, facecolor=col, edgecolor='#2C3E50', linewidth=0.8)
        ax.add_patch(b)
        ax.text(x + w/2, 0.50, lbl, ha='center', va='center', color='white', fontweight='bold', fontsize=6.8)

    ax.text(0.66, 0.22, "★ Chia nhỏ task + Sắp xếp xen kẽ ➔ Tận dụng thời gian rảnh\n★ Tại 1 thời điểm vi mô, CPU core chỉ thi hành đúng 1 task nhỏ!", ha='center', va='center', color='#B7950B', fontsize=7.2, fontweight='bold')

    ax.annotate("", xy=(0.35, 0.5), xytext=(0.30, 0.5), arrowprops=dict(arrowstyle="->", color='#2980B9', lw=2))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("XỬ LÝ ĐỒNG THỜI (CONCURRENCY): ĐIỀU PHỐI XEN KẼ TRÊN 1 NHÂN CPU", fontsize=9.5, fontweight='bold', color='#2C3E50', pad=10)

    plt.tight_layout()
    out = os.path.join(IMG_DIR, "diag_orig_concurrency_pid.png")
    plt.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out}")

# -----------------------------------------------------------------------------
# 3. Song song (Parallel - Trang 5 & 6 slide gốc: Đa nhân CPU vật lý)
# -----------------------------------------------------------------------------
def make_diag_parallel_multicore():
    fig, ax = plt.subplots(figsize=(8.5, 2.7), dpi=180)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    cores = [
        ("Core 1 (Vật lý)", "Task 1 (Độc lập)", '#2980B9', 0.70),
        ("Core 2 (Vật lý)", "Task 2 (Độc lập)", '#27AE60', 0.48),
        ("Core 3 (Vật lý)", "Task 3 (Độc lập)", '#8E44AD', 0.26),
        ("Core 4 (Vật lý)", "Task 4 (Độc lập)", '#D35400', 0.04)
    ]
    for core_lbl, task_lbl, col, y in cores:
        ax.text(0.02, y + 0.09, core_lbl, va='center', fontweight='bold', color='#2C3E50', fontsize=7.5)
        ax.broken_barh([(0.22, 0.70)], (y, 0.18), facecolors=col, edgecolors='#2C3E50', linewidth=1)
        ax.text(0.57, y + 0.09, f"{task_lbl} — Chạy cùng lúc t0", ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)

    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.02, 0.95)
    ax.set_yticks([])
    ax.set_xlabel("Thời điểm thực thi t0 ➔ Thực thi đồng thời vật lý trên các nhân khác nhau", fontsize=8, fontweight='bold', color='#2C3E50')
    ax.set_title("XỬ LÝ SONG SONG (PARALLEL COMPUTING): SỐ NHÂN CPU > 1, CÁC TASK HOÀN TOÀN ĐỘC LẬP", fontsize=9.5, fontweight='bold', color='#27AE60', pad=10)

    plt.tight_layout()
    out = os.path.join(IMG_DIR, "diag_orig_parallel_multicore.png")
    plt.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out}")

# -----------------------------------------------------------------------------
# 4. So sánh 3 mô hình (Tuần tự vs Đồng thời vs Song song)
# -----------------------------------------------------------------------------
def make_diag_compare_3_models():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8.8, 2.7), dpi=180)
    fig.patch.set_facecolor('#FFFFFF')

    # Card 1: Sequential
    ax1.set_facecolor('#EBF5FB')
    ax1.text(0.5, 0.85, "1. TUẦN TỰ\n(Sequential)", ha='center', va='center', fontweight='bold', color='#1B4F72', fontsize=8.5)
    ax1.text(0.5, 0.45, "• 1 task tại 1 thời điểm\n• Nối tiếp theo thứ tự\n• 1 nhân CPU đơn lẻ\n• Thời gian = Tổng task\n• Không chồng lấp", ha='center', va='center', color='#2C3E50', fontsize=7.2)
    ax1.axis('off')

    # Card 2: Concurrency
    ax2.set_facecolor('#FEF9E7')
    ax2.text(0.5, 0.85, "2. ĐỒNG THỜI\n(Concurrency)", ha='center', va='center', fontweight='bold', color='#7D6608', fontsize=8.5)
    ax2.text(0.5, 0.45, "• Nhiều task cùng tiến triển\n• Xen kẽ (Time-slicing)\n• Chạy trên 1 core CPU\n• Tận dụng thời gian rảnh\n• Vi mô: 1 task / thời điểm", ha='center', va='center', color='#2C3E50', fontsize=7.2)
    ax2.axis('off')

    # Card 3: Parallelism
    ax3.set_facecolor('#EAFAF1')
    ax3.text(0.5, 0.85, "3. SONG SONG\n(Parallelism)", ha='center', va='center', fontweight='bold', color='#145A32', fontsize=8.5)
    ax3.text(0.5, 0.45, "• Cùng lúc thực sự t0\n• Độc lập hoàn toàn\n• Số core phần cứng > 1\n• Rút ngắn thời gian vật lý\n• Đa nhân CPU / GPU", ha='center', va='center', color='#2C3E50', fontsize=7.2)
    ax3.axis('off')

    plt.suptitle("ĐỐI CHIẾU 3 MÔ HÌNH THỰC THI NỀN TẢNG CỦA CHƯƠNG 4", fontsize=9.5, fontweight='bold', color='#2C3E50')
    plt.tight_layout()
    out = os.path.join(IMG_DIR, "diag_orig_compare_3_models.png")
    plt.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out}")

# -----------------------------------------------------------------------------
# 5. Ví dụ đời sống trong slide gốc: Đi thi & Bãi giữ xe (Trang 7 slide gốc)
# -----------------------------------------------------------------------------
def make_diag_async_parking_exam():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 2.7), dpi=180)
    fig.patch.set_facecolor('#FFFFFF')

    # Ví dụ 1: Đi thi
    ax1.set_facecolor('#FDEDEC')
    ax1.text(0.5, 0.85, "VÍ DỤ 1: ĐI THI (LÀM BÀI THI)", ha='center', va='center', fontweight='bold', color='#922B21', fontsize=8.5)
    ax1.text(0.5, 0.48, "• Gặp câu hỏi khó / mất thời gian:\n  ➔ Thí sinh tạm bỏ qua, chuyển sang\n      làm câu dễ trước!\n• Khi có ý tưởng hoặc xong câu dễ:\n  ➔ Quay lại giải tiếp câu khó.\n• Ý nghĩa: Xử lý không theo thứ tự,\n  tối ưu hóa tổng thời gian làm bài!", ha='center', va='center', color='#2C3E50', fontsize=7.2)
    ax1.axis('off')

    # Ví dụ 2: Bãi giữ xe
    ax2.set_facecolor('#E8F8F5')
    ax2.text(0.5, 0.85, "VÍ DỤ 2: BÃI GIỮ XE (LẤY VÉ & GỬI XE)", ha='center', va='center', fontweight='bold', color='#117864', fontsize=8.5)
    ax2.text(0.5, 0.48, "• Người gửi xe quét thẻ / nhận vé (nhận handle)\n  ➔ Tự lái xe vào bãi tìm chỗ đỗ.\n• Nhân viên bảo vệ không cần đi theo xe:\n  ➔ Tiếp tục quét thẻ phục vụ người tiếp theo!\n• Ý nghĩa: Giải quyết nhiều yêu cầu đồng thời,\n  không ai bị chặn đứng chờ người khác đỗ xe!", ha='center', va='center', color='#2C3E50', fontsize=7.2)
    ax2.axis('off')

    plt.suptitle("HAI VÍ DỤ TRỰC QUAN ĐỜI SỐNG VỀ BẤT ĐỒNG BỘ TRONG BÀI GIẢNG GỐC C4", fontsize=9.5, fontweight='bold', color='#C0392B')
    plt.tight_layout()
    out = os.path.join(IMG_DIR, "diag_orig_async_parking_exam.png")
    plt.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out}")

# -----------------------------------------------------------------------------
# 6. Mô hình bất đồng bộ thực thi đồng thời trên 1 luồng duy nhất (Trang 8 slide gốc)
# -----------------------------------------------------------------------------
def make_diag_async_single_thread():
    fig, ax = plt.subplots(figsize=(8.5, 2.7), dpi=180)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    # Single thread bar
    ax.text(0.02, 0.75, "LUỒNG ĐIỀU KHIỂN DUY NHẤT (SINGLE THREAD):", fontweight='bold', color='#1B4F72', fontsize=8)

    # Interleaved blocks with yield/resume
    blocks = [
        (0.05, 0.18, 'Task A\n(Đang chạy)', '#2980B9'),
        (0.25, 0.22, 'Task B\n(Chạy khi A tạm dừng)', '#27AE60'),
        (0.49, 0.18, 'Task A\n(Tiếp tục lại)', '#2980B9'),
        (0.69, 0.22, 'Task C\n(Chạy xen kẽ)', '#8E44AD')
    ]
    for x, w, lbl, col in blocks:
        b = patches.Rectangle((x, 0.35), w, 0.30, facecolor=col, edgecolor='#2C3E50', linewidth=1)
        ax.add_patch(b)
        ax.text(x + w/2, 0.50, lbl, ha='center', va='center', color='white', fontweight='bold', fontsize=7)

    # Annotations
    ax.annotate("Tạm dừng A\n(Yield)", xy=(0.24, 0.50), xytext=(0.20, 0.18),
                arrowprops=dict(arrowstyle="->", color='#C0392B', lw=1.2), fontsize=6.8, color='#C0392B', fontweight='bold', ha='center')
    ax.annotate("Đánh thức A\n(Resume)", xy=(0.48, 0.50), xytext=(0.46, 0.18),
                arrowprops=dict(arrowstyle="->", color='#27AE60', lw=1.2), fontsize=6.8, color='#27AE60', fontweight='bold', ha='center')

    ax.set_xlim(0, 0.95)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("MÔ HÌNH BẤT ĐỒNG BỘ THỰC THI ĐỒNG THỜI TRÊN 1 LUỒNG DUY NHẤT (SLIDE 8 GỐC)", fontsize=9.5, fontweight='bold', color='#2C3E50', pad=10)

    plt.tight_layout()
    out = os.path.join(IMG_DIR, "diag_orig_async_single_thread.png")
    plt.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out}")

def main():
    print("Bắt đầu sinh 6 sơ đồ minh họa bám sát 100% nội dung bài giảng gốc C4...")
    make_diag_sequential()
    make_diag_concurrency_pid()
    make_diag_parallel_multicore()
    make_diag_compare_3_models()
    make_diag_async_parking_exam()
    make_diag_async_single_thread()
    print("HOÀN TẤT SINH BỘ 6 SƠ ĐỒ CHUẨN XÁC THEO FILE GỐC!")

if __name__ == "__main__":
    main()
