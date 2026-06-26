import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
# --- HÀM TỰ ĐỘNG HÓA (MÔ PHỎNG BACKEND LOGIC) ---
def auto_assign_task(task_name, priority_level):
    """
    Hàm này giả lập logic tự động gán việc.
    Trong thực tế, bạn có thể gọi API của AWS Lambda/Azure Function ở đây.
    """
    new_task = {
        "🚩 Quan trọng": True if priority_level == "High" else False,
        "📌 Tên công việc": task_name,
        "🏷️ Nhãn": "Hàng Nhập",
        "⏳ Trạng thái": "Chưa làm",
        "📅 Deadline": date.today(),
        "💬 Trao đổi / Ghi chú": "Tự động tạo bởi hệ thống"
    }
    # Thêm vào session_state để cập nhật bảng
    st.session_state.tasks_df = pd.concat([st.session_state.tasks_df, pd.DataFrame([new_task])], ignore_index=True)
# --- CẤU HÌNH ---
SENDER_EMAIL = "luongthaonhu22@gmail.com" 
APP_PASSWORD = "yjny odng vbgd czck"    

st.set_page_config(page_title="ELOGS Quản Trị", page_icon="🚢", layout="wide")

# --- NHÚNG MÃ CSS NÂNG CẤP (PHONG CÁCH SaaS HIỆN ĐẠI) ---
st.markdown("""
<style>
/* Bo tròn các khung thông tin */
    .stApp { background-color: #f5f7f9; }
    div.stButton > button { border-radius: 8px; border: 1px solid #ddd; }
    
    /* Làm nổi bật vùng Dashboard */
    .stDataFrame { border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    
    /* Font chữ hiện đại */
    body { font-family: 'Segoe UI', sans-serif; }
    /* 1. Đổi Font chữ sang loại hiện đại (Inter, Roboto hoặc Sans-serif) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* 2. Làm thẻ Tab bo tròn và gọn gàng */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        background-color: #f1f3f6;
        padding: 10px 20px;
    }
    
    /* 3. Bo tròn góc các ô nhập liệu và bảng biểu */
    input, textarea, div[data-testid="stDataFrame"] {
        border-radius: 12px !important;
        border: 1px solid #d1d9e6 !important;
    }
    
    /* 4. Nút bấm phẳng, bo tròn, màu xanh chuẩn SaaS */
    div.stButton > button {
        background-color: #2563eb !important; /* Xanh dương đậm chuẩn SaaS */
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    
    /* 5. Giao diện nền trắng sáng sạch sẽ */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* 6. Tạo đổ bóng nhẹ cho các khối nội dung (Cards) */
    .stColumn {
        background-color: #ffffff;
        border: 1px solid #f0f0f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)
# --- KHỞI TẠO BỘ NHỚ DATA (BẢNG CÔNG VIỆC) ---
if 'tasks_df' not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame({
        "🚩 Quan trọng": [True, False],
        "📌 Tên công việc": ["Khai E-port lô BKG-123", "Gửi SI hãng tàu Evergreen"],
        "🏷️ Nhãn": ["Hàng Nhập", "Chứng Từ"],
        "⏳ Trạng thái": ["Đang làm", "Chưa làm"],
        "📅 Deadline": [date.today(), date.today()],
        "💬 Trao đổi / Ghi chú": ["Sếp dặn check kỹ số cont", ""]
    })

st.title("🚢 HỆ THỐNG QUẢN LÝ LOGISTICS - ELOGS")
tab1, tab2 = st.tabs(["📧 PRE-ALERT (GỬI MAIL)", "📊 QUẢN TRỊ CÔNG VIỆC (DASHBOARD)"])

# ==========================================
# TAB 1: GỬI MAIL (GIỮ NGUYÊN BẢN CHUẨN)
# ==========================================
# --- BÊN TRONG TAB 1: PRE-ALERT & QUÉT MÃ ---
with tab1:
    st.subheader("📸 Quét mã QR/Barcode")
    # Giả lập quét mã vạch: khi quét xong, dữ liệu tự điền vào ô
    scanned_data = st.text_input("Nhập mã QR (hoặc dùng súng quét mã vạch tại đây):", placeholder="Quét mã tại đây...")
    
    if scanned_data:
        st.success(f"Đã nhận diện hàng hóa: {scanned_data}")
        # Tự động gợi ý thông tin dựa trên mã quét được
        st.info("Hệ thống đã nhận diện mã hàng, đang lấy dữ liệu từ Server...")
        
    st.markdown("---")
    # ... (giữ nguyên phần code gửi mail cũ của bạn ở dưới đây)
with tab1:
    receiver_email = st.text_input("Gửi đến (To - Bắt buộc):")
    cc_email = st.text_input("Đồng gửi (CC - Tùy chọn):")
    col1, col2, col3 = st.columns(3)
    booking_no = col1.text_input("Số Booking:", "BKG-VNM-998877")
    container_no = col2.text_input("Số Container:", "CMAU1234567")
    cut_off = col3.text_input("Cut-off:", "17:00 - 25/06/2026")
    
    if st.button("🚀 XÁC NHẬN GỬI THÔNG BÁO"):
        if not receiver_email:
            st.error("Vui lòng điền Email người nhận!")
        else:
            with st.spinner('Đang gửi mail...'):
                try:
                    msg = MIMEMultipart()
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = receiver_email
                    if cc_email: msg['Cc'] = cc_email
                    msg['Subject'] = f"[URGENT] Pre-alert Booking: {booking_no}"
                    msg.attach(MIMEText("Vui lòng hoàn tất thủ tục trước Cut-off.", 'html'))
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(SENDER_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    st.success("🎉 Gửi thành công!")
                except Exception as e:
                    st.error(f"Lỗi: {e}")

# ==========================================
# TAB 2: DASHBOARD QUẢN TRỊ CÔNG VIỆC
# ==========================================
with tab2:
    st.subheader("Bảng Kế hoạch & Theo dõi tiến độ")
with tab2:
    st.subheader("Bảng Kế hoạch & Theo dõi tiến độ")
    
    # --- THÊM PHẦN TỰ ĐỘNG HÓA ---
    if st.button("🤖 Kích hoạt tạo Task tự động (Mô phỏng hệ thống)"):
        auto_assign_task("Kiểm tra hàng tồn kho mới nhập", "High")
        st.success("Hệ thống đã tự động thêm task mới!")
        st.rerun() # Refresh lại trang để cập nhật bảng
    
    # ... (Phần code hiển thị metrics và data_editor cũ của bạn)
    
    # 1. BÁO CÁO NHANH (METRICS)
    df = st.session_state.tasks_df
    total_tasks = len(df)
    done_tasks = len(df[df["⏳ Trạng thái"] == "Hoàn thành"])
    important_tasks = len(df[df["🚩 Quan trọng"] == True])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tổng công việc", total_tasks)
    m2.metric("Đã hoàn thành", done_tasks)
    m3.metric("Cần chú ý (Quan trọng)", important_tasks, delta_color="inverse")
    if total_tasks > 0:
        m4.metric("Hiệu suất", f"{int((done_tasks/total_tasks)*100)}%")
    else:
        m4.metric("Hiệu suất", "0%")
        
    st.markdown("---")

    # 2. BẢNG TƯƠNG TÁC DỮ LIỆU (DATA EDITOR)
    # Tính năng này cho phép click đúp vào bảng để sửa trực tiếp như Excel
    edited_df = st.data_editor(
        st.session_state.tasks_df,
        use_container_width=True,
        num_rows="dynamic", # Cho phép ấn dấu + để thêm dòng mới
        column_config={
            "🚩 Quan trọng": st.column_config.CheckboxColumn("Quan trọng", default=False),
            "🏷️ Nhãn": st.column_config.SelectboxColumn("Nhãn", options=["Hàng Nhập", "Hàng Xuất", "Chứng Từ", "Hiện Trường", "Hải Quan"]),
            "⏳ Trạng thái": st.column_config.SelectboxColumn("Trạng thái", options=["Chưa làm", "Đang làm", "Hoàn thành"]),
            "📅 Deadline": st.column_config.DateColumn("Deadline"),
        }
    )
    
    # Lưu lại những thay đổi trên bảng vào bộ nhớ
    st.session_state.tasks_df = edited_df

    # 3. CẢNH BÁO NHẮC NHỞ NGAY TRÊN GIAO DIỆN
    st.markdown("### 🔔 Nhắc nhở hệ thống")
    for index, row in edited_df.iterrows():
        if row["🚩 Quan trọng"] == True and row["⏳ Trạng thái"] != "Hoàn thành":
            st.warning(f"⚠️ Đừng quên nhiệm vụ quan trọng: **{row['📌 Tên công việc']}** (Hạn: {row['📅 Deadline']})") 


# --- 4. DASHBOARD BÁO CÁO (BIỂU ĐỒ) ---
    st.markdown("---")
    st.subheader("📊 Báo cáo Kho vận trực quan")
    
    # Tính toán dữ liệu từ DataFrame
    status_counts = edited_df["⏳ Trạng thái"].value_counts()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("Tỷ lệ trạng thái công việc:")
        fig, ax = plt.subplots(figsize=(5, 3))
        status_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#ff9999','#66b3ff','#99ff99'])
        ax.set_ylabel("") # Bỏ label trục y
        st.pyplot(fig)
        
    with col_chart2:
        st.write("Số lượng đầu việc theo nhãn:")
        label_counts = edited_df["🏷️ Nhãn"].value_counts()
        st.bar_chart(label_counts)
