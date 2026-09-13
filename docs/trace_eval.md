# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Lê Quang Thành
> **Mã Sinh Viên / Mã Học viên:** 2A202602647
> **Chủ đề Lựa chọn:** Trợ lý Hỗ trợ Kỹ thuật IT Helpdesk: Tra cứu ticket sự cố mạng, tài khoản và tạo yêu cầu hỗ trợ kỹ thuật.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không? |
| **2. Tool Interaction** | 4 / 5 | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |
| **3. Dynamic Decision** | 5 / 5 | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không? |
| **4. Long Horizon Goal** | 3 / 5 | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không? |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tôi không thể kết nối Wi-Fi, tôi nên kiểm tra những gì?",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Chào bạn! Khi gặp sự cố không thể kết nối Wi-Fi, bạn có thể thực hiện theo các bước kiểm tra cơ bản sau đây:\n\n1. **Khởi động lại thiết bị (Restart):** Khởi động lại máy tính hoặc điện thoại của bạn. Thao tác này giúp làm mới các kết nối mạng đang bị treo.\n2. **Kiểm tra công tắc/cài đặt Wi-Fi:** \n   - Đảm bảo rằng Wi-Fi trên thiết bị của bạn đã được **Bật (On)**.\n   - Kiểm tra xem máy có đang ở **Chế độ máy bay (Airplane Mode)** hay không.\n3. **Quên mạng và kết nối lại (Forget Network):** \n   - Vào cài đặt Wi-Fi, chọn mạng bạn đang muốn kết nối và chọn \"Quên mạng này\" (Forget Network).\n   - Sau đó, nhập lại mật khẩu chính xác và kết nối lại.\n4. **Khởi động lại bộ định tuyến (Router/Modem):** Rút nguồn của router/modem Wi-Fi, chờ khoảng 30 giây đến 1 phút rồi cắm điện lại.\n5. **Kiểm tra trên thiết bị khác:** Thử kết nối một thiết bị khác (như điện thoại) vào cùng mạng Wi-Fi đó xem có vào được mạng không, để xác định lỗi do thiết bị của bạn hay do đường truyền Internet/Router.\n\nNếu bạn đã thử các bước trên mà vẫn không thể kết nối, hãy cho tôi biết (hoặc cung cấp mã nhân viên/mã người dùng và mô tả chi tiết nếu bạn cần tôi **tạo ticket hỗ trợ kỹ thuật IT** cho sự cố này nhé).",
    "latency_ms": 3547.42
  },
  {
    "step": 1,
    "query": "Hãy tra cứu thông tin ticket IT với mã INC2026001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "ticket_query",
    "arguments": {
      "ticket_id": "INC2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "ticket_id": "INC2026001",
      "data": {
        "ticket_id": "INC2026001",
        "user_id": "USR001",
        "issue_type": "vpn",
        "description": "Không thể đăng nhập vào hệ thống VPN của công ty.",
        "status": "IN_PROGRESS",
        "priority": "HIGH",
        "created_at": "2026-09-10 09:30",
        "assigned_to": "IT Support Team"
      }
    },
    "latency_ms": 2902.94
  },
  {
    "step": 2,
    "query": "Hãy tra cứu thông tin ticket IT với mã INC2026001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Ticket INC2026001: vpn. Trạng thái: IN_PROGRESS. Mức độ ưu tiên: HIGH. Mô tả: Không thể đăng nhập vào hệ thống VPN của công ty.. Được phân công cho: .",
    "latency_ms": 10.0
  },
  {
    "step": 1,
    "query": "Tôi không thể đăng nhập vào VPN của công ty. Hãy tạo một yêu cầu hỗ trợ IT cho tôi.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Để tôi có thể tạo yêu cầu hỗ trợ (ticket) giúp bạn, vui lòng cung cấp thêm **mã nhân viên (user_id)** của bạn nhé. \n\nVí dụ: `USR001`, `USR123`,...",
    "latency_ms": 3039.14
  },
  {
    "step": 1,
    "query": "Tôi không thể đăng nhập vào VPN. Hãy kiểm tra xem tài khoản của tôi có đang bị khóa hoặc có ticket nào liên quan đến sự cố này không. Nếu tài khoản bình thường và chưa có ticket đang xử lý, hãy tạo một ticket hỗ trợ IT mới cho tôi.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Chào bạn, để tôi có thể kiểm tra trạng thái tài khoản, tra cứu ticket hiện tại và tạo ticket mới cho bạn, bạn vui lòng cung cấp cho tôi **Mã nhân viên (User ID)** của bạn nhé!",
    "latency_ms": 2146.21
  },
  {
    "step": 1,
    "query": "Hãy tra cứu ticket IT với mã INC9999999.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "ticket_query",
    "arguments": {
      "ticket_id": "INC9999999"
    },
    "observation": {
      "status": "NOT_FOUND",
      "message": "Không tìm thấy ticket có mã 'INC9999999'"
    },
    "latency_ms": 2029.6
  },
  {
    "step": 2,
    "query": "Hãy tra cứu ticket IT với mã INC9999999.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Không tìm thấy ticket có mã 'INC9999999'",
    "latency_ms": 10.0
  },
  {
    "step": 1,
    "query": "Tôi không thể đăng nhập vào VPN. Hãy kiểm tra xem đã có ticket nào đang xử lý cho sự cố này chưa. Nếu chưa có, hãy tạo một ticket mới, đây là ID của tôi: USR001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "create_ticket",
    "arguments": {
      "description": "Người dùng không thể đăng nhập vào VPN cần hỗ trợ kỹ thuật.",
      "priority": "MEDIUM",
      "user_id": "USR001",
      "issue_type": "vpn"
    },
    "observation": {
      "status": "SUCCESS",
      "ticket_id": "INC2026004",
      "data": {
        "ticket_id": "INC2026004",
        "user_id": "USR001",
        "issue_type": "vpn",
        "description": "Người dùng không thể đăng nhập vào VPN cần hỗ trợ kỹ thuật.",
        "status": "OPEN",
        "priority": "MEDIUM",
        "created_at": "2026-09-13 14:00",
        "assigned_to": "IT Service Desk"
      },
      "message": "Tạo ticket thành công cho người dùng USR001. Mã ticket: INC2026004."
    },
    "latency_ms": 5799.66
  },
  {
    "step": 2,
    "query": "Tôi không thể đăng nhập vào VPN. Hãy kiểm tra xem đã có ticket nào đang xử lý cho sự cố này chưa. Nếu chưa có, hãy tạo một ticket mới, đây là ID của tôi: USR001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Đã tạo ticket hỗ trợ IT thành công. Mã ticket: INC2026004. Loại sự cố: . Mức độ ưu tiên: . Trạng thái: SUCCESS.",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 6 / 6 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 3/3 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
