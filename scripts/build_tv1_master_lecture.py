# -*- coding: utf-8 -*-
"""
build_tv1_master_lecture.py
Tạo bộ Slide BÀI GIẢNG ĐẠI HỌC CHÍNH QUY (24 Slide chuyên sâu 100% thuộc phạm vi TV1)
- Bám sát 100% Trang 1 đến 8 của Bài giảng gốc C4 (BaiGiang_TinhToanSongSong_PhanTan_C4.pdf)
- Loại bỏ hoàn toàn các yếu tố ngoài lề (không Amdahl toán học, không checklist benchmark, không nhãn WHAT/HOW)
- Bố cục 24 slide sư phạm chuẩn đại học, hình ảnh sắc nét, phân tích sâu cơ chế máy tính và hệ điều hành.
- Nhúng đầy đủ Speaker Notes cho từng slide để người thuyết trình/giảng viên giảng bài tự tin.
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import pptx
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

COLOR_RED = RGBColor(231, 76, 60)       # #E74C3C
COLOR_DARK_RED = RGBColor(192, 57, 43)  # #C0392B
COLOR_GRAY = RGBColor(189, 195, 199)    # #BDC3C7
COLOR_DARK = RGBColor(44, 62, 80)       # #2C3E50
COLOR_BODY = RGBColor(33, 47, 61)       # #212F3D
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BG = RGBColor(248, 249, 250) # #F8F9FA
COLOR_GREEN = RGBColor(39, 174, 96)     # #27AE60
COLOR_ORANGE = RGBColor(230, 126, 34)   # #E67E22
COLOR_BLUE = RGBColor(41, 128, 185)     # #2980B9

IMG_DIR = "slide_images"

def create_slide_base(prs, slide_num, header_title, footer_subtitle, session_info="01 - 2026"):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Header đỏ phía trên
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(0), Pt(14.16), Pt(765.36), Pt(99.24))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_RED
    top_bar.line.fill.background()
    
    tf_top = top_bar.text_frame
    tf_top.word_wrap = True
    tf_top.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_top.margin_left = Pt(28.34)
    p_top = tf_top.paragraphs[0]
    p_top.text = header_title.upper()
    p_top.font.name = "Arial"
    p_top.font.size = Pt(25)
    p_top.font.bold = True
    p_top.font.color.rgb = COLOR_WHITE

    # 2. Footer trái (Số trang)
    left_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(14.16), Pt(538.56), Pt(42.48), Pt(42.6))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = COLOR_RED
    left_box.line.fill.background()
    tf_num = left_box.text_frame
    tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_num = tf_num.paragraphs[0]
    p_num.text = str(slide_num)
    p_num.font.name = "Arial"
    p_num.font.size = Pt(16)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_WHITE
    p_num.alignment = PP_ALIGN.CENTER

    # 3. Footer giữa (Phụ đề chuyên đề)
    center_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(70.92), Pt(538.56), Pt(510.24), Pt(42.6))
    center_box.fill.solid()
    center_box.fill.fore_color.rgb = COLOR_GRAY
    center_box.line.fill.background()
    tf_mid = center_box.text_frame
    tf_mid.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_mid.margin_left = Pt(15.0)
    p_mid = tf_mid.paragraphs[0]
    p_mid.text = footer_subtitle
    p_mid.font.name = "Arial"
    p_mid.font.size = Pt(12.5)
    p_mid.font.color.rgb = COLOR_DARK

    # 4. Footer phải (Học kỳ / Niên khóa)
    right_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(595.32), Pt(538.56), Pt(198.36), Pt(42.6))
    right_box.fill.solid()
    right_box.fill.fore_color.rgb = COLOR_RED
    right_box.line.fill.background()
    tf_right = right_box.text_frame
    tf_right.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_right = tf_right.paragraphs[0]
    p_right.text = session_info
    p_right.font.name = "Arial"
    p_right.font.size = Pt(13)
    p_right.font.bold = True
    p_right.font.color.rgb = COLOR_WHITE
    p_right.alignment = PP_ALIGN.CENTER

    return slide

def add_content_title(slide, text):
    tx_box = slide.shapes.add_textbox(Pt(28.34), Pt(120.0), Pt(735.0), Pt(32.0))
    tf = tx_box.text_frame
    tf.margin_top = Pt(0); tf.margin_left = Pt(0)
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = "Arial"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK

def add_bullets(slide, items, left=Pt(28.34), top=Pt(155.0), width=Pt(735.0), height=Pt(170.0), font_size=Pt(12.0)):
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(0); tf.margin_top = Pt(0)
    for idx, (head, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(7)
        run_h = p.add_run()
        run_h.text = f"• {head}: "
        run_h.font.name = "Arial"
        run_h.font.size = font_size
        run_h.font.bold = True
        run_h.font.color.rgb = COLOR_RED
        
        run_b = p.add_run()
        run_b.text = body
        run_b.font.name = "Arial"
        run_b.font.size = font_size
        run_b.font.color.rgb = COLOR_BODY
    return tx_box

def add_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

def add_card(slide, title, items, left, top, width, height, border_color=COLOR_RED):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_CARD_BG
    box.line.color.rgb = border_color
    box.line.width = Pt(1.5)
    tf = box.text_frame
    tf.margin_left = Pt(16); tf.margin_top = Pt(12); tf.margin_right = Pt(16)
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = "Arial"; p0.font.size = Pt(12.5); p0.font.bold = True; p0.font.color.rgb = border_color
    for k, v in items:
        p = tf.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run(); r1.text = f"• {k}: "; r1.font.bold = True; r1.font.size = Pt(10.5); r1.font.color.rgb = COLOR_DARK
        r2 = p.add_run(); r2.text = v; r2.font.size = Pt(10.5); r2.font.color.rgb = COLOR_BODY
    return box

def add_table_box(slide, headers, rows, left, top, width, height, col_widths=None):
    rows_cnt = len(rows) + 1
    cols_cnt = len(headers)
    table_shape = slide.shapes.add_table(rows_cnt, cols_cnt, left, top, width, height)
    table = table_shape.table
    
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_RED
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        
    for r_idx, row_data in enumerate(rows):
        bg_c = COLOR_WHITE if r_idx % 2 == 0 else COLOR_CARD_BG
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_c
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_BODY
            
    if col_widths:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = Pt(w)
    return table_shape

def build_tv1_master_presentation(prs):
    # =========================================================================
    # SLIDE 1: BÌA BÀI GIẢNG CHƯƠNG 4 (Khớp Slide 1 gốc)
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    tx_top = s1.shapes.add_textbox(Pt(28.34), Pt(45.0), Pt(735.0), Pt(65.0))
    tf_top = tx_top.text_frame
    p_t1 = tf_top.paragraphs[0]
    p_t1.text = "TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ (CTUET)"
    p_t1.font.name = "Arial"; p_t1.font.size = Pt(14); p_t1.font.bold = True; p_t1.font.color.rgb = COLOR_DARK
    p_t2 = tf_top.add_paragraph()
    p_t2.text = "KHOA CÔNG NGHỆ THÔNG TIN — HỌC PHẦN: TÍNH TOÁN SONG SONG VÀ PHÂN TÁN"
    p_t2.font.name = "Arial"; p_t2.font.size = Pt(11.5); p_t2.font.color.rgb = COLOR_GRAY

    mid_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(0), Pt(235.0), Pt(765.36), Pt(125.0))
    mid_bar.fill.solid(); mid_bar.fill.fore_color.rgb = COLOR_RED; mid_bar.line.fill.background()
    tf_mid = mid_bar.text_frame; tf_mid.vertical_anchor = MSO_ANCHOR.MIDDLE; tf_mid.margin_left = Pt(28.34)
    p_m1 = tf_mid.paragraphs[0]
    p_m1.text = "CHƯƠNG  4:"
    p_m1.font.name = "Arial"; p_m1.font.size = Pt(26); p_m1.font.bold = True; p_m1.font.color.rgb = COLOR_WHITE
    p_m2 = tf_mid.add_paragraph()
    p_m2.text = "TÍNH TOÁN BẤT ĐỒNG BỘ TRONG PYTHON"
    p_m2.font.name = "Arial"; p_m2.font.size = Pt(30); p_m2.font.bold = True; p_m2.font.color.rgb = COLOR_WHITE

    tx_bot = s1.shapes.add_textbox(Pt(28.34), Pt(385.0), Pt(735.0), Pt(140.0))
    tf_bot = tx_bot.text_frame
    p_b1 = tf_bot.paragraphs[0]
    p_b1.text = "PHẦN I: GIỚI THIỆU — NỀN TẢNG CÁC MÔ HÌNH THỰC THI (SLIDE GỐC 1 – 8)"
    p_b1.font.name = "Arial"; p_b1.font.size = Pt(14); p_b1.font.bold = True; p_b1.font.color.rgb = COLOR_DARK
    p_b2 = tf_bot.add_paragraph()
    p_b2.text = "Báo cáo chuyên môn & Giảng dạy: Thành viên 1 (TV1)"
    p_b2.font.name = "Arial"; p_b2.font.size = Pt(12.5); p_b2.font.bold = True; p_b2.font.color.rgb = COLOR_ORANGE
    p_b3 = tf_bot.add_paragraph()
    p_b3.text = "Giảng viên hướng dẫn: ThS. Lê Anh Nhã Uyên (lanuyen@ctuet.edu.vn)"
    p_b3.font.name = "Arial"; p_b3.font.size = Pt(11); p_b3.font.color.rgb = COLOR_BODY

    add_speaker_notes(s1, "Kính chào cô và cả lớp. Hôm nay em đại diện Thành viên 1 trình bày Phần I: Giới thiệu trong Chương 4 - Tính toán bất đồng bộ trong Python. Đây là nền tảng cốt lõi định hình tư duy về các mô hình xử lý tính toán trong hệ thống hiện đại.")

    # =========================================================================
    # SLIDE 2: MỤC TIÊU HỌC TẬP & ĐỊNH HƯỚNG BÀI GIẢNG PHẦN I
    # =========================================================================
    s2 = create_slide_base(prs, 2, "GIỚI THIỆU", "Mục tiêu Học tập & Phạm vi Nghiên cứu TV1")
    add_content_title(s2, "Mục tiêu bài học và kiến thức cốt lõi cần làm chủ")
    add_bullets(s2, [
        ("Nắm vững bản chất 4 mô hình thực thi", "Hiểu tường tận sự khác biệt bản chất giữa Tuần tự (Sequential), Đồng thời (Concurrency), Song song (Parallelism) và Bất đồng bộ (Asynchronous)."),
        ("Hiểu rõ cơ chế điều phối của Hệ điều hành", "Cách hệ điều hành quản lý chương trình thông qua Process ID (PID) và cách CPU Core phân chia thời gian cho các tác vụ."),
        ("Phân biệt điều kiện phần cứng", "Nắm rõ khi nào bài toán đòi hỏi đa nhân vật lý (Multi-core) và khi nào có thể tối ưu hóa ngay trên một nhân đơn (Single-core)."),
        ("Làm chủ mô hình Luồng đơn Bất đồng bộ", "Hiểu cơ chế tạm dừng (pause/suspend) và tiếp tục lại (resume) trong một luồng điều khiển duy nhất qua 2 ví dụ thực tế: Đi thi và Bãi giữ xe.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s2, "KIM CHỈ NAM CỦA THÀNH VIÊN 1:", [
        ("Bám sát bài giảng gốc", "Trọng tâm trọn vẹn từ Slide 1 đến Slide 8 của tài liệu Chương 4 chính thức."),
        ("Phương pháp tiếp cận", "Đi từ trực quan sinh động đến bản chất kiến trúc máy tính và cơ chế điều phối hệ điều hành."),
        ("Chuẩn bị chuyển giao", "Tạo nền tảng tư duy vững chắc trước khi bước vào các thư viện cụ thể như concurrent.futures và asyncio.")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_RED)
    add_speaker_notes(s2, "Mục tiêu của phần này là giải quyết triệt để sự nhầm lẫn giữa các thuật ngữ. Sinh viên thường nhầm đồng thời với song song, hoặc nghĩ bất đồng bộ là phải có nhiều luồng. Chúng ta sẽ làm sáng tỏ điều này.")

    # =========================================================================
    # SLIDE 3: BẢN ĐỒ TƯ DUY 4 MÔ HÌNH TÍNH TOÁN NỀN TẢNG
    # =========================================================================
    s3 = create_slide_base(prs, 3, "GIỚI THIỆU", "Bản đồ Tư duy 4 Mô hình Tính toán")
    add_content_title(s3, "Bản đồ tư duy: Bốn mô hình tính toán nền tảng của Chương 4")
    add_bullets(s3, [
        ("Mô hình 1 — Tuần tự (Sequential)", "Xử lý 1 tác vụ trong 1 khoảng thời gian; các task nối tiếp nhau theo thứ tự cố định nghiêm ngặt."),
        ("Mô hình 2 — Đồng thời (Concurrency)", "Phân chia và điều phối nhiều tác vụ cùng tiến triển xen kẽ nhau trong cùng khoảng thời gian trên 1 nhân CPU."),
        ("Mô hình 3 — Song song (Parallelism)", "Nhiều tác vụ độc lập được thực thi đồng thời vật lý tại cùng thời điểm trên nhiều nhân CPU độc lập."),
        ("Mô hình 4 — Bất đồng bộ (Asynchronous)", "Xử lý không theo thứ tự, giải quyết nhiều yêu cầu đồng thời trong khoảng thời gian ngắn hơn rất nhiều.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    s3.shapes.add_picture(os.path.join(IMG_DIR, "diag_orig_compare_3_models.png"), Pt(28.34), Pt(325.0), Pt(735.0), Pt(195.0))
    add_speaker_notes(s3, "Slide 3 trực quan hóa 4 mô hình. Sơ đồ bên dưới cho thấy sự khác nhau rất rõ ràng về trục thời gian giữa chạy tuần tự, chạy xen kẽ trên 1 CPU, và chạy song song đồng thời trên nhiều CPU.")

    # =========================================================================
    # SLIDE 4: MÔ HÌNH 1 — XỬ LÝ TUẦN TỰ (SEQUENTIAL) — Slide 2 gốc
    # =========================================================================
    s4 = create_slide_base(prs, 4, "GIỚI THIỆU", "Sequential - Tuần tự (Slide 2 gốc)")
    add_content_title(s4, "Mô hình xử lý tuần tự (Sequential Computing)")
    add_bullets(s4, [
        ("Định nghĩa xử lý tuần tự", "Xử lý 1 tác vụ (task) trong một khoảng thời gian xác định."),
        ("Quy tắc thứ tự thực thi", "Các task sẽ được thực thi tuần tự theo thứ tự: Tác vụ trước phải kết thúc hoàn toàn thì tác vụ sau mới được phép bắt đầu."),
        ("Đường đi của luồng điều khiển", "Chương trình chỉ duy trì một dòng thực thi duy nhất (Single Execution Path) từ điểm bắt đầu đến điểm kết thúc."),
        ("Đặc điểm dự đoán", "Hệ thống có tính tất định cao nhất (Deterministic), dễ gỡ lỗi nhất, không có hiện tượng tranh chấp tài nguyên.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    s4.shapes.add_picture(os.path.join(IMG_DIR, "diag_orig_sequential.png"), Pt(28.34), Pt(330.0), Pt(735.0), Pt(190.0))
    add_speaker_notes(s4, "Đây là nội dung Slide 2 bài giảng gốc: Xử lý tuần tự là mô hình cơ bản và trực quan nhất. 1 task làm xong mới tới task tiếp theo. Mọi dòng mã chạy từ trên xuống dưới.")

    # =========================================================================
    # SLIDE 5: TIMELINE TUẦN TỰ & NGHẼN TÀI NGUYÊN (I/O WAIT)
    # =========================================================================
    s5 = create_slide_base(prs, 5, "GIỚI THIỆU", "Phân tích Hạn chế của Xử lý Tuần tự")
    add_content_title(s5, "Hạn chế cốt tử của xử lý tuần tự: Lãng phí tài nguyên CPU")
    add_bullets(s5, [
        ("Nút thắt chặn dòng (Blocking)", "Nếu một tác vụ gặp thao tác cần thời gian chờ (ví dụ: đọc ghi đĩa, truy vấn cơ sở dữ liệu, chờ phản hồi qua mạng Internet), nó sẽ giữ chặt luồng xử lý."),
        ("Trạng thái CPU nhàn rỗi (CPU Idle)", "Trong thời gian tác vụ chờ dữ liệu bên ngoài, bộ vi xử lý (CPU) hoàn toàn rơi vào trạng thái nhàn rỗi lãng phí."),
        ("Thời gian thực thi tích lũy", "Tổng thời gian của chương trình bằng tổng thời gian của từng tác vụ cộng lại: T_total = T_1 + T_2 + ... + T_n."),
        ("Nhu cầu cấp bách", "Cần một giải pháp cho phép hệ thống tận dụng khoảng thời gian chết này để làm việc khác mà không phải chờ đợi vô ích.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s5, "BÀI TOÁN THỰC TẾ: TẢI 100 TỆP DỮ LIỆU TỪ MẠNG", [
        ("Chạy tuần tự", "Mỗi tệp mất 1 giây chờ mạng ➔ Tổng thời gian: 100 giây! Suốt 100 giây đó, CPU chạy chưa tới 1% công suất."),
        ("Vấn đề", "CPU phải chờ thiết bị ngoại vi I/O hoàn thành mới chuyển sang lệnh kế tiếp."),
        ("Giải pháp đặt ra", "Chuyển giao việc chờ đợi cho hệ thống ngoại vi và chuyển CPU sang xử lý tác vụ khác!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_ORANGE)
    add_speaker_notes(s5, "Slide 5 giải thích vì sao tuần tự lại không hiệu quả. Điểm nghẽn không nằm ở tốc độ tính toán của CPU, mà nằm ở việc CPU phải chờ các thao tác I/O. Đây chính là lý do chúng ta cần đến Concurrency.")

    # =========================================================================
    # SLIDE 6: MÔ HÌNH 2 — XỬ LÝ ĐỒNG THỜI (CONCURRENCY) & VAI TRÒ HĐH (Slide 3 gốc)
    # =========================================================================
    s6 = create_slide_base(prs, 6, "GIỚI THIỆU", "Concurrency - Đồng thời (Slide 3 gốc)")
    add_content_title(s6, "Xử lý đồng thời: Vai trò của Hệ điều hành và Tiến trình")
    add_bullets(s6, [
        ("Chương trình và Tiến trình (Process)", "Hệ điều hành quản lý các chương trình đang chạy trong máy tính thông qua các Tiến trình (Process)."),
        ("Mã định danh Process ID (PID)", "Hệ điều hành cấp phát một mã số Process ID (PID) duy nhất để nhận diện, giám sát và phân bổ tài nguyên cho từng chương trình."),
        ("Cơ chế phân chia của CPU Core", "Nhân CPU (CPU Core) chia các task của process thành các task nhỏ hơn + sắp xếp xen kẽ nhau linh hoạt."),
        ("Mục tiêu tối ưu hóa tài nguyên", "Tận dụng tối đa thời gian rảnh của task này để chuyển sang thực hiện task khác, không để CPU rơi vào trạng thái lãng phí.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    s6.shapes.add_picture(os.path.join(IMG_DIR, "diag_orig_concurrency_pid.png"), Pt(28.34), Pt(325.0), Pt(735.0), Pt(195.0))
    add_speaker_notes(s6, "Nội dung Slide 3 bài giảng gốc: Hệ điều hành đóng vai trò nhạc trưởng. Nó quản lý tiến trình bằng PID. CPU Core thông minh ở chỗ nó băm nhỏ task và sắp xếp xen kẽ nhau.")

    # =========================================================================
    # SLIDE 7: XỬ LÝ ĐỒNG THỜI — CƠ CHẾ PHÂN CHIA XEN KẼ TRÊN 1 CPU CORE
    # =========================================================================
    s7 = create_slide_base(prs, 7, "GIỚI THIỆU", "Cơ chế Điều phối Xen kẽ trên 1 Nhân CPU")
    add_content_title(s7, "Cơ chế phân chia và lập lịch xen kẽ (Time-slicing)")
    add_bullets(s7, [
        ("Phân đoạn thời gian (Quantum / Time Slice)", "Hệ điều hành chia thời gian xử lý của CPU Core thành các lát cắt siêu nhỏ (khoảng vài mili-giây đến micro-giây)."),
        ("Chuyển đổi ngữ cảnh (Context Switching)", "CPU tạm dừng task A, lưu trạng thái thanh ghi và bộ nhớ của A, sau đó nạp trạng thái của task B vào để thực thi tiếp tục."),
        ("Tạo cảm giác chạy cùng lúc", "Tốc độ chuyển đổi giữa các task cực nhanh (hàng nghìn lần mỗi giây) tạo cho người dùng cảm giác các tác vụ đang chạy đồng thời mượt mà."),
        ("Tiến triển đồng thời (Concurrent Progress)", "Tất cả các task đều đạt được sự tiến triển (progress) trong cùng một khoảng thời gian quan sát.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s7, "QUY TRÌNH TIME-SLICING VÍ DỤ:", [
        ("0ms - 10ms", "CPU thực thi một đoạn của Tiến trình 1 (PID 1024 - Trình duyệt Web)."),
        ("10ms - 20ms", "CPU chuyển đổi ngữ cảnh, thực thi một đoạn của Tiến trình 2 (PID 1088 - Phát nhạc Spotify)."),
        ("20ms - 30ms", "CPU chuyển đổi ngữ cảnh, tiếp tục thực thi Tiến trình 1 ➔ Người dùng vừa nghe nhạc vừa lướt web trơn tru!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_BLUE)
    add_speaker_notes(s7, "Slide 7 đào sâu vào cơ chế Time-slicing. Nhờ tốc độ chuyển đổi ngữ cảnh siêu nhanh, người dùng thấy nhạc vẫn phát, web vẫn tải, chuột vẫn di chuyển mượt mà dù máy chỉ có đúng 1 nhân CPU.")

    # =========================================================================
    # SLIDE 8: XỬ LÝ ĐỒNG THỜI — BẢN CHẤT VI MÔ VS VĨ MÔ (Slide 4 gốc)
    # =========================================================================
    s8 = create_slide_base(prs, 8, "GIỚI THIỆU", "Concurrency - Bản chất Thực thi (Slide 4 gốc)")
    add_content_title(s8, "Xử lý đồng thời: Bản chất vi mô so với góc nhìn vĩ mô")
    add_bullets(s8, [
        ("Điều phối trong cùng khoảng thời gian", "Hệ thống phân chia, điều phối nhiều tác vụ (task) khác nhau trong cùng một khoảng thời gian xác định."),
        ("Quy tắc vật lý vi mô bên dưới", "Bên dưới CPU core chỉ có thể thực thi MỘT TASK NHỎ trong task lớn tại một thời điểm vi mô duy nhất!"),
        ("Góc nhìn người dùng (Vĩ mô)", "Máy tính xử lý nhiều việc cùng lúc tại cùng thời điểm dưới góc nhìn của người dùng."),
        ("Kết luận cốt lõi của Concurrency", "Concurrency là sự TIẾN TRIỂN XEN KẼ (Interleaving), giải quyết bài toán quản lý và điều phối nhiều việc trên tài nguyên hạn chế.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s8, "TỔNG KẾT SLIDE 4 BÀI GIẢNG GỐC:", [
        ("Khái niệm", "Xử lý đồng thời là điều phối nhiều task trong cùng 1 khoảng thời gian."),
        ("Góc nhìn vĩ mô", "Người dùng thấy nhiều chương trình cùng chạy song hành trơn tru."),
        ("Góc nhìn vi mô", "Tại MỘT thời điểm cực nhỏ trên 1 nhân CPU, CHỈ CÓ ĐÚNG 1 task được thi hành!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_ORANGE)
    add_speaker_notes(s8, "Slide 8 nhấn mạnh slide 4 gốc: Concurrency là cấu trúc xử lý nhiều việc cùng lúc (dealing with lots of things at once). Dưới góc nhìn người dùng là cùng lúc, nhưng ở mức vi mô 1 nhân CPU thì lệnh vẫn chạy lần lượt.")

    # =========================================================================
    # SLIDE 9: MÔ HÌNH 3 — XỬ LÝ SONG SONG (PARALLEL) — ĐA NHÂN VẬT LÝ (Slide 5 gốc)
    # =========================================================================
    s9 = create_slide_base(prs, 9, "GIỚI THIỆU", "Parallel - Song song (Slide 5 gốc)")
    add_content_title(s9, "Mô hình xử lý song song (Parallel Computing)")
    add_bullets(s9, [
        ("Định nghĩa xử lý song song", "Nhiều task khác nhau được xử lý trong CÙNG 1 THỜI ĐIỂM (thực thi đồng thời vật lý thực sự)."),
        ("Yêu cầu tính độc lập dữ liệu", "Các task phải hoàn toàn độc lập với nhau để có thể chạy song song mà không xung đột hay tranh chấp bộ nhớ."),
        ("Điều kiện phần cứng bắt buộc", "Chỉ có thể thực hiện trên máy tính có số nhân (core) vật lý lớn hơn 1 (Multi-core CPU, hệ thống Multi-CPU hoặc GPU)."),
        ("Rút ngắn thời gian thực tế", "Thời gian hoàn thành toàn bộ khối lượng công việc được rút ngắn nhờ tận dụng đồng thời nhiều bộ vi xử lý vật lý.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    s9.shapes.add_picture(os.path.join(IMG_DIR, "diag_orig_parallel_multicore.png"), Pt(28.34), Pt(325.0), Pt(735.0), Pt(195.0))
    add_speaker_notes(s9, "Slide 9 phản ánh slide 5 gốc: Khác hẳn với Concurrency, Parallelism bắt buộc phải có phần cứng hỗ trợ (số core > 1). Tại cùng 1 khoảnh khắc đồng hồ vật lý, có nhiều lệnh được thực thi cùng lúc trên các core khác nhau.")

    # =========================================================================
    # SLIDE 10: XỬ LÝ SONG SONG — ĐIỀU KIỆN PHẦN CỨNG & ĐỘC LẬP TÁC VỤ
    # =========================================================================
    s10 = create_slide_base(prs, 10, "GIỚI THIỆU", "Điều kiện Phần cứng & Tính Độc lập Dữ liệu")
    add_content_title(s10, "Điều kiện tiên quyết để đạt được xử lý song song thực sự")
    add_bullets(s10, [
        ("Kiến trúc vi xử lý đa nhân (Multi-core)", "Mỗi nhân CPU là một đơn vị xử lý độc lập hoàn chỉnh, sở hữu tập thanh ghi và bộ giải mã lệnh riêng biệt."),
        ("Tính độc lập dữ liệu (Data Independence)", "Nếu Task B cần kết quả của Task A để tính toán, Task B không thể chạy song song với Task A mà buộc phải chờ!"),
        ("Khả năng phân rã bài toán (Decomposition)", "Bài toán phải có khả năng chia thành các phần việc độc lập (như xử lý từng pixel của ảnh, nhân ma trận theo khối)."),
        ("Phân biệt với Concurrency", "Concurrency có thể chạy trên 1 nhân CPU đơn lẻ; nhưng Parallelism tuyệt đối không thể tồn tại nếu chỉ có 1 nhân CPU duy nhất.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s10, "HAI ĐIỀU KIỆN BẮT BUỘC ĐỂ SONG SONG HÓA:", [
        ("1. Điều kiện Phần cứng", "Hệ thống phải có từ 2 nhân CPU vật lý trở lên (hoặc nhiều vi xử lý / GPU)."),
        ("2. Điều kiện Thuật toán", "Các tác vụ không phụ thuộc dữ liệu lẫn nhau (Data-independent tasks)."),
        ("Nếu thiếu 1 trong 2", "Hệ thống sẽ tự động quay trở về mô hình Đồng thời (Concurrency) xen kẽ thông thường.")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_GREEN)
    add_speaker_notes(s10, "Slide 10 làm rõ điều kiện để có song song thực sự. Nếu bài toán có sự phụ thuộc dữ liệu chặt chẽ thì dù máy có 64 nhân cũng không thể chạy song song được hoàn toàn.")

    # =========================================================================
    # SLIDE 11: MỐI QUAN HỆ SONG SONG & ĐỒNG THỜI TRÊN ĐA NHÂN (Slide 6 gốc)
    # =========================================================================
    s11 = create_slide_base(prs, 11, "GIỚI THIỆU", "Parallel - Song song (Slide 6 gốc)")
    add_content_title(s11, "Mối quan hệ thực tế giữa Song song và Đồng thời trên Đa nhân")
    add_bullets(s11, [
        ("Thực tế kiến trúc máy tính hiện đại", "Trên thực tế, trên mỗi nhân của CPU vẫn xảy ra quá trình xử lý ĐỒNG THỜI (xen kẽ các task nền của hệ điều hành)."),
        ("Quy tắc không trùng lặp tác vụ", "Tại một thời điểm, KHÔNG xảy ra việc xử lý cùng một task trên hai nhân CPU khác nhau."),
        ("Sự phối hợp giữa hai cấp độ", "Hệ thống đa nhân vừa có tính song song (giữa các nhân với nhau) vừa có tính đồng thời (bên trong từng nhân riêng lẻ)."),
        ("Hiệu quả tối ưu toàn diện", "Khai thác tối đa công suất phần cứng: vừa tận dụng sức mạnh đa nhân vật lý, vừa không lãng phí thời gian nhàn rỗi của từng nhân.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s11, "QUY TẮC BẢN QUYỀN SLIDE 6 BÀI GIẢNG GỐC:", [
        ("Nội bộ từng nhân", "Vẫn diễn ra Concurrency (xen kẽ các thread / process do OS điều phối)."),
        ("Giữa các nhân", "Diễn ra Parallelism thực sự (chạy song song các tiến trình độc lập)."),
        ("Điều kiện chốt", "Tại cùng một thời điểm vi mô, tuyệt đối không có chuyện 2 nhân CPU cùng chạy chung 1 task!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_GREEN)
    add_speaker_notes(s11, "Slide 11 bám sát slide 6 gốc: Giảng viên đưa ra lưu ý rất tinh tế về kiến trúc thực tế. Trên mỗi nhân vẫn có concurrency để chạy các task nền, và không bao giờ có chuyện 2 core cùng chạy 1 task tại 1 thời điểm.")

    # =========================================================================
    # SLIDE 12: BẢNG SO SÁNH TRỰC QUAN 3 MÔ HÌNH: TUẦN TỰ VS ĐỒNG THỜI VS SONG SONG
    # =========================================================================
    s12 = create_slide_base(prs, 12, "SO SÁNH", "So sánh Ba Mô hình Tính toán Cơ bản")
    add_content_title(s12, "Bảng đối chiếu toàn diện: Tuần tự vs Đồng thời vs Song song")
    
    t_h = ["Tiêu chí so sánh", "Tuần tự (Sequential)", "Đồng thời (Concurrency)", "Song song (Parallelism)"]
    t_r = [
        ["Số tác vụ cùng lúc", "1 tác vụ tại 1 thời điểm", "Nhiều tác vụ cùng tiến triển", "Nhiều tác vụ chạy đồng thời vật lý"],
        ["Số nhân CPU tối thiểu", "1 nhân CPU là đủ", "1 nhân CPU là đủ", "Bắt buộc phải > 1 nhân CPU"],
        ["Cơ chế thực thi", "Nối tiếp từ đầu đến cuối", "Phân chia thời gian xen kẽ", "Chạy thực sự tại cùng 1 khoảnh khắc"],
        ["Xử lý khi bị nghẽn", "Toàn bộ hệ thống bị chặn", "Chuyển sang làm task khác", "Các core khác vẫn chạy bình thường"],
        ["Mục tiêu cốt lõi", "Đơn giản, đúng thứ tự", "Cấu trúc hóa nhiều việc", "Tăng tốc độ tính toán phần cứng"]
    ]
    add_table_box(s12, t_h, t_r, Pt(28.34), Pt(165.0), Pt(735.0), Pt(350.0), col_widths=[145, 185, 205, 200])
    add_speaker_notes(s12, "Bảng so sánh này giúp sinh viên tổng hợp nhanh sự khác biệt giữa 3 mô hình. Hãy nhấn mạnh cột Số nhân CPU: Concurrency chỉ cần 1 nhân, nhưng Parallelism bắt buộc phải có từ 2 nhân trở lên.")

    # =========================================================================
    # SLIDE 13: MÔ HÌNH 4 — XỬ LÝ BẤT ĐỒNG BỘ (ASYNCHRONOUS) (Slide 7 gốc)
    # =========================================================================
    s13 = create_slide_base(prs, 13, "GIỚI THIỆU", "Asynchronous - Bất đồng bộ (Slide 7 gốc)")
    add_content_title(s13, "Mô hình xử lý bất đồng bộ (Asynchronous Computing)")
    add_bullets(s13, [
        ("Xử lý không theo thứ tự cố định", "Cho phép các task được xử lý KHÔNG THEO THỨ TỰ (có thể chuyển sang làm task khác trước khi task trước đó hoàn thành)."),
        ("Tiếp nhận nhiều yêu cầu cùng lúc", "Hệ thống có thể liên tục tiếp nhận các yêu cầu mới mà không bị chặn lại bởi các yêu cầu cũ đang chờ xử lý."),
        ("Rút ngắn thời gian toàn cục", "Giải quyết nhiều yêu cầu đồng thời trong khoảng thời gian ngắn hơn rất nhiều so với mô hình tuần tự truyền thống."),
        ("Ví dụ đời sống trong slide gốc", "Đi thi (làm bài thi), Bãi giữ xe (quét thẻ gửi xe), ...")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    s13.shapes.add_picture(os.path.join(IMG_DIR, "diag_orig_async_parking_exam.png"), Pt(28.34), Pt(325.0), Pt(735.0), Pt(195.0))
    add_speaker_notes(s13, "Slide 13 dẫn nhập slide 7 gốc: Bất đồng bộ (Asynchronous). Khái niệm then chốt là: Xử lý không theo thứ tự, có thể chuyển sang task khác trước khi task trước hoàn thành. Giảng viên đưa 2 ví dụ: Đi thi và Bãi giữ xe.")

    # =========================================================================
    # SLIDE 14: VÌ SAO BẤT ĐỒNG BỘ RÚT NGẮN ĐƯỢC THỜI GIAN THỰC THI?
    # =========================================================================
    s14 = create_slide_base(prs, 14, "GIỚI THIỆU", "Cơ chế Tối ưu Thời gian của Bất đồng bộ")
    add_content_title(s14, "Cơ chế tối ưu hóa thời gian: Chồng lấp thời gian chờ I/O")
    add_bullets(s14, [
        ("Khoảng chờ I/O là cơ hội", "Trong các ứng dụng thực tế (web, mạng, cơ sở dữ liệu), hơn 90% thời gian là chờ phản hồi từ thiết bị hoặc server khác."),
        ("Cơ chế Không chờ đợi (Non-blocking)", "Khi gửi yêu cầu I/O, tác vụ không đứng chờ kết quả mà đăng ký một điểm hẹn (callback / event / future) rồi nhường quyền thực thi."),
        ("Chồng lấp thời gian chờ (I/O Overlapping)", "Thời gian chờ của 10 yêu cầu diễn ra song song cùng lúc trong mạng; CPU chỉ tốn chút thời gian phát lệnh và thu hoạch kết quả."),
        ("Kết quả tăng tốc vượt bậc", "Thời gian hoàn thành 10 tác vụ I/O xấp xỉ bằng thời gian của 1 tác vụ lâu nhất, thay vì tổng thời gian của cả 10 tác vụ cộng lại!")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s14, "SO SÁNH THỜI GIAN THỰC HIỆN 5 LỆNH TRUY VẤN MẠNG (MỖI LỆNH MẤT 1 GIÂY):", [
        ("Mô hình Đồng bộ (Sync)", "Lệnh 1 (1s) ➔ Lệnh 2 (1s) ➔ Lệnh 3 (1s) ➔ Lệnh 4 (1s) ➔ Lệnh 5 (1s). Tổng cộng: 5 GIÂY!"),
        ("Mô hình Bất đồng bộ (Async)", "Phát 5 lệnh cùng lúc (tốn 0.01s CPU) ➔ Cả 5 lệnh cùng chờ mạng ➔ Tổng cộng: KHOẢNG 1.05 GIÂY!"),
        ("Hiệu quả", "Tăng tốc gấp gần 5 lần mà không cần tạo thêm bất kỳ luồng hay tiến trình nào!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_RED)
    add_speaker_notes(s14, "Slide 14 làm rõ tại sao bất đồng bộ lại nhanh hơn. Nó không làm CPU tính toán nhanh hơn, mà nó tận dụng việc chồng lấp thời gian chờ I/O của nhiều tác vụ với nhau.")

    # =========================================================================
    # SLIDE 15: PHÂN TÍCH VÍ DỤ ĐỜI SỐNG 1 — ĐI THI (LÀM BÀI THI)
    # =========================================================================
    s15 = create_slide_base(prs, 15, "VÍ DỤ THỰC TẾ", "Ví dụ 1: Đi thi (Làm bài thi)")
    add_content_title(s15, "Phân tích ví dụ Đi thi: Xử lý không theo thứ tự trong bài thi")
    add_bullets(s15, [
        ("Bối cảnh trong phòng thi", "Đề thi gồm 10 câu hỏi, được đánh số từ Câu 1 đến Câu 10. Mỗi câu có độ khó và thời gian giải khác nhau."),
        ("Cách làm theo kiểu Tuần tự", "Thí sinh cắm đầu làm Câu 1. Đến Câu 2 gặp bài toán hóc búa, thí sinh ngồi suy nghĩ 45 phút không nhúc nhích ➔ Hết giờ thi chỉ làm được 2 câu!"),
        ("Cách làm theo kiểu Bất đồng bộ", "Thí sinh đọc Câu 2 thấy khó ➔ TẠM DỪNG, đánh dấu lại và CHUYỂN NGAY sang làm Câu 3, Câu 4 dễ hơn. Khi làm xong các câu dễ và não bộ đã có thêm ý tưởng ➔ QUAY LẠI giải Câu 2!"),
        ("Bài học công nghệ", "Chương trình máy tính cũng vậy: Khi gặp một tác vụ mất thời gian chờ dữ liệu, nó tạm bỏ qua để phục vụ các yêu cầu khác trước.")
    ], top=Pt(150.0), height=Pt(170.0), font_size=Pt(12.0))
    add_card(s15, "Ý NGHĨA KỸ THUẬT CỦA VÍ DỤ 'ĐI THI':", [
        ("Tài nguyên xử lý", "Một thí sinh duy nhất (tương ứng với MỘT LUỒNG ĐIỀU KHIỂN DUY NHẤT)."),
        ("Tác vụ khó/chờ lâu", "Tương ứng với thao tác Blocking I/O (chờ mạng, chờ đĩa)."),
        ("Hành động tạm dừng & quay lại", "Tương ứng với lệnh 'await' và cơ chế Cooperative Scheduling trong Python Asyncio!")
    ], Pt(28.34), Pt(345.0), Pt(735.0), Pt(170.0), border_color=COLOR_ORANGE)
    add_speaker_notes(s15, "Ví dụ Đi thi là ví dụ cực kỳ gần gũi trong slide 7 gốc. Người đi thi thông minh không bao giờ ngồi chờ chết thời gian ở câu khó, mà tạm gác lại làm câu dễ trước. Đó chính là bất đồng bộ!")

    # =========================================================================
    # SLIDE 16: PHÂN TÍCH VÍ DỤ ĐỜI SỐNG 2 — BÃI GIỮ XE (GỬI & LẤY THẺ XE)
    # =========================================================================
    s16 = create_slide_base(prs, 16, "VÍ DỤ THỰC TẾ", "Ví dụ 2: Bãi giữ xe (Gửi & Lấy thẻ xe)")
    add_content_title(s16, "Phân tích ví dụ Bãi giữ xe: Tiếp nhận nhiều yêu cầu không bị chặn")
    add_bullets(s16, [
        ("Bối cảnh tại cổng bãi xe", "Khách hàng liên tục đi xe máy đến gửi xe tại cổng trường hoặc trung tâm thương mại vào giờ cao điểm."),
        ("Cách phục vụ Tuần tự (Blocking)", "Bác bảo vệ phát thẻ xe, sau đó DẪN XE CỦA KHÁCH VÀO TẬN VỊ TRÍ ĐỖ, khóa xe xong mới quay ra cổng đón người tiếp theo ➔ Hàng dài xe bị ùn tắc hàng cây số!"),
        ("Cách phục vụ Bất đồng bộ (Non-blocking)", "Bác bảo vệ quẹt thẻ xe, trao vé cho khách (nhận vé hẹn / handle). Khách TỰ DẮT XE VÀO BÃI. Bác bảo vệ KHÔNG CHỜ mà lập tức quẹt thẻ phục vụ người tiếp theo!"),
        ("Bài học công nghệ", "Bảo vệ (CPU/Server) chỉ làm nhiệm vụ tiếp nhận và cấp phát vé (handle). Việc dắt xe vào bãi (I/O chờ đĩa/mạng) do khách tự thực hiện độc lập.")
    ], top=Pt(150.0), height=Pt(170.0), font_size=Pt(12.0))
    add_card(s16, "Ý NGHĨA KỸ THUẬT CỦA VÍ DỤ 'BÃI GIỮ XE':", [
        ("Nhân viên bảo vệ", "Bộ điều phối Event Loop (chỉ có 1 luồng duy nhất nhưng xử lý hàng nghìn khách)."),
        ("Vé gửi xe", "Đối tượng Future / Task trong Python (giữ quyền nhận kết quả sau này)."),
        ("Kết quả đạt được", "Không một ai bị chặn ở cổng bãi xe, hệ thống đạt thông lượng (Throughput) tối đa!")
    ], Pt(28.34), Pt(345.0), Pt(735.0), Pt(170.0), border_color=COLOR_BLUE)
    add_speaker_notes(s16, "Ví dụ Bãi giữ xe trong slide 7 giải thích tuyệt vời mô hình Non-blocking: Bác bảo vệ không chờ khách dắt xe vào vị trí mới tiếp người sau. Bác chỉ quét thẻ, phát vé rồi tiếp tục ngay lập tức.")

    # =========================================================================
    # SLIDE 17: MÔ HÌNH BẤT ĐỒNG BỘ TRÊN MỘT LUỒNG ĐIỀU KHIỂN DUY NHẤT (Slide 8 gốc)
    # =========================================================================
    s17 = create_slide_base(prs, 17, "GIỚI THIỆU", "Single Thread of Control (Slide 8 gốc)")
    add_content_title(s17, "Mô hình bất đồng bộ thực thi đồng thời trên một luồng điều khiển")
    add_bullets(s17, [
        ("Thực hiện xen kẽ trong một khoảng thời gian", "Trong một khoảng thời gian xác định, các task được thực hiện xen kẽ nhau linh hoạt."),
        ("Nằm trong một luồng điều khiển duy nhất", "Toàn bộ mô hình chạy trong MỘT LUỒNG ĐIỀU KHIỂN CHÍNH DUY NHẤT (Single Thread of Control)."),
        ("Nguyên tắc thực thi luồng đơn", "Khi 1 task đang thực thi thì các task khác KHÔNG THỰC THI; việc thực thi của 1 task có thể bị TẠM DỪNG và sau đó TIẾP TỤC LẠI."),
        ("Phạm vi ứng dụng rộng rãi", "Áp dụng hiệu quả cả trong hệ thống đơn bộ xử lý (Uniprocessor systems) lẫn hệ thống đa bộ xử lý (Multiprocessor systems).")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    s17.shapes.add_picture(os.path.join(IMG_DIR, "diag_orig_async_single_thread.png"), Pt(28.34), Pt(325.0), Pt(735.0), Pt(195.0))
    add_speaker_notes(s17, "Slide 17 là slide kết luận cực kỳ quan trọng của phần Giới thiệu (Slide 8 gốc): Bất đồng bộ thực thi đồng thời nằm trong MỘT LUỒNG ĐIỀU KHIỂN DUY NHẤT. Task có thể tạm dừng và tiếp tục lại sau.")

    # =========================================================================
    # SLIDE 18: CƠ CHẾ TẠM DỪNG (SUSPEND) & TIẾP TỤC LẠI (RESUME)
    # =========================================================================
    s18 = create_slide_base(prs, 18, "GIỚI THIỆU", "Cơ chế Tạm dừng & Tiếp tục lại")
    add_content_title(s18, "Cơ chế sâu sắc: Tạm dừng (Suspend) và Tiếp tục lại (Resume)")
    add_bullets(s18, [
        ("Điểm nhượng quyền chủ động (Yield Point)", "Khác với lập lịch cưỡng bức của hệ điều hành, trong mô hình này tác vụ CHỦ ĐỘNG TẠM DỪNG khi nó biết mình phải chờ đợi I/O."),
        ("Lưu trữ trạng thái Coroutine (Frame State)", "Khi tạm dừng, con trỏ lệnh và các biến cục bộ của hàm không bị xóa khỏi bộ nhớ, mà được đóng gói lưu trữ lại an toàn."),
        ("Sự tiếp tục lại thông minh (Resume)", "Khi tài nguyên I/O sẵn sàng, tác vụ được đánh thức và tiếp tục chạy ngay tại vị trí vừa tạm dừng như thể chưa từng bị gián đoạn."),
        ("Không tốn tài nguyên chuyển ngữ cảnh nặng", "Việc tạm dừng và tiếp tục diễn ra hoàn toàn ở tầng ứng dụng (User Space), không cần gọi xuống nhân hệ điều hành (Kernel Space).")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s18, "SO SÁNH CƠ CHẾ DỪNG GIỮA HỆ ĐIỀU HÀNH VÀ ASYNC:", [
        ("Preemptive Scheduling (HĐH)", "HĐH tự động ngắt ép buộc tiến trình bất kỳ lúc nào ➔ Tốn chi phí lưu trữ phần cứng lớn."),
        ("Cooperative Scheduling (Async)", "Tác vụ tự giác nhường CPU tại các lệnh chờ (như 'await') ➔ Cực kỳ nhẹ, có thể chạy hàng triệu tác vụ!"),
        ("Ý nghĩa", "Cho phép 1 luồng duy nhất phục vụ hàng trăm nghìn kết nối mạng đồng thời mà không bị tràn bộ nhớ.")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_RED)
    add_speaker_notes(s18, "Slide 18 phân tích cơ chế Tạm dừng và Tiếp tục lại. Đây là chìa khóa của lập trình Coroutine trong Python: Khi gặp await, nó chủ động nhường quyền, và khi có dữ liệu thì tiếp tục chạy lại ngay điểm đó.")

    # =========================================================================
    # SLIDE 19: ỨNG DỤNG TRÊN UNIPROCESSOR & MULTIPROCESSOR (Slide 8 gốc)
    # =========================================================================
    s19 = create_slide_base(prs, 19, "GIỚI THIỆU", "Khả năng Ứng dụng trên Mọi Hệ thống Phần cứng")
    add_content_title(s19, "Tính linh hoạt: Hiệu quả trên cả Uniprocessor và Multiprocessor")
    add_bullets(s19, [
        ("Trên hệ thống Đơn bộ xử lý (Uniprocessor - 1 CPU)", "Mô hình bất đồng bộ luồng đơn phát huy hiệu quả tối đa: Tận dụng thời gian rảnh của 1 CPU duy nhất để không bị chết nghẽn bởi các tác vụ I/O chậm chạp."),
        ("Trên hệ thống Đa bộ xử lý (Multiprocessor - Nhiều CPU)", "Mô hình vẫn hoạt động hoàn hảo: Mỗi nhân CPU có thể chạy một tiến trình chứa một luồng điều khiển bất đồng bộ riêng biệt."),
        ("Tính độc lập phần cứng", "Mô hình bất đồng bộ không phụ thuộc vào việc máy tính có bao nhiêu nhân vật lý để có thể đem lại lợi ích hiệu năng."),
        ("Tiết kiệm chi phí phần cứng", "Các máy chủ chỉ cần 1 lõi hoặc 2 lõi vẫn có thể chịu tải hàng chục nghìn kết nối mạng khi áp dụng mô hình bất đồng bộ.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s19, "KHẲNG ĐỊNH CỦA BÀI GIẢNG GỐC TẠI TRANG 8:", [
        ("Đơn bộ xử lý (Uniprocessor)", "Vẫn đạt hiệu năng vượt trội nhờ tối ưu hóa chu kỳ nhàn rỗi của vi xử lý."),
        ("Đa bộ xử lý (Multiprocessor)", "Có thể kết hợp nhiều luồng bất đồng bộ trên các nhân khác nhau để tăng tốc gấp bội."),
        ("Kết luận", "Bất đồng bộ là giải pháp kiến trúc phần mềm tối ưu độc lập với cấu hình phần cứng bên dưới!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_BLUE)
    add_speaker_notes(s19, "Slide 19 chứng minh nhận định ở cuối slide 8 gốc: Mô hình này áp dụng tốt cho cả máy 1 CPU lẫn máy nhiều CPU. Đây là giải pháp phần mềm tối ưu giúp tiết kiệm chi phí phần cứng máy chủ tối đa.")

    # =========================================================================
    # SLIDE 20: PHÂN BIỆT BẤT ĐỒNG BỘ LUỒNG ĐƠN VS ĐA LUỒNG (MULTI-THREADING)
    # =========================================================================
    s20 = create_slide_base(prs, 20, "ĐỐI CHIẾU", "Phân biệt Bất đồng bộ Luồng đơn vs Đa luồng")
    add_content_title(s20, "Phân biệt then chốt: Async Single-thread vs Multi-threading")
    
    t20_h = ["Đặc tính kỹ thuật", "Async Single-thread (Luồng đơn Bất đồng bộ)", "Multi-threading (Đa luồng truyền thống)"]
    t20_r = [
        ["Số luồng điều khiển", "Duy nhất 1 luồng hệ điều hành (1 OS Thread)", "Nhiều luồng chạy đồng thời (N OS Threads)"],
        ["Tiêu tốn bộ nhớ RAM", "Cực thấp (khoảng vài KB cho mỗi tác vụ)", "Cao (mỗi luồng tốn từ 1MB đến 8MB Stack memory)"],
        ["Hiện tượng Race Condition", "Không bao giờ xảy ra giữa các coroutines", "Rất dễ xảy ra nếu không dùng Lock / Mutex cẩn thận"],
        ["Hiện tượng Deadlock", "Hầu như không bị khóa chết luồng", "Nguy cơ Deadlock rất cao khi khóa chéo tài nguyên"],
        ["Chi phí chuyển đổi", "Cực nhẹ (User-space context switch)", "Nặng (Kernel-space thread context switch)"],
        ["Khả năng mở rộng", "Có thể xử lý 100,000+ kết nối đồng thời", "Thường bị giới hạn ở vài nghìn luồng là quá tải"]
    ]
    add_table_box(s20, t20_h, t20_r, Pt(28.34), Pt(165.0), Pt(735.0), Pt(350.0), col_widths=[155, 290, 290])
    add_speaker_notes(s20, "Bảng đối chiếu Slide 20 giúp giải đáp thắc mắc lớn nhất của sinh viên: Tại sao lại dùng luồng đơn bất đồng bộ thay vì dùng đa luồng? Vì nó nhẹ hơn hàng trăm lần và không lo bị Race Condition hay Deadlock!")

    # =========================================================================
    # SLIDE 21: MINH HỌA MÃ NGUỒN PYTHON: DÒNG ĐIỀU KHIỂN SYNC VS ASYNC
    # =========================================================================
    s21 = create_slide_base(prs, 21, "MINH HỌA PYTHON", "Minh họa Dòng điều khiển Đồng bộ vs Bất đồng bộ")
    add_content_title(s21, "Minh họa mã nguồn Python: Sự khác biệt về luồng điều khiển")
    add_bullets(s21, [
        ("Mã đồng bộ tuần tự (Synchronous)", "Sử dụng hàm `time.sleep()`. Khi gặp lệnh này, toàn bộ tiến trình bị đóng băng (blocking), không làm được việc gì khác."),
        ("Mã bất đồng bộ (Asynchronous)", "Sử dụng từ khóa `async def` và `await asyncio.sleep()`. Lệnh `await` chủ động nhường quyền cho Event Loop để chạy tác vụ khác."),
        ("Quan sát thời gian thực tế", "Đo thời gian hoàn thành 3 tác vụ (mỗi tác vụ chờ 1 giây): Mã đồng bộ mất 3 giây; mã bất đồng bộ chỉ mất 1 giây duy nhất!")
    ], top=Pt(150.0), height=Pt(120.0), font_size=Pt(11.5))
    
    add_card(s21, "CODE 1: ĐỒNG BỘ TUẦN TỰ (MẤT 3 GIÂY)", [
        ("Cú pháp", "import time"),
        ("Thực thi", "def fetch(i): time.sleep(1) # Bị chặn luồng hoàn toàn"),
        ("Kết quả", "fetch(1); fetch(2); fetch(3) ➔ Tổng thời gian = 3.0s")
    ], Pt(28.34), Pt(280.0), Pt(360.0), Pt(230.0), border_color=COLOR_RED)

    add_card(s21, "CODE 2: BẤT ĐỒNG BỘ LUỒNG ĐƠN (MẤT 1 GIÂY)", [
        ("Cú pháp", "import asyncio"),
        ("Thực thi", "async def fetch(i): await asyncio.sleep(1) # Nhường quyền"),
        ("Kết quả", "await asyncio.gather(fetch(1), fetch(2), fetch(3)) ➔ Tổng = 1.0s!")
    ], Pt(400.0), Pt(280.0), Pt(363.0), Pt(230.0), border_color=COLOR_GREEN)

    add_speaker_notes(s21, "Slide 21 đưa ra ví dụ code Python cực kỳ đơn giản để minh họa. Một bên dùng time.sleep làm đơ luồng mất 3 giây, một bên dùng await asyncio.sleep nhường quyền và gom bằng gather chỉ mất đúng 1 giây.")

    # =========================================================================
    # SLIDE 22: BẢNG TỔNG KẾT TOÀN DIỆN 4 MÔ HÌNH CỦA THÀNH VIÊN 1
    # =========================================================================
    s22 = create_slide_base(prs, 22, "TỔNG KẾT NỀN TẢNG", "Bảng Tổng kết Toàn diện 4 Mô hình Thực thi")
    add_content_title(s22, "Bảng tổng hợp toàn diện kiến thức nền tảng của Thành viên 1")
    
    t22_h = ["Mô hình tính toán", "Số nhân CPU", "Số luồng điều khiển", "Cơ chế chính", "Ứng dụng phù hợp nhất"]
    t22_r = [
        ["1. Tuần tự (Sequential)", "1 nhân", "1 luồng", "Chạy nối tiếp từ đầu đến cuối theo thứ tự", "Bài toán đơn giản, script nhỏ, tính toán tuần tự"],
        ["2. Đồng thời (Concurrency)", "1 nhân", "1 hoặc nhiều", "Chia lát thời gian (time-slicing), xen kẽ", "Hệ thống phục vụ nhiều người dùng trên 1 máy"],
        ["3. Song song (Parallelism)", "≥ 2 nhân", "Nhiều luồng/tiến trình", "Thực thi đồng thời vật lý trên các lõi độc lập", "Tính toán khoa học, đồ họa 3D, xử lý dữ liệu lớn"],
        ["4. Bất đồng bộ (Async)", "1 nhân", "1 luồng duy nhất", "Nhường quyền khi chờ I/O, tạm dừng & tiếp tục", "Máy chủ web, mạng, truy vấn API, microservices"]
    ]
    add_table_box(s22, t22_h, t22_r, Pt(28.34), Pt(165.0), Pt(735.0), Pt(350.0), col_widths=[145, 95, 125, 185, 185])
    add_speaker_notes(s22, "Slide 22 là bảng đúc kết toàn bộ 8 slide đầu tiên. Đây là chiếc la bàn kiến trúc giúp người lập trình viên biết chính xác khi nào chọn mô hình nào cho bài toán của mình.")

    # =========================================================================
    # SLIDE 23: CẦU NỐI KỸ THUẬT: TỪ NỀN TẢNG TV1 CHUYỂN GIAO SANG TV2
    # =========================================================================
    s23 = create_slide_base(prs, 23, "CHUYỂN GIAO KỸ THUẬT", "Cầu nối Chuyển giao sang Phần II (concurrent.futures)")
    add_content_title(s23, "Cầu nối chuyển giao kỹ thuật sang Phần II của bài giảng")
    add_bullets(s23, [
        ("Nền tảng đã thiết lập (TV1)", "Đã hiểu rõ bản chất Tuần tự, Đồng thời, Song song và Bất đồng bộ. Đã phân định rõ ranh giới giữa phần cứng (đa nhân) và phần mềm (điều phối)."),
        ("Câu hỏi đặt ra cho thực tế", "Làm thế nào để lập trình viên Python tận dụng các mô hình này một cách tiện lợi nhất mà không phải tự quản lý luồng thủ công phức tạp?"),
        ("Giải pháp trong Python chuẩn", "Module `concurrent.futures` ra đời cung cấp giao diện Executor cấp cao và đối tượng Future để quản lý kết quả bất đồng bộ."),
        ("Sẵn sàng cho bài học tiếp theo", "Xin trân trọng giới thiệu Thành viên 2 (TV2) sẽ trình bày Phần II: Sử dụng Module `concurrent.futures` với `ThreadPoolExecutor`!")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(12.0))
    add_card(s23, "MẠCH LIÊN KẾT BÀI GIẢNG CHƯƠNG 4:", [
        ("Phần I (Slide 1 – 8, TV1)", "Nền tảng lý thuyết: Phân biệt 4 mô hình thực thi và cơ chế luồng đơn bất đồng bộ."),
        ("Phần II (Slide 9 – 12, TV2)", "Kỹ thuật thực chiến 1: Quản lý ThreadPoolExecutor và Future objects."),
        ("Phần III (Slide 13 – 15, TV3)", "Kỹ thuật thực chiến 2: Vượt rào cản GIL với ProcessPoolExecutor."),
        ("Phần IV - VI (Slide 16 – 24, TV4 - TV6)", "Chuyên sâu Asyncio: Event Loop, Coroutines, Pipeline và Tổng kết.")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_RED)
    add_speaker_notes(s23, "Slide 23 kết nối mạch giảng từ TV1 sang TV2. Sau khi đã nắm vững lý thuyết, câu hỏi tự nhiên là: Python cung cấp module nào để hiện thực hóa điều này? Đó chính là concurrent.futures do TV2 trình bày.")

    # =========================================================================
    # SLIDE 24: TỔNG KẾT & CÂU HỎI THẢO LUẬN MỞ ĐẦU CHƯƠNG
    # =========================================================================
    s24 = create_slide_base(prs, 24, "TỔNG KẾT & THẢO LUẬN", "Tổng kết Phần I & Câu hỏi Tương tác Lớp học", "KẾT THÚC PHẦN I")
    add_content_title(s24, "Tổng kết Phần I và Câu hỏi thảo luận tương tác với lớp học")
    add_bullets(s24, [
        ("Câu hỏi 1 (Về tính đồng thời)", "Một máy tính chỉ có duy nhất 1 nhân CPU vật lý thì có thể chạy song song (Parallelism) được không? Có thể chạy đồng thời (Concurrency) được không? Vì sao?"),
        ("Câu hỏi 2 (Về tính bất đồng bộ)", "Tại sao nói mô hình bất đồng bộ trong ví dụ 'Bãi giữ xe' lại giúp nâng cao thông lượng phục vụ mà không cần tuyển thêm nhân viên bảo vệ mới?"),
        ("Câu hỏi 3 (Về cơ chế luồng đơn)", "Trong mô hình luồng đơn bất đồng bộ (Slide 8 gốc), điều gì xảy ra nếu một tác vụ thực hiện tính toán số học rất nặng mà không chịu nhường quyền (không tạm dừng)?")
    ], top=Pt(150.0), height=Pt(160.0), font_size=Pt(12.0))
    add_card(s24, "THÔNG ĐIỆP CHỐT LẠI CỦA THÀNH VIÊN 1:", [
        ("1. Concurrency", "Nói về cách tổ chức và tiến triển xen kẽ nhiều công việc trên tài nguyên hữu hạn."),
        ("2. Parallelism", "Nói về khả năng thực thi đồng thời vật lý tại cùng thời điểm nhờ phần cứng đa nhân."),
        ("3. Asynchronous", "Nói về nghệ thuật không chờ đợi, tận dụng thời gian rảnh khi I/O tạm dừng để phục vụ công việc khác!"),
        ("Lời cảm ơn", "Cảm ơn cô và các bạn đã lắng nghe phần trình bày của Thành viên 1!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), border_color=COLOR_DARK)
    add_speaker_notes(s24, "Em xin kết thúc phần trình bày của Thành viên 1 tại đây. 3 câu hỏi thảo luận này sẽ giúp lớp khắc sâu bài học. Kính mời cô và các bạn đưa ra câu hỏi hoặc mời bạn TV2 tiếp tục phần trình bày!")

    # Lưu file
    out_file = "TV1_BaiGiang_ChuyenSau_24Slide_C4.pptx"
    prs.save(out_file)
    print(f"XUẤT BẢN THÀNH CÔNG BỘ SLIDE CHUYÊN SÂU 24 SLIDE TV1: {out_file} (Kích thước: {os.path.getsize(out_file):,} bytes)")

    try:
        prs.save("TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx")
        print("ĐÃ GHI ĐÈ VÀO: TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx")
    except PermissionError:
        print("LƯU Ý: TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx đang mở trong ứng dụng khác. Đã lưu an toàn tại TV1_BaiGiang_ChuyenSau_24Slide_C4.pptx")

def main():
    prs = Presentation()
    prs.slide_width = Pt(793.8)
    prs.slide_height = Pt(595.2)
    build_tv1_master_presentation(prs)

if __name__ == "__main__":
    main()
