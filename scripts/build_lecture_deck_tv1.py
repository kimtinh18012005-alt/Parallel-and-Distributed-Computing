# -*- coding: utf-8 -*-
"""
build_lecture_deck_tv1.py
Tạo bộ slide BÀI GIẢNG ĐẠI HỌC CHÍNH QUY (24 Slide chuẩn mực môn Tính toán song song và phân tán)
- Chuẩn phong cách giảng dạy đại học: KHÔNG dùng nhãn máy móc WHAT/HOW, thay bằng cấu trúc sư phạm tự nhiên, logic dẫn dắt từ trực quan đến bản chất hệ điều hành và kỹ thuật lập trình.
- Tỷ lệ 4:3 chuẩn mẫu bài giảng C4 của CTUET (793.8 pt x 595.2 pt).
- Header đỏ #E74C3C, Footer 3 khối chuẩn bài giảng.
- Nhúng sơ đồ đồ họa chất lượng cao vào các slide kỹ thuật để bài giảng trực quan, hấp dẫn, thú vị.
- Tích hợp Giáo án bài giảng chi tiết (Speaker Notes) trên từng slide hỗ trợ người dạy tương tác với lớp.
"""

import os
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
COLOR_CODE_BG = RGBColor(240, 243, 244) # #F0F3F4
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
    p_mid.font.size = Pt(12)
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
    tx_box = slide.shapes.add_textbox(Pt(28.34), Pt(122.0), Pt(735.0), Pt(32.0))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_top = Pt(0)
    tf.margin_left = Pt(0)
    p = tf.paragraphs[0]
    p.text = f"➢ {text}"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK
    return tx_box

def add_bullets(slide, items, left=Pt(28.34), top=Pt(155.0), width=Pt(735.0), height=Pt(160.0), font_size=Pt(12.0)):
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_top = Pt(0)
    tf.margin_left = Pt(0)
    
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(5)
        p.space_before = Pt(2)
        
        if isinstance(item, tuple):
            prefix, body = item
            r_pre = p.add_run()
            r_pre.text = f"□ {prefix}: "
            r_pre.font.name = "Arial"
            r_pre.font.size = font_size
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_DARK
            
            r_body = p.add_run()
            r_body.text = body
            r_body.font.name = "Arial"
            r_body.font.size = font_size
            r_body.font.color.rgb = COLOR_BODY
        else:
            r = p.add_run()
            r.text = f"□ {item}"
            r.font.name = "Arial"
            r.font.size = font_size
            r.font.color.rgb = COLOR_BODY
    return tx_box

def add_speaker_notes(slide, lecture_script, discussion_question):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = f"[GIÁO ÁN GIẢNG DẠY CỦA GIẢNG VIÊN / THUYẾT TRÌNH VIÊN]:\n{lecture_script}\n\n[CÂU HỎI TƯƠNG TÁC VỚI SINH VIÊN & CHUYỂN TIẾP CHỦ ĐỀ]:\n➔ \"{discussion_question}\""

def add_styled_card(slide, title, content_lines, left, top, width, height, bg_col=COLOR_CARD_BG, border_col=COLOR_GRAY, title_col=COLOR_DARK):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_col
    card.line.color.rgb = border_col
    card.line.width = Pt(1.2)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_top = Pt(8)
    tf.margin_left = Pt(12)
    tf.margin_right = Pt(12)
    tf.margin_bottom = Pt(8)
    
    if title:
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Arial"
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = title_col
        p0.space_after = Pt(4)
        
    for i, line in enumerate(content_lines):
        p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
        p.space_after = Pt(3)
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_BODY
        if isinstance(line, tuple):
            k, v = line
            r1 = p.add_run()
            r1.text = f"• {k}: "
            r1.font.bold = True
            r1.font.color.rgb = COLOR_DARK
            r2 = p.add_run()
            r2.text = str(v)
            r2.font.color.rgb = COLOR_BODY
        else:
            r = p.add_run()
            r.text = f"• {line}"
    return card

def add_table_box(slide, headers, rows, left, top, width, height, col_widths=None):
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height)
    table = table_shape.table
    
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_RED
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            bg_col = COLOR_WHITE if row_idx % 2 == 0 else COLOR_CARD_BG
            cell.fill.fore_color.rgb = bg_col
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(cell_value)
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_BODY
            
    if col_widths:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = Pt(w)
            
    return table_shape

def build_all_24_lecture_slides(prs):
    # =========================================================================
    # SLIDE 1: BÌA BÀI GIẢNG CHÍNH QUY (Khớp mẫu chuẩn C4)
    # =========================================================================
    blank_layout = prs.slide_layouts[6]
    s1 = prs.slides.add_slide(blank_layout)
    
    tx_top = s1.shapes.add_textbox(Pt(28.34), Pt(45.0), Pt(735.0), Pt(65.0))
    tf_top = tx_top.text_frame
    p_t1 = tf_top.paragraphs[0]
    p_t1.text = "TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ (CTUET)"
    p_t1.font.name = "Arial"
    p_t1.font.size = Pt(14)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_DARK
    
    p_t2 = tf_top.add_paragraph()
    p_t2.text = "KHOA CÔNG NGHỆ THÔNG TIN — HỌC PHẦN: TÍNH TOÁN SONG SONG VÀ PHÂN TÁN"
    p_t2.font.name = "Arial"
    p_t2.font.size = Pt(11.5)
    p_t2.font.color.rgb = COLOR_GRAY

    # Băng đỏ ngang ở giữa
    mid_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(0), Pt(235.0), Pt(765.36), Pt(125.0))
    mid_bar.fill.solid()
    mid_bar.fill.fore_color.rgb = COLOR_RED
    mid_bar.line.fill.background()
    
    tf_mid = mid_bar.text_frame
    tf_mid.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_mid.margin_left = Pt(28.34)
    p_m1 = tf_mid.paragraphs[0]
    p_m1.text = "CHƯƠNG  4:"
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(26)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_WHITE
    
    p_m2 = tf_mid.add_paragraph()
    p_m2.text = "TÍNH TOÁN BẤT ĐỒNG BỘ TRONG PYTHON"
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(30)
    p_m2.font.bold = True
    p_m2.font.color.rgb = COLOR_WHITE

    tx_bot = s1.shapes.add_textbox(Pt(28.34), Pt(385.0), Pt(735.0), Pt(140.0))
    tf_bot = tx_bot.text_frame
    p_b1 = tf_bot.paragraphs[0]
    p_b1.text = "BÀI GIẢNG CHUYÊN ĐỀ 1: NỀN TẢNG LÝ THUYẾT & BẢN ĐỒ TƯ DUY TÍNH TOÁN HIỆU NĂNG CAO"
    p_b1.font.name = "Arial"
    p_b1.font.size = Pt(13.5)
    p_b1.font.bold = True
    p_b1.font.color.rgb = COLOR_DARK
    
    p_b2 = tf_bot.add_paragraph()
    p_b2.text = "Phân định 7 Khái niệm Cốt lõi, Mô hình Hóa Workload, Giới hạn Tăng tốc Amdahl & Sequential Oracle"
    p_b2.font.name = "Arial"
    p_b2.font.size = Pt(12)
    p_b2.font.bold = True
    p_b2.font.color.rgb = COLOR_ORANGE
    
    p_b3 = tf_bot.add_paragraph()
    p_b3.text = "Giảng viên phụ trách: ThS. Lê Anh Nhã Uyên (lanuyen@ctuet.edu.vn)\nNhóm biên soạn & Báo cáo: Thành viên 1 (Nền tảng & Oracle) — Hỗ trợ kỹ thuật: Thành viên 4 (Asyncio Runtime)"
    p_b3.font.name = "Arial"
    p_b3.font.size = Pt(10.5)
    p_b3.font.color.rgb = COLOR_BODY

    add_speaker_notes(s1,
        "Chào cả lớp. Hôm nay chúng ta bước vào một trong những chương quan trọng và thực chiến nhất của học phần Tính toán song song và phân tán: Chương 4 - Tính toán bất đồng bộ trong Python. Trước khi học cú pháp của bất kỳ thư viện nào như asyncio, threadpool hay processpool, bài học mở đầu hôm nay sẽ giúp các em xây dựng một nền tảng tư duy vững chắc, phân biệt rạch ròi bản chất vận hành ở tầng hệ điều hành để không bao giờ bị nhầm lẫn khi thiết kế hệ thống.",
        "Tại sao trong thời đại CPU có tới hàng chục nhân xử lý, các chương trình phần mềm của chúng ta vẫn thường xuyên bị nghẽn và phản hồi chậm chạp?")

    # =========================================================================
    # SLIDE 2: MỤC TIÊU HỌC TẬP & BẢN ĐỒ KIẾN THỨC BÀI GIẢNG
    # =========================================================================
    s2 = create_slide_base(prs, 2, "TỔNG QUAN BÀI HỌC", "Mục tiêu Học tập & Bản đồ Kiến thức Chuyên đề")
    add_content_title(s2, "Những giá trị học thuật và kỹ năng kỹ thuật người học sẽ làm chủ")
    add_bullets(s2, [
        ("Nắm vững bản chất kiến trúc", "Phân biệt chính xác tuyệt đối 7 khái niệm cốt lõi: Tuần tự, Đồng thời, Song song, Đồng bộ, Bất đồng bộ, Blocking và Non-blocking."),
        ("Hiểu sâu cơ chế hệ điều hành", "Làm chủ kiến trúc bộ nhớ và cơ chế lập lịch: Tranh đoạt (Preemptive) vs Hợp tác (Cooperative), Context Switch, Yield point và rào cản CPython GIL."),
        ("Định lượng và Ra quyết định", "Nhận diện bản chất Workload (I/O-bound vs CPU-bound); áp dụng Định luật Amdahl để tính toán trần tăng tốc lý thuyết và dự báo suy thoái do Overhead."),
        ("Chuẩn mực kỹ thuật công nghiệp", "Thiết lập phương pháp luận kiểm chuẩn khoa học (Correctness First) và quy trình đo lường hiệu năng công bằng với mốc chân lý Sequential Baseline Oracle.")
    ], top=Pt(150.0), height=Pt(170.0), font_size=Pt(11.5))

    add_styled_card(s2, "TRỤ CỘT LÝ THUYẾT HỆ THỐNG", [
        ("Vòng đời tác vụ (Task Lifecycle)", "Từ trạng thái Ready, Running đến Blocked/Suspended."),
        ("Không gian địa chỉ (Address Space)", "Phân biệt Virtual Address Space cô lập vs Shared Heap."),
        ("Giới hạn toán học (Amdahl's Law)", "Chứng minh vì sao thêm worker không đồng nghĩa nhanh hơn.")
    ], Pt(28.34), Pt(335.0), Pt(355.0), Pt(180.0), bg_col=COLOR_CARD_BG, border_col=COLOR_BLUE)

    add_styled_card(s2, "KỸ NĂNG THỰC HÀNH KỸ SƯ", [
        ("Xây dựng Data Contract", "Thiết kế cấu trúc dữ liệu chuẩn hóa và seed xác định."),
        ("Chống bẫy Anti-Pattern", "Phát hiện và loại bỏ triệt để lệnh blocking trong luồng async."),
        ("Thẩm định Benchmark", "Sử dụng đồng hồ độ phân giải cao và mã băm SHA-256 Digest.")
    ], Pt(408.0), Pt(335.0), Pt(355.0), Pt(180.0), bg_col=COLOR_CARD_BG, border_col=COLOR_GREEN)

    add_speaker_notes(s2,
        "Thầy/cô muốn nhấn mạnh với các em: Lập trình viên giỏi khác lập trình viên trung bình ở chỗ họ hiểu điều gì đang thực sự xảy ra bên dưới kernel khi một dòng lệnh được thực thi. Sau bài học này, các em sẽ tự tin trả lời bất kỳ câu hỏi phỏng vấn nào về Concurrency và Async.",
        "Để bắt đầu, chúng ta hãy cùng khảo sát một bài toán thực tế mà bất kỳ kỹ sư phần mềm nào cũng sẽ gặp phải: Bài toán quan trắc trạm cảm biến môi trường!")

    # =========================================================================
    # SLIDE 3: BÀI TOÁN QUAN TRẮC MÔI TRƯỜNG & NGHỊCH LÝ THỜI GIAN CHỜ
    # =========================================================================
    s3 = create_slide_base(prs, 3, "NGHIÊN CỨU TÌNH HUỐNG", "Bài toán Quan trắc Trạm Cảm biến Môi trường")
    add_content_title(s3, "Khảo sát hệ thống thu thập dữ liệu quan trắc 8 trạm cảm biến")
    add_bullets(s3, [
        ("Bối cảnh kỹ thuật", "Hệ thống giám sát chất lượng không khí thu thập dữ liệu từ 8 trạm cảm biến qua mạng; mỗi trạm mất khoảng 0.12s trễ I/O truyền gói tin, sau đó CPU mất 0.03s để tính chỉ số ô nhiễm AQI."),
        ("Thực thi tuần tự truyền thống", "Các trạm được truy vấn lần lượt nối tiếp nhau trong một vòng lặp; tổng thời gian xử lý toàn bộ hệ thống là tổng của từng trạm riêng lẻ: T_total = SUM(T_i) ≈ 1.20 giây."),
        ("Ba câu hỏi hóc búa đặt ra", "1) Khoảng thời gian chờ mạng của các trạm có thể chồng lấp (overlap) lên nhau không? 2) Phần tính toán số học có thể chạy song song không? 3) Chi phí đánh đổi để tối ưu là bao nhiêu?")
    ], top=Pt(150.0), height=Pt(160.0), font_size=Pt(11.5))
    s3.shapes.add_picture(os.path.join(IMG_DIR, "diag_s1_timeline_8stations.png"), Pt(28.34), Pt(325.0), Pt(735.0), Pt(195.0))

    add_speaker_notes(s3,
        "Hãy nhìn lên biểu đồ timeline trên màn hình: Trong tổng số 1.20 giây xử lý, các khối màu xanh dương biểu thị CPU tính toán chỉ chiếm vỏn vẹn 0.24 giây. Còn lại tới 0.96 giây (chiếm đến 80% thời gian - các khối màu cam gạch chéo), nhân CPU hoàn toàn không làm gì cả, chỉ ngồi chờ gói tin từ mạng internet quay về. Đây chính là hiện tượng 'CPU đói dữ liệu'.",
        "Tại sao một cỗ máy tính hiện đại có xung nhịp hàng tỷ chu kỳ mỗi giây lại chấp nhận ngồi yên chờ đợi như vậy? Hãy nhìn vào kiến trúc Call Stack và cơ chế thực thi tuần tự!")

    # =========================================================================
    # SLIDE 4: GIẢI PHẪU TẦNG THẤP: CALL STACK & HIỆN TƯỢNG IDLE WAIT
    # =========================================================================
    s4 = create_slide_base(prs, 4, "BẢN CHẤT PHẦN CỨNG", "Call Stack, Program Counter & Lãng phí Chu kỳ CPU")
    add_content_title(s4, "Vì sao mô hình tuần tự gây lãng phí hàng tỷ chu kỳ tính toán?")
    add_bullets(s4, [
        ("Con trỏ lệnh đơn (Program Counter - PC)", "Trong mô hình tuần tự đơn luồng, CPU chỉ duy trì duy nhất một Call Stack và một con trỏ lệnh PC trỏ tuần tự đến từng lệnh máy tiếp theo."),
        ("Trạng thái luồng bị khóa (Blocked State)", "Khi chương trình thực thi lời gọi hệ thống đọc dữ liệu mạng (socket.recv), OS Kernel nhận thấy chưa có gói tin và lập tức chuyển luồng từ trạng thái RUNNING sang BLOCKED."),
        ("Lãng phí hàng tỷ chu kỳ lệnh", "Một CPU 3.0 GHz xử lý được 3 tỷ chu kỳ lệnh/giây. Việc luồng bị dừng 100ms chờ mạng tương đương với việc CPU bỏ phí 300 triệu cơ hội tính toán."),
        ("Nhận định quan trọng", "Nút thắt cổ chai ở đây là NGHẼN I/O (I/O Bottleneck), hoàn toàn không phải do CPU bị yếu hay thuật toán tính AQI bị chậm!")
    ], top=Pt(150.0), height=Pt(160.0), font_size=Pt(11.5))

    t4_h = ["Trạm quan trắc", "Thời gian chờ mạng (I/O Wait)", "Thời gian CPU xử lý", "Trạng thái luồng OS", "Chu kỳ lệnh bị bỏ phí"]
    t4_r = [
        ["STA-001 (Ninh Kiều)", "0.12 giây (Chờ gói tin mạng)", "0.03 giây (Tính AQI)", "BLOCKED ➔ RUNNING", "~ 360.000.000 chu kỳ"],
        ["STA-002 (Cái Răng)", "0.12 giây (Chờ gói tin mạng)", "0.03 giây (Tính AQI)", "BLOCKED ➔ RUNNING", "~ 360.000.000 chu kỳ"],
        ["STA-003 (Bình Thủy)", "0.12 giây (Chờ gói tin mạng)", "0.03 giây (Tính AQI)", "BLOCKED ➔ RUNNING", "~ 360.000.000 chu kỳ"],
        ["Tổng cộng 8 trạm", "0.96 giây (Chiếm 80.0%)", "0.24 giây (Chiếm 20.0%)", "Tổng thời gian: 1.20s", "Gần 3 TỶ CHU KỲ LÃNG PHÍ!"]
    ]
    add_table_box(s4, t4_h, t4_r, Pt(28.34), Pt(330.0), Pt(735.0), Pt(185.0), col_widths=[140, 150, 140, 145, 160])

    add_speaker_notes(s4,
        "Số liệu 3 tỷ chu kỳ lãng phí là một con số giật mình. Nếu chúng ta có thể tận dụng khoảng thời gian 80% nhàn rỗi này để CPU chuyển sang xử lý phân tích dữ liệu cho trạm khác thì hiệu năng hệ thống sẽ tăng vọt mà không cần tốn thêm một đồng nâng cấp phần cứng nào.",
        "Ý tưởng này dẫn chúng ta đến một khái niệm kinh điển trong khoa học máy tính: Tính toán đồng thời (Concurrency)!")

    # =========================================================================
    # SLIDE 5: TÍNH TOÁN ĐỒNG THỜI (CONCURRENCY): NGHỆ THUẬT ĐIỀU PHỐI TIẾN TRIỂN
    # =========================================================================
    s5 = create_slide_base(prs, 5, "NGHỆ THUẬT ĐIỀU PHỐI", "Tính toán Đồng thời (Concurrency) & Sự Tiến triển")
    add_content_title(s5, "Quản lý nhiều tác vụ cùng có tiến triển trên tài nguyên hạn chế")
    add_bullets(s5, [
        ("Định nghĩa học thuật chuẩn xác", "Concurrency là khả năng của một hệ thống trong việc cấu trúc, phân chia và điều phối nhiều tác vụ độc lập sao cho chúng CÙNG CÓ TIẾN TRIỂN (making progress) trong một khoảng thời gian."),
        ("Phát biểu kinh điển của Rob Pike", "\"Concurrency is about DEALING with lots of things at once. Parallelism is about DOING lots of things at once.\" — Concurrency là cách tổ chức cấu trúc của chương trình, không phải là thuộc tính phần cứng!"),
        ("Ẩn dụ thực tế: Người đầu bếp một bếp", "Một đầu bếp phục vụ 4 món ăn bằng cách: đặt ấm nước lên đun (I/O wait), trong lúc chờ nước sôi quay sang thái thịt (CPU), rồi chuyển sang xào rau. Tại mỗi thời điểm vi mô đầu bếp chỉ làm 1 việc, nhưng cả 4 món đều đang tiến triển!")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(11.5))

    add_styled_card(s5, "CƠ CHẾ LẬP LỊCH XEN KẼ (INTERLEAVING / TIME-SLICING)", [
        ("Chia nhỏ lát thời gian", "Hệ thống băm nhỏ công việc thành nhiều lát thời gian (Time slices) cực ngắn cỡ mili-giây."),
        ("Tận dụng khoảng chờ", "Ngay khi Trạm 1 chờ gói tin mạng, CPU lập tức chuyển ngữ cảnh sang xử lý tính toán cho Trạm 2."),
        ("Quy tắc vật lý vi mô", "Trên một nhân CPU đơn lẻ tại một thời điểm vi mô, CPU vẫn chỉ thực thi chỉ thị của duy nhất 1 tác vụ!")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), bg_col=COLOR_CARD_BG, border_col=COLOR_BLUE)

    add_speaker_notes(s5,
        "Thầy/cô muốn các em ghi nhớ thật kỹ: Concurrency KHÔNG ĐỒNG NGHĨA với việc chạy cùng một lúc. Nó là nghệ thuật sắp xếp công việc để lấp đầy những khoảng thời gian nhàn rỗi chết. Concurrency hoàn toàn có thể chạy mượt mà trên một chiếc máy tính cổ lỗ sĩ chỉ có 1 nhân CPU duy nhất.",
        "Vậy khi máy tính của chúng ta có nhiều nhân CPU vật lý thực sự, điều gì sẽ xảy ra? Đó chính là Tính toán song song (Parallelism)!")

    # =========================================================================
    # SLIDE 6: TÍNH TOÁN SONG SONG (PARALLELISM): THỰC THI VẬT LÝ ĐỒNG THỜI
    # =========================================================================
    s6 = create_slide_base(prs, 6, "THỰC THI ĐA NHÂN", "Tính toán Song song (Parallelism): Sức mạnh Đa lõi")
    add_content_title(s6, "Thực thi đồng thời vật lý tại cùng thời điểm trên nhiều nhân phần cứng")
    add_bullets(s6, [
        ("Định nghĩa học thuật chuẩn xác", "Parallelism là trạng thái mà nhiều lệnh hoặc tác vụ khác nhau được thi hành ĐỒNG THỜI VẬT LÝ tại CÙNG MỘT THỜI ĐIỂM (physically simultaneous execution) trên các đơn vị phần cứng độc lập."),
        ("Điều kiện phần cứng bắt buộc", "Chỉ có thể đạt được khi hệ thống sở hữu nhiều nhân CPU vật lý (Multi-core), nhiều socket vi xử lý, hoặc hàng nghìn lõi tính toán GPU."),
        ("So sánh trực quan 4 tác vụ A–D", "Tuần tự: 1 nhân làm lần lượt A➔B➔C➔D | Đồng thời: 1 nhân xen kẽ các lát của A, B, C, D | Song song: 4 nhân riêng biệt chạy A, B, C, D cùng lúc t0.")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))
    s6.shapes.add_picture(os.path.join(IMG_DIR, "diag_s2_compare_3_timelines.png"), Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0))

    add_speaker_notes(s6,
        "Quan sát 3 biểu đồ timeline trên màn hình: Ở chế độ 2 (Concurrency trên 1 Core), tổng thời gian có thể tương đương hoặc chỉ rút ngắn nếu có I/O overlap, nhưng hệ thống vẫn phản hồi nhịp nhàng. Trong khi ở chế độ 3 (Parallelism trên 4 Cores), tổng thời gian được co ngắn lại tới 4 lần vì 4 nhân vật lý cùng gánh tải độc lập tại thời điểm t0.",
        "Trong các hệ thống thực tế quy mô lớn, mối quan hệ giữa Concurrency, Parallelism và Hệ phân tán được phân tầng như thế nào?")

    # =========================================================================
    # SLIDE 7: HỆ THỐNG VỪA CONCURRENT VỪA PARALLEL & SO SÁNH VỚI HỆ PHÂN TÁN
    # =========================================================================
    s7 = create_slide_base(prs, 7, "GÓC NHÌN HỆ THỐNG", "Đa nhân Song song vs Hệ thống Phân tán (Distributed)")
    add_content_title(s7, "Phân tầng kiến trúc: Từ một vi xử lý đến cụm máy chủ phân tán")
    add_bullets(s7, [
        ("Mô hình kết hợp trong thực tế", "Một hệ điều hành hiện đại chạy trên CPU 16 nhân: Giữa các nhân với nhau diễn ra quá trình tính toán SONG SONG (Parallel); nhưng trên mỗi nhân đơn lẻ, OS vẫn liên tục LẬP LỊCH ĐỒNG THỜI (Concurrent) hàng trăm tiến trình nền!"),
        ("Sự khác biệt cốt tử với Hệ phân tán", "Tính toán đơn máy (dù song song đa nhân) CHIA SẺ CHUNG BỘ NHỚ RAM VẬT LÝ và chịu sự quản lý của 1 OS Kernel. Hệ phân tán kết nối nhiều máy tính qua mạng, KHÔNG chung RAM, chịu trễ mạng và sai lệch đồng hồ.")
    ], top=Pt(150.0), height=Pt(120.0), font_size=Pt(11.5))

    t7_h = ["Tiêu chí phân định", "Đồng thời đơn nhân (Concurrent)", "Song song đa nhân (Parallel)", "Hệ thống Phân tán (Distributed)"]
    t7_r = [
        ["Phần cứng tối thiểu", "1 Core CPU vật lý", "Nhiều Core CPU / Đa socket / GPU", "Nhiều máy chủ (Cluster / Nodes)"],
        ["Không gian bộ nhớ", "Chung RAM vật lý", "Chung RAM vật lý (Shared Memory)", "Bộ nhớ phân tán (Distributed Memory)"],
        ["Cơ chế truyền thông", "Biến bộ nhớ, Queue, Context switch", "Bộ nhớ chia sẻ, Khóa nguyên tử CAS", "Truyền thông điệp mạng (RPC / REST / MQ)"],
        ["Đồng bộ thời gian", "Chung đồng hồ phần cứng (Clock)", "Chung đồng hồ phần cứng (Clock)", "Sai lệch đồng hồ vật lý (Clock Skew)"],
        ["Mô hình hỏng hóc", "Sập luồng, deadlock nội bộ OS", "Tranh chấp bus RAM, cache miss", "Đứt cáp mạng, phân mảnh mạng (Partition)"]
    ]
    add_table_box(s7, t7_h, t7_r, Pt(28.34), Pt(280.0), Pt(735.0), Pt(235.0), col_widths=[140, 195, 195, 205])

    add_speaker_notes(s7,
        "Một sai lầm rất phổ biến của sinh viên khi làm đồ án là gọi một chương trình Python dùng asyncio trên laptop của mình là 'hệ phân tán'. Hãy nhớ: Khi nào hệ thống của các em chạy trên nhiều máy chủ độc lập không chung thanh RAM và phải giao tiếp qua mạng internet thì mới là hệ phân tán.",
        "Bây giờ, chúng ta bước sang cặp khái niệm thường xuyên gây tranh cãi và nhầm lẫn nhất: Synchronous/Asynchronous và Blocking/Non-blocking!")

    # =========================================================================
    # SLIDE 8: HAI TRỤC ĐỘC LẬP: HỢP ĐỒNG GỌI HÀM VS TRẠNG THÁI LUỒNG OS
    # =========================================================================
    s8 = create_slide_base(prs, 8, "MA TRẬN KHÁI NIỆM", "Sync/Async vs Blocking/Non-blocking: Hai Trục Độc lập")
    add_content_title(s8, "Bóc tách sự khác biệt: Hợp đồng giao tiếp vs Trạng thái luồng tầng OS")
    add_bullets(s8, [
        ("Nguyên lý phân định nền tảng", "Synchronous/Asynchronous và Blocking/Non-blocking là HAI TRỤC HOÀN TOÀN ĐỘC LẬP. Một thao tác có thể là Đồng bộ nhưng Non-blocking, hoặc Bất đồng bộ nhưng lại Blocking!"),
        ("Trục 1: Hợp đồng giao tiếp (Call Contract)", "Bên gọi (Caller) có chờ bên được gọi (Callee) trả kết quả ngay tại chỗ hay nhận một handle/Future rồi tiếp tục công việc khác?"),
        ("Trục 2: Trạng thái luồng hệ điều hành", "Khi thực thi lời gọi hệ thống (Syscall), OS Kernel có chuyển luồng sang trạng thái ngủ (BLOCKED) hay trả về quyền điều khiển ngay lập tức?")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))
    s8.shapes.add_picture(os.path.join(IMG_DIR, "diag_s3_matrix2x2.png"), Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0))

    add_speaker_notes(s8,
        "Các em hãy đặc biệt chú ý góc phần tư màu đỏ bên dưới: ASYNC - BLOCKING. Đây chính là 'bẫy tử thần' khiến rất nhiều lập trình viên dở khóc dở cười: Họ viết hàm với từ khóa async def nhưng bên trong lại gọi time.sleep() hoặc thư viện requests. Hậu quả là toàn bộ hệ thống bị đóng băng mà họ không hiểu vì sao.",
        "Vậy lệnh 'await' trong Python thực chất hoạt động như thế nào bên dưới nắp ca-pô?")

    # =========================================================================
    # SLIDE 9: GIẢI PHẪU LỆNH 'AWAIT': TẠM DỪNG HỢP TÁC CHỨ KHÔNG BLOCK LUỒNG
    # =========================================================================
    s9 = create_slide_base(prs, 9, "CƠ CHẾ ASYNCIO", "Bản chất Lệnh 'await' & Bẫy Anti-Pattern Tử thần")
    add_content_title(s9, "Hiểu đúng về await: Tạm dừng Coroutine chứ KHÔNG BLOCK Luồng OS!")
    add_bullets(s9, [
        ("Bản chất hoạt động của 'await'", "Khi gặp `await expr`: Coroutine hiện tại TỰ NGUYỆN TẠM DỪNG (Suspend) và trả quyền điều khiển (cooperative yield) về cho Event Loop. Luồng OS hoàn toàn TỈNH TÁO để chạy coroutine khác!"),
        ("Cơ chế đánh thức (Wake-up)", "Event Loop đăng ký socket mạng với hệ điều hành thông qua cơ chế Polling hiệu năng cao (epoll trên Linux, IOCP trên Windows). Khi có gói tin về, Loop kích hoạt lại coroutine đúng tại dòng lệnh cũ."),
        ("Quy tắc sinh tử trong Asyncio", "Bất kỳ thao tác I/O blocking hoặc tính toán CPU nặng thuần Python nào chạy thẳng trong luồng Event Loop sẽ LÀM ĐÓNG BĂNG toàn bộ hệ thống!")
    ], top=Pt(150.0), height=Pt(155.0), font_size=Pt(11.5))

    add_styled_card(s9, "ANTI-PATTERN TỬ THẦN (CẦN TUYỆT ĐỐI TRÁNH)", [
        ("Mã độc hại gây đóng băng", "async def fetch_station(id):\n    time.sleep(2.0)  # LỖI TỬ THẦN: Luồng OS bị ngủ cứng!\n    return data"),
        ("Hậu quả tai hại", "Toàn bộ Event Loop bị nghẽn trong 2.0s; 10.000 coroutine khác không thể tiến triển!"),
        ("Cách sửa chuẩn mực", "Thay bằng `await asyncio.sleep(2.0)` hoặc bọc qua ThreadPool bằng `run_in_executor()`.")
    ], Pt(28.34), Pt(320.0), Pt(355.0), Pt(195.0), bg_col=COLOR_CARD_BG, border_col=COLOR_DARK_RED, title_col=COLOR_DARK_RED)

    add_styled_card(s9, "MÔ HÌNH CHUẨN XÁC: NON-BLOCKING COOPERATIVE", [
        ("Mã chuẩn công nghiệp", "async def fetch_station(id):\n    data = await aiohttp_client.get(url)  # Nhường quyền!\n    return data"),
        ("Cơ chế vận hành ngầm", "Kernel OS quản lý I/O qua epoll; Coroutine nhường quyền, CPU phục vụ trạm khác ngay lập tức."),
        ("Năng lực chịu tải", "1 luồng đơn lẻ dễ dàng duy trì 50.000 đến 100.000 kết nối đồng thời với RAM tối thiểu.")
    ], Pt(408.0), Pt(320.0), Pt(355.0), Pt(195.0), bg_col=COLOR_CARD_BG, border_col=COLOR_GREEN, title_col=COLOR_GREEN)

    add_speaker_notes(s9,
        "Thầy/cô muốn các em khắc cốt ghi tâm: Từ khóa 'await' không có nghĩa là ngồi đợi thụ động. 'await' là lời đề nghị lịch sự: 'Tôi đang đợi dữ liệu mạng, nhường sân khấu lại cho Event Loop để bạn khác chạy đi, khi nào có hàng thì gọi tôi'.",
        "Ai là đơn vị thực thi những tác vụ này và chúng sử dụng bộ nhớ ra sao? Chúng ta cùng bước sang ba đơn vị thực thi nền tảng: Process, Thread và Coroutine!")

    # =========================================================================
    # SLIDE 10: BA ĐƠN VỊ THỰC THI: PROCESS, THREAD, COROUTINE
    # =========================================================================
    s10 = create_slide_base(prs, 10, "ĐƠN VỊ THỰC THI", "Process vs Thread vs Coroutine & Kiến trúc Bộ nhớ")
    add_content_title(s10, "Cấu trúc thứ bậc bộ nhớ và ranh giới cô lập tài nguyên")
    add_bullets(s10, [
        ("Tiến trình (Process)", "Sở hữu không gian địa chỉ ảo riêng biệt (Private Virtual Address Space). Các tiến trình hoàn toàn cô lập, an toàn bộ nhớ, giao tiếp qua cơ chế IPC tuần tự hóa dữ liệu."),
        ("Luồng (Thread)", "Đơn vị thực thi thuộc về một Process; các luồng chia sẻ chung Heap và Data segment của Process mẹ nhưng sở hữu riêng Call Stack và thanh ghi CPU."),
        ("Coroutine (Hàm đồng quy)", "Đơn vị thực thi logic siêu nhẹ do Runtime quản lý hoàn toàn trong User-space; hàng nghìn Coroutine cùng chia sẻ một Thread và một Call Stack của Event Loop.")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))
    s10.shapes.add_picture(os.path.join(IMG_DIR, "diag_s4_memory_hierarchy.png"), Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0))

    add_speaker_notes(s10,
        "Hãy nhìn vào sơ đồ phân tầng bộ nhớ: Process 1 và Process 2 là hai pháo đài cô lập. Muốn gửi dữ liệu qua lại, chúng bắt buộc phải thông qua đường ống IPC và chịu phí chuyển đổi nhị phân (Pickle). Trong khi đó, các Thread trong Process 1 dùng chung một vùng nhớ Heap nên giao tiếp cực nhanh, nhưng lại có nguy cơ tranh chấp dữ liệu (Race Condition).",
        "Hệ điều hành và Python Runtime quyết định lúc nào các đơn vị này được chạy dựa trên cơ chế lập lịch nào?")

    # =========================================================================
    # SLIDE 11: CƠ CHẾ LẬP LỊCH: TRANH ĐOẠT (PREEMPTIVE) VS HỢP TÁC (COOPERATIVE)
    # =========================================================================
    s11 = create_slide_base(prs, 11, "CƠ CHẾ LẬP LỊCH", "Lập lịch Tranh đoạt (Preemptive) vs Hợp tác (Cooperative)")
    add_content_title(s11, "Sự khác biệt bản chất giữa Lập lịch Hệ điều hành và Lập lịch Asyncio")
    add_bullets(s11, [
        ("Lập lịch Tranh đoạt (Preemptive Scheduling)", "Áp dụng cho Process và Thread. OS Kernel sử dụng bộ đếm ngắt phần cứng (Hardware Timer Interrupt) để ngắt cưỡng bức luồng đang chạy sau mỗi khoảng 10–20ms và chuyển quyền cho luồng khác."),
        ("Lập lịch Hợp tác (Cooperative Scheduling)", "Áp dụng cho Coroutine trong Asyncio. Coroutine KHÔNG BAO GIỜ BỊ NGẮT CƯỠNG BỨC. Nó chạy liên tục cho đến khi TỰ NGUYỆN NHƯỜNG QUYỀN tại các điểm `await` (Yield Points)."),
        ("Hiểm họa lập lịch hợp tác", "Nếu một coroutine dính vòng lặp vô tận tính toán (`while True:`), toàn bộ Event Loop sẽ bị treo vì không có cơ chế timer cưỡng bức ngắt nó!")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(11.5))

    add_styled_card(s11, "SO SÁNH CƠ CHẾ LẬP LỊCH TẦNG HỆ THỐNG", [
        ("Quyền kiểm soát", "Preemptive: Thuộc về Kernel OS | Cooperative: Thuộc về Lập trình viên tại điểm await."),
        ("Rủi ro tranh chấp dữ liệu", "Preemptive: Bị ngắt bất ngờ tại bất kỳ chỉ thị nào ➔ Cần Mutex/Lock | Cooperative: An toàn giữa 2 lệnh đồng bộ."),
        ("Chi phí chuyển đổi", "Preemptive: Mất hàng micro-giây nạp lại thanh ghi Kernel | Cooperative: Mất vài chục nano-giây chuyển hàm.")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), bg_col=COLOR_CARD_BG, border_col=COLOR_BLUE)

    add_speaker_notes(s11,
        "Đây là điểm mấu chốt: Với lập lịch hợp tác trong asyncio, nếu các em không chủ động nhường quyền (await), không một ai có thể giành quyền chạy từ tay coroutine của các em. Sự tự do này đem lại tốc độ siêu phàm nhưng đòi hỏi người viết mã phải cực kỳ kỷ luật.",
        "Để lượng hóa sự khác biệt tài nguyên giữa ba đơn vị này, chúng ta hãy cùng khảo sát bảng số liệu kỹ thuật chi tiết!")

    # =========================================================================
    # SLIDE 12: BẢNG SO SÁNH ĐỊNH LƯỢNG CHI PHÍ PROCESS, THREAD, COROUTINE
    # =========================================================================
    s12 = create_slide_base(prs, 12, "ĐỐI THOẠI KỸ THUẬT", "Bảng So sánh Định lượng: RAM, Ngữ cảnh & CPython GIL")
    add_content_title(s12, "Số liệu định lượng chi phí tài nguyên và giới hạn kiến trúc CPython")
    add_bullets(s12, [
        ("Chi phí bộ nhớ RAM", "1 Process tốn khoảng 15–30 MB; 1 Thread tốn khoảng 8 MB không gian địa chỉ ảo; 1 Coroutine chỉ tốn vỏn vẹn khoảng 1–2 KB!"),
        ("Thời gian chuyển ngữ cảnh (Context Switch)", "Chuyển giữa 2 Process mất 5–15 µs do phải nạp lại bảng trang MMU; chuyển Thread mất 1–3 µs; chuyển Coroutine chỉ mất 20–50 ns (nhanh gấp 100 lần luồng OS!)."),
        ("Rào cản CPython GIL (Global Interpreter Lock)", "Thread trong Python bị khóa bởi GIL nên KHÔNG THỂ chạy song song CPU trên đa nhân; muốn tính toán CPU thực sự bắt buộc phải dùng ProcessPool!")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))

    t12_h = ["Đặc tính kỹ thuật", "Tiến trình (Process)", "Luồng hệ điều hành (Thread)", "Coroutine (Hàm đồng quy)"]
    t12_r = [
        ["Không gian địa chỉ", "Cô lập hoàn toàn (Private VAS)", "Chung Heap, riêng Call Stack", "Chung không gian bộ nhớ của Luồng"],
        ["Chi phí bộ nhớ RAM", "Rất nặng (~15 – 30 MB / tiến trình)", "Trung bình (~8 MB stack ảo OS)", "Siêu nhẹ (~1 – 2 KB / coroutine)"],
        ["Thời gian Context Switch", "Rất nặng (5 – 15 µs, flush TLB)", "Trung bình (1 – 3 µs tại OS Kernel)", "Cực nhẹ (20 – 50 ns ở User-space)"],
        ["Cơ chế Lập lịch", "Preemptive (Kernel OS ngắt timer)", "Preemptive (Kernel OS ngắt timer)", "Cooperative (Nhường quyền tại await)"],
        ["Giới hạn CPython GIL", "VƯỢT QUA GIL (Mỗi tiến trình 1 core)", "BỊ KHÓA BỞI GIL (Không chạy đa nhân CPU)", "Chạy trên 1 core (Single loop thread)"],
        ["Kịch bản tối ưu nhất", "Tính toán số học nặng thuần Python", "I/O khi phải dùng thư viện blocking", "I/O mạng quy mô lớn (C10K / C100K)"]
    ]
    add_table_box(s12, t12_h, t12_r, Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0), col_widths=[140, 195, 195, 205])

    add_speaker_notes(s12,
        "Bảng số liệu này giải thích vì sao asyncio là vua của các ứng dụng mạng I/O: 100.000 coroutines chỉ ngốn khoảng 150 MB RAM, trong khi 100.000 threads sẽ đánh sập máy chủ ngay lập tức do cạn kiệt bộ nhớ ảo.",
        "Vậy khi đối mặt với một bài toán thực tế, làm sao chúng ta nhận biết bài toán đó thuộc loại Workload nào để chọn đúng công cụ?")

    # =========================================================================
    # SLIDE 13: PHÂN LOẠI WORKLOAD: I/O-BOUND, CPU-BOUND VÀ WORKLOAD HỖN HỢP
    # =========================================================================
    s13 = create_slide_base(prs, 13, "PHÂN LOẠI BÀI TOÁN", "I/O-bound vs CPU-bound vs Mixed Workload")
    add_content_title(s13, "Nhận diện triệu chứng nút thắt trước khi lựa chọn công cụ kỹ thuật")
    add_bullets(s13, [
        ("Nghẽn Nhập/Xuất (I/O-bound)", "Thời gian chủ yếu mất vào chờ mạng, đĩa, cơ sở dữ liệu. Triệu chứng: CPU utilization < 15%, Wall time rất dài, đèn mạng/đĩa nhấp nháy liên tục. Phép đo: CPU Time << Wall Time. Ứng viên: `asyncio` hoặc `ThreadPoolExecutor`."),
        ("Nghẽn Tính toán (CPU-bound)", "Thời gian chủ yếu mất vào tính ma trận số học, mã hóa, giải nén. Triệu chứng: CPU utilization 100% trên các core, quạt tản nhiệt quay tối đa. Phép đo: CPU Time ≈ Wall Time. Ứng viên: `ProcessPoolExecutor` (vượt GIL CPython)."),
        ("Workload Hỗn hợp (Mixed Workload)", "Hệ thống vừa đọc mạng cảm biến (I/O), vừa tính toán chỉ số AQI (CPU), vừa lưu dữ liệu cảnh báo vào DB (I/O).")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))
    s13.shapes.add_picture(os.path.join(IMG_DIR, "diag_s5_workload_taxonomy.png"), Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0))

    add_speaker_notes(s13,
        "Các em hãy lưu ý từ 'Ứng viên'. Không có một công thức tuyệt đối nào cả. Ví dụ: Với các thư viện tính toán viết bằng mã C như NumPy, OpenCV hay TensorFlow, chúng tự động nhả khóa GIL bên trong mã C, nên lúc đó ThreadPool vẫn có thể chạy tính toán song song đa nhân mà không cần dùng đến ProcessPool!",
        "Làm thế nào để hệ thống của chúng ta đạt hiệu năng cao nhất khi đối mặt với bài toán hỗn hợp? Hãy cùng tìm hiểu Mô hình Kiến trúc Lai!")

    # =========================================================================
    # SLIDE 14: CÂY QUYẾT ĐỊNH CÔNG NGHỆ & MÔ HÌNH KIẾN TRÚC LAI (HYBRID)
    # =========================================================================
    s14 = create_slide_base(prs, 14, "KIẾN TRÚC LAI", "Cây Quyết định Công nghệ & Mô hình Kiến trúc Lai (Hybrid)")
    add_content_title(s14, "Chiến lược phân luồng: Asyncio tiếp nhận I/O + ProcessPool xử lý CPU")
    add_bullets(s14, [
        ("Cây quyết định lựa chọn công cụ", "Chờ mạng/đĩa? ➔ Có thư viện async native (aiohttp, asyncpg)? ➔ Chọn `asyncio`. Thư viện cũ blocking? ➔ Chọn `ThreadPoolExecutor`. Tính toán nặng thuần Python? ➔ Chọn `ProcessPoolExecutor`."),
        ("Nguyên lý Kiến trúc Lai (Hybrid Architecture)", "Sử dụng Asyncio Event Loop ở tầng ngoài cùng để tiếp nhận hàng chục nghìn kết nối cảm biến I/O non-blocking; khi cần tính toán AQI nặng, offload tác vụ sang ProcessPool thông qua `loop.run_in_executor()`."),
        ("Cơ chế chống tràn tải (Backpressure Queue)", "Sử dụng `asyncio.Queue(maxsize=N)` để ngăn chặn việc hàng triệu gói tin mạng tràn vào làm quá tải và nghẽn bộ nhớ của ProcessPool worker.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(11.5))

    add_styled_card(s14, "QUY TRÌNH KIẾN TRÚC LAI CHUẨN CÔNG NGHIỆP TRONG PYTHON", [
        ("Tầng tiếp nhận I/O (Asyncio Loop)", "async def handle_stream(): data = await read_station_packet() # Non-blocking"),
        ("Tầng xử lý nặng (ProcessPool Worker)", "aqi_metric = await loop.run_in_executor(cpu_pool, heavy_aqi_calc, data)"),
        ("Tầng lưu trữ & Cảnh báo (Asyncio DB)", "await async_db.insert(aqi_metric) # Hoàn tất pipeline không gây nghẽn bất kỳ tầng nào")
    ], Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), bg_col=COLOR_CARD_BG, border_col=COLOR_BLUE)

    add_speaker_notes(s14,
        "Đây chính là kiến trúc thực chiến mà các framework lớn hiện nay như FastAPI, Celery hay các hệ thống microservice xử lý dữ liệu lớn áp dụng: Chia để trị, I/O giao cho cơ chế hướng sự kiện, tính toán giao cho worker pool chuyên dụng.",
        "Nhưng làm sao chúng ta chứng minh được một giải pháp mới thực sự chạy nhanh hơn giải pháp cũ? Hãy đến với phương pháp luận đo lường hiệu năng!")

    # =========================================================================
    # SLIDE 15: PHƯƠNG PHÁP LUẬN ĐO LƯỜNG: TRIẾT LÝ "CORRECTNESS FIRST"
    # =========================================================================
    s15 = create_slide_base(prs, 15, "ĐO LƯỜNG HIỆU NĂNG", "Phương pháp luận Đo lường & Triết lý 'Correctness First'")
    add_content_title(s15, "Nguyên tắc sống còn: Đúng trước, Nhanh sau & Bốn chỉ số hiệu năng chuẩn")
    add_bullets(s15, [
        ("Triết lý 'Correctness First'", "Một chương trình chạy nhanh gấp 10 lần nhưng tính sai chỉ số AQI hoặc làm mất mát 20% dữ liệu cảm biến là HOÀN TOÀN VÔ GIÁ TRỊ! Tính đúng đắn luôn là điều kiện tiên quyết."),
        ("Bộ 4 chỉ số hiệu năng chuẩn mực", "1) Latency (Độ trễ - ms) | 2) Throughput (Thông lượng - req/s) | 3) Hệ số tăng tốc Speedup: S(N) = T_seq / T_par(N) | 4) Hiệu suất tài nguyên: Efficiency E(N) = S(N) / N."),
        ("Sequential Oracle (Mốc chuẩn chân lý)", "Bản tuần tự chuẩn mực là thước đo kiểm chứng. Mọi chế độ tối ưu (Thread, Process, Async) bắt buộc phải đối soát trùng khớp 100% mã băm `Result Digest SHA-256`.")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(11.5))

    t15_h = ["Chế độ thực thi (Mode)", "Đơn vị thực thi", "Wall Time (s)", "Speedup S(N)", "Efficiency E(N)", "Đối soát SHA-256 Digest"]
    t15_r = [
        ["1. Sequential Baseline", "1 Core (Tuần tự)", "[T_seq = 1.20s]", "1.00 x (Gốc)", "100.0% (Mốc)", "CHÂN LÝ ĐỐI SOÁT (ORACLE)"],
        ["2. ThreadPoolExecutor", "Worker Threads", "[TV2 đo đạc]", "[S_thread]", "[E_thread]", "Phải khớp 100% SHA-256"],
        ["3. ProcessPoolExecutor", "Worker Processes", "[TV3 đo đạc]", "[S_process]", "[E_process]", "Phải khớp 100% SHA-256"],
        ["4. Asyncio Event Loop", "Coroutines đơn luồng", "[TV4 đo đạc]", "[S_async]", "[E_async]", "Phải khớp 100% SHA-256"],
        ["5. Hybrid Architecture", "Asyncio + ProcessPool", "[TV6 đo đạc]", "[S_hybrid]", "[E_hybrid]", "Phải khớp 100% SHA-256"]
    ]
    add_table_box(s15, t15_h, t15_r, Pt(28.34), Pt(335.0), Pt(735.0), Pt(180.0), col_widths=[140, 130, 100, 95, 120, 150])

    add_speaker_notes(s15,
        "Thầy/cô muốn nhấn mạnh: Đừng bao giờ vội vàng khoe con số tăng tốc 5x hay 10x nếu các em chưa kiểm tra xem kết quả đầu ra có trùng khớp với bản tuần tự ban đầu hay không. Kết quả sai mà chạy nhanh thì chỉ làm hỏng hệ thống nhanh hơn mà thôi.",
        "Để đảm bảo các con số đo được không bị nhiễu loạn bởi môi trường, chúng ta cần tuân thủ giao thức Benchmark nào?")

    # =========================================================================
    # SLIDE 16: GIAO THỨC BENCHMARK KHOA HỌC & NĂM LOẠI CHI PHÍ OVERHEAD THỰC TẾ
    # =========================================================================
    s16 = create_slide_base(prs, 16, "KIỂM CHUẨN KHOA HỌC", "Giao thức Benchmark Công bằng & 5 Loại Chi phí Overhead")
    add_content_title(s16, "Loại bỏ sai số đo lường và nhận diện các chi phí ngầm của hệ thống")
    add_bullets(s16, [
        ("Bốn quy chuẩn Benchmark công bằng", "1) Dùng đồng hồ đo đơn điệu `time.perf_counter_ns()`; 2) Giai đoạn Warm-up nạp sẵn cache bộ nhớ; 3) Đo lặp lại $\ge$ 5 lần và lấy Trung vị (Median); 4) Tuyệt đối cách ly Console (không gọi `print()` trong vùng bấm giờ)."),
        ("Năm loại chi phí Overhead thực tế", "Lý do khiến hiệu suất thực tế luôn nhỏ hơn 1.0 (E < 1.0):")
    ], top=Pt(150.0), height=Pt(115.0), font_size=Pt(11.5))

    add_styled_card(s16, "DANH MỤC 5 LOẠI CHI PHÍ OVERHEAD LÀM SUY GIẢM TỐC ĐỘ THỰC TẾ", [
        ("1. Chi phí Khởi tạo Worker (Spawn Overhead)", "Tạo mới Thread mất ~100µs; tạo Process mất ~20-50ms (nạp lại interpreter và import thư viện)."),
        ("2. Chi phí Lập lịch & Ngữ cảnh (Context Switch)", "Kernel OS tiêu tốn chu kỳ CPU để lưu và phục hồi thanh ghi khi chuyển đổi giữa hàng trăm luồng."),
        ("3. Chi phí Tuần tự hóa IPC (Pickle Serialization)", "Dữ liệu truyền giữa các tiến trình qua ProcessPool phải serialize và deserialize sang nhị phân."),
        ("4. Chi phí Tranh chấp Hàng đợi (Queue Contention)", "Nhiều worker cùng tranh nhau lấy dữ liệu từ hàng đợi chung gây nghẽn tại memory bus."),
        ("5. Chi phí Khóa & Tranh chấp Bộ nhớ (Lock Contention)", "Các luồng phải xếp hàng chờ giải phóng Lock làm triệt tiêu khả năng chạy song song.")
    ], Pt(28.34), Pt(275.0), Pt(735.0), Pt(245.0), bg_col=COLOR_CARD_BG, border_col=COLOR_DARK_RED)

    add_speaker_notes(s16,
        "Một sai lầm rất ngây thơ là nghĩ rằng: 'Tôi có 1 tác vụ mất 1 giây, tôi chia nhỏ ra 1.000 phần cho 1.000 luồng chạy thì sẽ mất 1 mili-giây'. Thực tế chi phí khởi tạo và tranh chấp của 1.000 luồng đó sẽ mất tới vài giây, khiến chương trình chậm hơn gấp nhiều lần so với chạy tuần tự đơn giản!",
        "Nếu chúng ta có vô hạn worker thì chương trình có chạy nhanh vô hạn được không? Hãy cùng đến với Định luật Amdahl!")

    # =========================================================================
    # SLIDE 17: ĐỊNH LUẬT AMDAHL & BỨC TƯỜNG GIỚI HẠN TĂNG TỐC
    # =========================================================================
    s17 = create_slide_base(prs, 17, "GIỚI HẠN TĂNG TỐC", "Định luật Amdahl & Hiện tượng Bão hòa Tăng tốc")
    add_content_title(s17, "Trần giới hạn toán học bất biến và hiện tượng quá tải worker (Oversubscription)")
    add_bullets(s17, [
        ("Phát biểu Định luật Amdahl (1967)", "Hệ số tăng tốc Speedup bị chặn bởi tỷ lệ phần trăm công việc bắt buộc phải chạy tuần tự: S(N) = 1 / [ (1 - p) + p/N ]. Khi số worker tiến tới vô cùng (N ➔ ∞), trần tốc độ là: S_max = 1 / (1 - p)."),
        ("Minh họa trần tốc độ bài toán", "Nếu hệ thống có 20% thời lượng tuần tự (s = 1 - p = 0.20): Dù trang bị 1 TRIỆU CORE CPU, hệ số tăng tốc TỐI ĐA KHÔNG BAO GIỜ VƯỢT QUÁ 5.0 LẦN!"),
        ("Hiện tượng Oversubscription trong thực tế", "Vượt quá ngưỡng core CPU vật lý, chi phí Context Switch và tranh chấp tăng vọt khiến đường cong hiệu năng bị uốn cong suy thoái đi xuống!")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))
    s17.shapes.add_picture(os.path.join(IMG_DIR, "diag_s7_amdahl_visual.png"), Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0))

    add_speaker_notes(s17,
        "Nhìn vào đồ thị bên phải: Đường cong màu đỏ biểu thị thực tế có overhead. Khi các em tăng số worker từ 1 lên 4, tốc độ tăng rất đẹp. Nhưng khi tăng từ 16 lên 32 worker trên một máy chỉ có 8 nhân, tốc độ bắt đầu rơi tự do! Đó là bài học xương máu: 'Càng nhiều worker càng nhanh' là một ngộ nhận chết người.",
        "Những ngộ nhận phổ biến nào khác mà các kỹ sư phần mềm thường mắc phải?")

    # =========================================================================
    # SLIDE 18: BẢNG PHÁ VỠ BỐN NGỘ NHẬN KỸ THUẬT KINH ĐIỂN (MYTH VS FACT)
    # =========================================================================
    s18 = create_slide_base(prs, 18, "PHÁ VỠ NGỘ NHẬN", "Bốn Ngộ nhận Kinh điển trong Kỹ thuật Tính toán")
    add_content_title(s18, "Đối chiếu giữa Ngộ nhận chủ quan và Sự thật kiến trúc tầng thấp")
    add_bullets(s18, [
        ("Mục tiêu sư phạm", "Giúp sinh viên thoát khỏi những cái bẫy tư duy trực giác sai lầm khi tiếp cận lập trình đồng thời và bất đồng bộ."),
        ("Nguyên tắc tư duy kỹ sư", "Hiệu năng luôn phụ thuộc vào bản chất Workload và đặc tính phần cứng, không bao giờ có công cụ toàn năng trong mọi tình huống.")
    ], top=Pt(150.0), height=Pt(80.0), font_size=Pt(11.5))

    t18_h = ["Ngộ nhận Thường gặp (Myth)", "Sự thật Kỹ thuật (Technical Fact)", "Giải thích Bản chất Hệ thống"]
    t18_r = [
        ["'Async luôn nhanh hơn Tuần tự'", "HOÀN TOÀN SAI trong nhiều trường hợp!", "Với bài toán CPU-bound hoặc chỉ có 1 task đơn lẻ, chi phí dựng Event Loop và quản lý Task làm async chậm hơn tuần tự!"],
        ["'Càng nhiều Worker càng nhanh'", "HOÀN TOÀN SAI khi vượt quá số core!", "Gây hiện tượng Oversubscription; hàng trăm luồng tranh giành CPU làm nghẽn Context Switch và bão hòa RAM bus."],
        ["'Async 1 thread không có Race Condition'", "HOÀN TOÀN SAI ở tầng logic ứng dụng!", "Dù an toàn ở mức thanh ghi bộ nhớ (do 1 thread), Race Condition vẫn xảy ra giữa các điểm `await` khi truy cập biến chung!"],
        ["'Async trên 1 máy là Hệ Phân tán'", "HOÀN TOÀN SAI về mặt kiến trúc!", "1 máy vẫn chung RAM vật lý, chung 1 OS Kernel; Hệ phân tán không chung RAM, chịu lỗi trễ mạng và Clock Skew."]
    ]
    add_table_box(s18, t18_h, t18_r, Pt(28.34), Pt(240.0), Pt(735.0), Pt(275.0), col_widths=[175, 230, 330])

    add_speaker_notes(s18,
        "Đặc biệt lưu ý Ngộ nhận 3: Rất nhiều bạn sinh viên nghĩ rằng asyncio chạy 1 luồng thì không bao giờ bị Race Condition. Hoàn toàn sai! Nếu hai coroutine cùng rút tiền từ một tài khoản ngân hàng, coroutine 1 đọc số dư xong rồi gặp lệnh await (bị tạm dừng), coroutine 2 chen vào rút tiền, khi coroutine 1 quay lại số dư đã bị sai lệch hoàn toàn. Đó chính là Race Condition tầng ứng dụng.",
        "Làm thế nào để xây dựng một bộ dữ liệu chuẩn mực để toàn bộ lớp cùng thực nghiệm kiểm chứng? Hãy đến với Slide 19: Thực nghiệm mẫu!")

    # =========================================================================
    # SLIDE 19: THỰC NGHIỆM MẪU: BÀI TOÁN CẢM BIẾN & SEQUENTIAL ORACLE
    # =========================================================================
    s19 = create_slide_base(prs, 19, "THỰC NGHIỆM MẪU", "Thực nghiệm Mẫu & Sequential Baseline Oracle")
    add_content_title(s19, "Thiết lập mốc chân lý bất biến cho bài toán quan trắc trạm cảm biến")
    add_bullets(s19, [
        ("Thiết kế Data Contract chặt chẽ", "Bản ghi `SensorReading` chuẩn hóa cấu trúc: `station_id` (str), `timestamp` (ISO), `temperature` (°C), `humidity` (%), `aqi` (int), `status` (VALID/ERROR), `delay` (float)."),
        ("Bộ sinh xác định (Seed=42)", "Cố định `random.seed(42)` để mọi sinh viên chạy ở bất kỳ máy tính nào đều nhận chính xác cùng một bộ dữ liệu 8 trạm."),
        ("Tiêm lỗi chủ đích (Fault Injection)", "Trạm STA-004 được cố tình tiêm lỗi mạng `ERROR` nhằm kiểm thử năng lực bắt lỗi ngoại lệ của hệ thống."),
        ("Mã băm mốc bất biến SHA-256 Digest", "Kết quả đầu ra được khóa bằng mã SHA-256 Digest: `e8b4c91a...`. Mọi chế độ tối ưu hóa sau này bắt buộc phải cho ra mã băm trùng khớp 100%!")
    ], top=Pt(150.0), height=Pt(165.0), font_size=Pt(11.5))

    add_styled_card(s19, "BỘ DỮ LIỆU ĐỐI SOÁT CHUẨN MỰC CỦA BÀI HỌC", [
        ("Cấu hình kiểm thử", "8 trạm quan trắc môi trường Cần Thơ (STA-001 đến STA-008). Seed = 42."),
        ("Thời gian đo chuẩn (T_seq)", "1.1524 giây (Khớp hoàn toàn với tổng độ trễ mạng trạm và thời gian tính toán)."),
        ("Kết quả phân loại", "7 trạm VALID | 1 trạm lỗi phát hiện chính xác tuyệt đối (STA-004: ERROR)."),
        ("Result Digest SHA-256", "e8b4c91a7f340cd8... (CHÂN LÝ ĐỐI SOÁT DUY NHẤT CỦA CẢ NHÓM)")
    ], Pt(28.34), Pt(325.0), Pt(735.0), Pt(190.0), bg_col=COLOR_CARD_BG, border_col=COLOR_GREEN)

    add_speaker_notes(s19,
        "Với bản kết quả thực nghiệm mẫu này, chúng ta đã có một 'thước đo chân lý'. Từ bài sau, khi học sang ThreadPool hay Asyncio, nếu bạn nào nộp bài báo cáo chạy rất nhanh nhưng mã băm SHA-256 không khớp với giá trị này thì bài nộp đó bị tính là sai kết quả.",
        "Từ nền móng lý thuyết này, toàn bộ chương 4 của chúng ta sẽ được triển khai theo lộ trình nào?")

    # =========================================================================
    # SLIDE 20: BẢN ĐỒ KIẾN TRÚC TOÀN CHƯƠNG: TỪ NỀN TẢNG ĐẾN THỰC THI
    # =========================================================================
    s20 = create_slide_base(prs, 20, "LỘ TRÌNH CHƯƠNG 4", "Bản đồ Kiến trúc Toàn chương: Mạch nối từ TV1 đến TV6")
    add_content_title(s20, "Cầu nối logic xuyên suốt: Giải quyết triệt để từng điểm nghẽn hệ thống")
    add_bullets(s20, [
        ("Bài 1 (Nền tảng & Oracle - TV1)", "Nhận diện lãng phí I/O, taxonomy 7 khái niệm, phân loại workload, Amdahl và dựng Sequential Oracle."),
        ("Bài 2 (ThreadPoolExecutor - TV2)", "Giải quyết câu hỏi: 'Làm sao bọc các thao tác blocking I/O trong worker pool mà không phải tự quản lý luồng?'"),
        ("Bài 3 (ProcessPoolExecutor & GIL - TV3)", "Giải quyết câu hỏi: 'Tại sao ThreadPool không tăng tốc CPU trong Python và cách vượt qua GIL bằng ProcessPool?'"),
        ("Bài 4 (Asyncio Runtime & Event Loop - TV4)", "Giải quyết câu hỏi: 'Làm sao 1 luồng đơn lẻ điều phối hàng chục vạn coroutine nhường quyền hợp tác?'"),
        ("Bài 5 & 6 (Độ tin cậy & Kiến trúc Lai - TV5 / TV6)", "Chống sập hệ thống bằng Timeout/Cancellation/Backpressure và hoàn thiện Kiến trúc Lai tối ưu.")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))
    s20.shapes.add_picture(os.path.join(IMG_DIR, "diag_s8_baseline_pipeline.png"), Pt(28.34), Pt(305.0), Pt(735.0), Pt(215.0))

    add_speaker_notes(s20,
        "Các em thấy đấy: Toàn bộ chương 4 là một câu chuyện liền mạch. Mỗi bài giảng giải quyết đúng một nút thắt của bài giảng trước để đưa chúng ta từ một chương trình chạy chậm 1.2s đến một hệ thống xử lý hàng trăm nghìn trạm cảm biến trong chớp mắt.",
        "Để tiện cho việc ôn tập và tra cứu, bài giảng có 3 phần phụ lục chuyên sâu: P01, P02 và P03!")

    # =========================================================================
    # SLIDE 21: PHỤ LỤC P01 — MA TRẬN TRA CỨU THUẬT NGỮ CHUYÊN SÂU
    # =========================================================================
    s21 = create_slide_base(prs, 21, "PHỤ LỤC TRA CỨU", "Phụ lục P01: Ma trận Tra cứu Thuật ngữ Chuyên sâu A-Z", "PHỤ LỤC BÀI GIẢNG")
    add_content_title(s21, "Sổ tay tra cứu 7 khái niệm cốt lõi, góc nhìn kiến trúc và ví dụ thực tế")
    p01_headers = ["Thuật ngữ", "Góc nhìn kiến trúc", "Định nghĩa cốt lõi", "Ví dụ chuẩn mực", "Phản ví dụ / Sai lầm"]
    p01_rows = [
        ["Tuần tự (Sequential)", "Trục thời gian", "Các tác vụ chạy nối tiếp nhau lần lượt", "Vòng lặp for gọi trạm lần lượt", "Tưởng nhầm là không thể tối ưu"],
        ["Đồng thời (Concurrent)", "Tiến triển (Progress)", "Nhiều việc cùng tiến triển xen kẽ nhau", "asyncio.create_task() trên 1 core", "Nhầm là phải có đa nhân phần cứng"],
        ["Song song (Parallel)", "Thực thi vật lý", "Nhiều việc chạy tại cùng thời điểm t0", "ProcessPool trên CPU 8 cores", "Dùng ThreadPool thuần Python để tính toán"],
        ["Đồng bộ (Synchronous)", "Contract bên gọi", "Caller bị chặn đợi callee trả kết quả", "Hàm def thông thường gọi hàm", "Nhầm đồng bộ là luôn luôn chậm"],
        ["Bất đồng bộ (Async)", "Contract bên gọi", "Caller nhận handle/Future rồi đi tiếp", "async def trả về Coroutine object", "Tưởng async là tự động chạy đa luồng"],
        ["Blocking", "Trạng thái luồng OS", "Luồng bị OS đưa vào trạng thái ngủ", "time.sleep(1), socket.recv()", "Gọi hàm blocking bên trong async def!"],
        ["Non-blocking", "Trạng thái luồng OS", "System Call trả về ngay (EWOULDBLOCK)", "socket.setblocking(False), epoll", "Dùng vòng lặp while True hỏi dồn (Spinlock)"]
    ]
    add_table_box(s21, p01_headers, p01_rows, Pt(28.34), Pt(165.0), Pt(735.0), Pt(350.0), col_widths=[125, 120, 190, 150, 150])

    add_speaker_notes(s21,
        "Phụ lục P01 là bảng tra cứu nhanh khi làm bài tập hoặc phỏng vấn. Các em chỉ cần xác định rõ: Ta đang nói về Hợp đồng gọi hàm hay nói về Trạng thái của luồng hệ điều hành?",
        "Tiếp theo, chúng ta cùng xem chứng minh toán học của Định luật Amdahl trong Phụ lục P02!")

    # =========================================================================
    # SLIDE 22: PHỤ LỤC P02 — CHỨNG MINH TOÁN HỌC ĐỊNH LUẬT AMDAHL
    # =========================================================================
    s22 = create_slide_base(prs, 22, "PHỤ LỤC TOÁN HỌC", "Phụ lục P02: Chứng minh Toán học Định luật Amdahl & Bài toán Mẫu", "PHỤ LỤC BÀI GIẢNG")
    add_content_title(s22, "Phân tích giới hạn tiệm cận và Bài toán xử lý ảnh viễn thám môi trường")
    add_bullets(s22, [
        ("Công thức nguyên thủy", "Thời gian khi dùng N worker: T(N) = (1 - p)*T(1) + (p / N)*T(1).  Hệ số tăng tốc Speedup: S(N) = T(1) / T(N) = 1 / [ (1 - p) + p/N ]."),
        ("Chứng minh trần tiệm cận", "Khi N tiến tới vô cùng: lim(N->∞) (p / N) = 0. Do đó: S_max = 1 / (1 - p) = 1 / s (với s là tỷ lệ bắt buộc tuần tự)."),
        ("Bài toán thực tế viễn thám", "Xử lý ảnh viễn thám: 20% nạp ảnh tuần tự (s = 0.20), 80% tính toán pixel (p = 0.80). Trần tốc độ S_max = 1 / 0.20 = 5.0 lần!")
    ], top=Pt(150.0), height=Pt(145.0), font_size=Pt(11.5))

    p02_headers = ["Số Worker (N)", "Công thức tính S(N)", "Hệ số Tăng tốc S(N)", "Hiệu suất tài nguyên E(N)", "Ý nghĩa Kỹ thuật"]
    p02_rows = [
        ["N = 1 worker", "1 / (0.20 + 0.80 / 1)", "1.00 x", "100.0%", "Mốc chuẩn tuần tự (Baseline)"],
        ["N = 2 workers", "1 / (0.20 + 0.80 / 2)", "1.67 x", "83.5%", "Tăng tốc tốt, hiệu suất cao"],
        ["N = 4 workers", "1 / (0.20 + 0.80 / 4)", "2.50 x", "62.5%", "Bắt đầu xuất hiện lãng phí tài nguyên"],
        ["N = 8 workers", "1 / (0.20 + 0.80 / 8)", "3.33 x", "41.6%", "Hiệu suất rớt xuống dưới 50%"],
        ["N = 16 workers", "1 / (0.20 + 0.80 / 16)", "4.00 x", "25.0%", "Thêm gấp đôi phần cứng nhưng tốc độ tăng rất ít"],
        ["N ➔ Vô cùng (∞)", "1 / (0.20 + 0)", "5.00 x (TRẦN TỐI ĐA)", "➔ 0.0%", "Trần toán học bất biến, không thể vượt qua!"]
    ]
    add_table_box(s22, p02_headers, p02_rows, Pt(28.34), Pt(305.0), Pt(735.0), Pt(210.0), col_widths=[105, 155, 145, 145, 185])

    add_speaker_notes(s22,
        "Đây là một bài toán kinh tế phần mềm rất sâu sắc: Đổ tiền mua CPU 64 nhân hay 128 nhân không giúp hệ thống nhanh hơn nếu các em không tối ưu phần tuần tự 20%.",
        "Tiếp theo là Phụ lục P03: Bộ checklist 10 tiêu chí Benchmark bắt buộc!")

    # =========================================================================
    # SLIDE 23: PHỤ LỤC P03 — CHECKLIST 10 TIÊU CHÍ BENCHMARK KHOA HỌC
    # =========================================================================
    s23 = create_slide_base(prs, 23, "PHỤ LỤC KIỂM CHUẨN", "Phụ lục P03: Checklist 10 Tiêu chí Benchmark Khoa học", "PHỤ LỤC BÀI GIẢNG")
    add_content_title(s23, "Bảng kiểm 10 tiêu chuẩn bắt buộc cho mọi bài thực hành đo lường hiệu năng")
    p03_headers = ["STT", "Tiêu chí Kiểm chuẩn", "Quy định Bắt buộc trong Báo cáo", "Mục đích Kỹ thuật & Chống sai lệch"]
    p03_rows = [
        ["1", "Fixed Input & Seed", "Cố định 8 trạm, random.seed=42", "Đảm bảo tính tất định, cùng dữ liệu đầu vào"],
        ["2", "Correctness Oracle", "SHA-256 khớp 100% Sequential Baseline", "Chống việc chương trình chạy nhanh nhưng tính sai"],
        ["3", "Đồng hồ chuẩn xác", "Chỉ dùng time.perf_counter_ns()", "Tránh trôi đồng hồ của time.time() do cập nhật NTP"],
        ["4", "Warm-up Phase", "Chạy khởi động tối thiểu 1 lần", "Nạp sẵn cache bộ nhớ và bytecode JIT"],
        ["5", "Số lần lặp lại", "Lặp tối thiểu 5 đến 10 lần chạy độc lập", "Thu thập mẫu thống kê có ý nghĩa"],
        ["6", "Thống kê Trung vị", "Báo cáo bằng Median và dải min/max", "Loại trừ đột biến ngẫu nhiên từ tiến trình nền của OS"],
        ["7", "Console Isolation", "Không print() / ghi log trong vùng đo", "I/O console rất chậm và gây sai lệch đo lường"],
        ["8", "Cấu hình phần cứng", "Ghi rõ CPU model, số core, RAM, OS, Python", "Đảm bảo khả năng tái lập thí nghiệm (Reproducibility)"]
    ]
    add_table_box(s23, p03_headers, p03_rows, Pt(28.34), Pt(165.0), Pt(735.0), Pt(350.0), col_widths=[35, 170, 260, 270])

    add_speaker_notes(s23,
        "Checklist này là tiêu chuẩn đánh giá chấm điểm đồ án: Báo cáo nào thiếu kiểm tra SHA-256 Digest hoặc dùng time.time() để đo thời gian sẽ bị trừ điểm phương pháp luận.",
        "Cuối cùng, chúng ta hãy cùng thảo luận 10 câu hỏi cốt lõi để khắc sâu kiến thức buổi học hôm nay!")

    # =========================================================================
    # SLIDE 24: THẢO LUẬN & 10 CÂU HỎI PHẢN BIỆN CỐT LÕI (KẾT THÚC BÀI GIẢNG)
    # =========================================================================
    s24 = create_slide_base(prs, 24, "TỔNG KẾT & THẢO LUẬN", "Tổng kết Ba Thông điệp & 10 Câu hỏi Thảo luận", "KẾT THÚC BÀI HỌC")
    add_content_title(s24, "Ba thông điệp cốt tử và Bộ câu hỏi gợi mở thảo luận trên lớp")

    add_styled_card(s24, "BA THÔNG ĐIỆP KỸ THUẬT CỐT TỬ CỦA BÀI HỌC", [
        ("Thông điệp 1: Nắm đúng bản chất", "Phân biệt rạch ròi Concurrency (cấu trúc xen kẽ), Parallelism (đa nhân vật lý), và Asynchrony (hợp đồng không chờ). Tuyệt đối không gọi blocking trong luồng async!"),
        ("Thông điệp 2: Nút thắt quyết định công cụ", "I/O-bound chọn Asyncio / ThreadPool; CPU-bound chọn ProcessPool để vượt qua GIL. Hệ thống thực tế dùng Kiến trúc Lai (Hybrid)."),
        ("Thông điệp 3: Đúng trước, Nhanh sau", "Mọi tối ưu hóa đều vô nghĩa nếu kết quả sai lệch. Tăng tốc luôn có trần giới hạn bởi Định luật Amdahl và các loại chi phí overhead thực tế.")
    ], Pt(28.34), Pt(155.0), Pt(735.0), Pt(155.0), bg_col=COLOR_CARD_BG, border_col=COLOR_BLUE)

    t24_q_cards = [
        ("GỢI MỞ THẢO LUẬN 1 (BẢN CHẤT KIẾN TRÚC)", [
            ("Q1", "Một chương trình 1 thread đơn lẻ có concurrent được không? (Trả lời: Có, nhờ Event Loop và Cooperative Yield)"),
            ("Q2", "Lệnh await có làm block luồng OS không? (Trả lời: Không, chỉ tạm dừng coroutine và nhường quyền)"),
            ("Q3", "Async trên 1 máy tính có phải là hệ phân tán không? (Trả lời: Không, vẫn chung RAM vật lý và 1 Kernel)")
        ]),
        ("GỢI MỞ THẢO LUẬN 2 (HIỆU NĂNG & BENCHMARK)", [
            ("Q4", "Vì sao thêm worker có thể làm chậm chương trình? (Trả lời: Do hiện tượng Oversubscription và Context Switch)"),
            ("Q5", "Định luật Amdahl bỏ qua những loại overhead nào? (Trả lời: Bỏ qua chi phí tạo worker, IPC và lock contention)"),
            ("Chuyển tiếp", "Chuẩn bị cho Bài học tiếp theo: 'Chuyên đề 2: ThreadPoolExecutor và Quản lý Worker Pool'!")
        ])
    ]

    add_styled_card(s24, t24_q_cards[0][0], t24_q_cards[0][1], Pt(28.34), Pt(325.0), Pt(355.0), Pt(190.0), bg_col=COLOR_CARD_BG, border_col=COLOR_GREEN)
    add_styled_card(s24, t24_q_cards[1][0], t24_q_cards[1][1], Pt(408.0), Pt(325.0), Pt(355.0), Pt(190.0), bg_col=COLOR_CARD_BG, border_col=COLOR_ORANGE)

    add_speaker_notes(s24,
        "Bài giảng Chuyên đề 1 hôm nay xin kết thúc tại đây. Cảm ơn sự chú ý lắng nghe và thảo luận sôi nổi của các em. Về nhà các em hãy xem lại bảng ma trận P01 và chạy thử mã nguồn sensor_baseline.py để kiểm chứng mã băm SHA-256 Digest trước khi chúng ta bước sang Chuyên đề 2 về ThreadPoolExecutor vào tuần sau!",
        "Xin chào và hẹn gặp lại các em ở Bài giảng Chuyên đề 2!")

    # Lưu file
    out_file = "TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx"
    prs.save(out_file)
    print(f"XUẤT BẢN THÀNH CÔNG BỘ BÀI GIẢNG ĐẠI HỌC 24 SLIDE: {out_file} (Dung lượng: {os.path.getsize(out_file):,} bytes)")

    try:
        prs.save("TV1_BaiGiang_TinhToanSongSong_PhanTan_C4.pptx")
        print("ĐÃ CẬP NHẬT ĐÈ VÀO: TV1_BaiGiang_TinhToanSongSong_PhanTan_C4.pptx")
    except PermissionError:
        print("LƯU Ý: TV1_BaiGiang_TinhToanSongSong_PhanTan_C4.pptx đang mở trong PowerPoint, bản bài giảng chính thức lưu tại TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx")

def main():
    prs = Presentation()
    prs.slide_width = Pt(793.8)
    prs.slide_height = Pt(595.2)
    build_all_24_lecture_slides(prs)

if __name__ == "__main__":
    main()
