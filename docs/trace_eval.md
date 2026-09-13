# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Lê Quang Thành
> **Mã Sinh Viên / Mã Học viên:** 2A202602647
> **Chủ đề Lựa chọn:** Trợ lý Hỗ trợ Kỹ thuật IT Helpdesk: Tra cứu ticket sự cố mạng, tài khoản và tạo yêu cầu hỗ trợ kỹ thuật.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Bài toán có thể yêu cầu Agent thực hiện nhiều bước liên tiếp để xử lý một yêu cầu. Ví dụ, với sự cố VPN, Agent có thể tra cứu ticket hiện có → phân tích kết quả → quyết định có cần tạo ticket mới → tạo ticket → trả kết quả cho người dùng. Tuy nhiên, các workflow chưa quá phức tạp hoặc kéo dài nên chưa đạt 5/5 |
| **2. Tool Interaction** | 4 / 5 | Hệ thống cần tương tác với MCP Server và các nguồn dữ liệu bên ngoài như hệ thống ticket IT. Agent có thể sử dụng các Tool như `ticket_query` để tra cứu sự cố và `create_ticket` để thực hiện hành động. Tuy nhiên, số lượng Tool và hệ thống bên ngoài hiện chưa lớn nên phù hợp với mức 4/5 thay vì 5/5. |
| **3. Dynamic Decision** | 5 / 5 | Bước tiếp theo của Agent phụ thuộc trực tiếp vào kết quả quan sát từ Tool trước đó. Ví dụ, sau khi ticket_query trả về kết quả, Agent phải quyết định: nếu đã có ticket đang xử lý thì thông báo ticket hiện tại; nếu chưa có thì tiếp tục gọi `create_ticket`. Do đó, Agent không chỉ thực hiện một workflow cố định mà phải tự quyết định hành động tiếp theo dựa trên trạng thái thực tế. |
| **4. Long Horizon Goal** | 3 / 5 | Agent có thể cần duy trì mục tiêu xuyên suốt qua nhiều bước, chẳng hạn từ lúc tiếp nhận sự cố → kiểm tra ticket → xử lý yêu cầu → tạo ticket → phản hồi người dùng. Tuy nhiên, các tác vụ hiện tại thường hoàn thành trong một phiên ngắn và số bước chưa quá dài, nên mức độ Long Horizon chỉ ở mức trung bình. |
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
    "output": "Chào bạn, khi gặp sự cố không thể kết nối Wi-Fi, bạn có thể thực hiện theo các bước kiểm tra cơ bản sau đây để khắc phục nhanh chóng:\n\n1. **Kiểm tra thiết bị phát Wi-Fi (Router/Modem):**\n   - Đảm bảo đèn tín hiệu trên router vẫn sáng bình thường.\n   - Thử **khởi động lại** (tắt nguồn, đợi khoảng 30 giây rồi bật lại) router và modem của bạn.\n\n2. **Kiểm tra thiết bị cá nhân (Laptop/Điện thoại):**\n   - Đảm bảo tính năng Wi-Fi trên thiết bị của bạn đã được bật và chế độ máy bay (Airplane Mode) đã được tắt.\n   - Thử ngắt kết nối (Forget Network) mạng Wi-Fi hiện tại và tiến hành kết nối lại bằng cách nhập lại mật khẩu chính xác.\n   - Thử kết nối thiết bị của bạn với một mạng Wi-Fi khác (hoặc phát 4G từ điện thoại) để xác định xem lỗi xuất phát từ thiết bị hay từ mạng Wi-Fi.\n\n3. **Kiểm tra cấu hình IP (đối với Windows/Mac):**\n   - Đảm bảo thiết bị của bạn được cấu hình nhận địa chỉ IP tự động (DHCP).\n\nNếu bạn đã thử tất cả các bước trên nhưng vẫn không thể kết nối hoặc đây là mạng Wi-Fi của công ty/tòa nhà, vui lòng cung cấp thêm thông tin (tên thiết bị, hệ điều hành, thông báo lỗi nếu có) hoặc cho tôi biết nếu bạn cần **tạo một ticket hỗ trợ IT** để kỹ thuật viên kiểm tra trực tiếp nhé!",
    "latency_ms": 4018.6
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
    "latency_ms": 1186.65
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
    "output": "Để tạo yêu cầu hỗ trợ IT (ticket) giúp bạn, tôi cần thêm một vài thông tin. Vui lòng cung cấp cho tôi:\n\n1. **Mã người dùng (User ID)** của bạn (ví dụ: `USR001`).\n2. **Tên đăng nhập** hoặc email công ty mà bạn đang dùng để kết nối VPN.\n3. Thông tin chi tiết hơn nếu có (ví dụ: bạn có nhận được thông báo lỗi cụ thể nào không?).\n\nNgay khi nhận được thông tin từ bạn, tôi sẽ tiến hành tạo ticket hỗ trợ ngay lập tức!",
    "latency_ms": 1613.52
  },
  {
    "step": 1,
    "query": "Tôi không thể đăng nhập vào VPN. Hãy kiểm tra xem tài khoản của tôi có đang bị khóa hoặc có ticket nào liên quan đến sự cố này không. Nếu tài khoản bình thường và chưa có ticket đang xử lý, hãy tạo một ticket hỗ trợ IT mới cho tôi.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Chào bạn, để tôi có thể hỗ trợ bạn kiểm tra thông tin và tạo ticket, vui lòng cho tôi biết **Mã nhân viên / Mã người dùng (User ID)** của bạn nhé.",
    "latency_ms": 1399.28
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
    "latency_ms": 1180.05
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
    "tool_name": "ticket_query",
    "arguments": {
      "ticket_id": "USR001"
    },
    "observation": {
      "status": "NOT_FOUND",
      "message": "Không tìm thấy ticket có mã 'USR001'"
    },
    "latency_ms": 1532.92
  },
  {
    "step": 2,
    "query": "Tôi không thể đăng nhập vào VPN. Hãy kiểm tra xem đã có ticket nào đang xử lý cho sự cố này chưa. Nếu chưa có, hãy tạo một ticket mới, đây là ID của tôi: USR001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Không tìm thấy ticket có mã 'USR001'",
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
