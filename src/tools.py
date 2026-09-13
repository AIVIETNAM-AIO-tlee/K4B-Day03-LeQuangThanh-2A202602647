"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "ticket_query",
        "description": "Tra cứu thông tin ticket hỗ trợ IT bằng mã ticket.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "Mã ticket cần tra cứu (ví dụ: 'INC2026001')"
                }
            },
            "required": ["ticket_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "create_ticket",
        "description": "Tạo yêu cầu hỗ trợ kỹ thuật IT cho người dùng.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Mã người dùng cần tạo yêu cầu hỗ trợ (ví dụ: 'USR001')"
                },
                "issue_type": {
                    "type": "string",
                    "description": "Loại sự cố IT, ví dụ: 'network', 'account', 'vpn', 'hardware', 'software'"
                },
                "description": {
                    "type": "string",
                    "description": "Mô tả chi tiết vấn đề người dùng đang gặp phải"
                },
                "priority": {
                    "type": "string",
                    "description": "Mức độ ưu tiên của ticket: 'LOW', 'MEDIUM', 'HIGH', hoặc 'CRITICAL'"
                }
            },
            "required": [
                "user_id",
                "issue_type",
                "description",
                "priority"
            ]
        },
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_TICKETS = {
    "INC2026001": {
        "ticket_id": "INC2026001",
        "user_id": "USR001",
        "issue_type": "vpn",
        "description": "Không thể đăng nhập vào hệ thống VPN của công ty.",
        "status": "IN_PROGRESS",
        "priority": "HIGH",
        "created_at": "2026-09-10 09:30",
        "assigned_to": "IT Support Team"
    },

    "INC2026002": {
        "ticket_id": "INC2026002",
        "user_id": "USR002",
        "issue_type": "network",
        "description": "Không thể kết nối Internet tại văn phòng tầng 5.",
        "status": "OPEN",
        "priority": "MEDIUM",
        "created_at": "2026-09-11 14:15",
        "assigned_to": "Network Team"
    },

    "INC2026003": {
        "ticket_id": "INC2026003",
        "user_id": "USR001",
        "issue_type": "account",
        "description": "Tài khoản email công ty bị khóa sau nhiều lần đăng nhập sai.",
        "status": "RESOLVED",
        "priority": "HIGH",
        "created_at": "2026-09-08 10:20",
        "assigned_to": "IT Service Desk"
    }
}

MOCK_USERS = {
    "USR001": {
        "user_id": "USR001",
        "full_name": "Nguyễn Văn An",
        "email": "an.nguyen@company.vn",
        "department": "Engineering",
        "account_status": "ACTIVE"
    },

    "USR002": {
        "user_id": "USR002",
        "full_name": "Trần Thị Bình",
        "email": "binh.tran@company.vn",
        "department": "Finance",
        "account_status": "ACTIVE"
    },

    "USR003": {
        "user_id": "USR003",
        "full_name": "Lê Minh Thành",
        "email": "thanh.le@company.vn",
        "department": "Human Resources",
        "account_status": "LOCKED"
    }
}


def execute_ticket_query(ticket_id: str) -> str:
    """Thực thi tra cứu thông tin ticket IT."""

    ticket_id = ticket_id.strip().upper()

    ticket = MOCK_TICKETS.get(ticket_id)

    if ticket:
        return json.dumps({
            "status": "SUCCESS",
            "ticket_id": ticket_id,
            "data": ticket
        }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy ticket có mã '{ticket_id}'"
    }, ensure_ascii=False)


def execute_create_ticket(
    user_id: str,
    issue_type: str,
    description: str,
    priority: str
) -> str:
    """Thực thi tạo ticket hỗ trợ IT."""

    user_id = user_id.strip().upper()
    issue_type = issue_type.strip().lower()
    priority = priority.strip().upper()

    # Kiểm tra user có tồn tại hay không
    user = MOCK_USERS.get(user_id)

    if not user:
        return json.dumps({
            "status": "USER_NOT_FOUND",
            "message": f"Không tìm thấy người dùng có mã '{user_id}'"
        }, ensure_ascii=False)

    # Validate priority
    valid_priorities = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    if priority not in valid_priorities:
        return json.dumps({
            "status": "INVALID_PRIORITY",
            "message": (
                f"Mức độ ưu tiên '{priority}' không hợp lệ. "
                f"Giá trị hợp lệ: {sorted(valid_priorities)}"
            )
        }, ensure_ascii=False)

    # Sinh ticket ID giả lập
    ticket_id = f"INC2026{len(MOCK_TICKETS) + 1:03d}"

    new_ticket = {
        "ticket_id": ticket_id,
        "user_id": user_id,
        "issue_type": issue_type,
        "description": description,
        "status": "OPEN",
        "priority": priority,
        "created_at": "2026-09-13 14:00",
        "assigned_to": "IT Service Desk"
    }

    # Lưu vào mock database
    MOCK_TICKETS[ticket_id] = new_ticket

    return json.dumps({
        "status": "SUCCESS",
        "ticket_id": ticket_id,
        "data": new_ticket,
        "message": (
            f"Tạo ticket thành công cho người dùng {user_id}. "
            f"Mã ticket: {ticket_id}."
        )
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "ticket_query": execute_ticket_query,
    "create_ticket": execute_create_ticket,
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        if tool_name == "ticket_query":
            return execute_ticket_query(**arguments)
        elif tool_name == "create_ticket":
            return execute_create_ticket(**arguments)
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
