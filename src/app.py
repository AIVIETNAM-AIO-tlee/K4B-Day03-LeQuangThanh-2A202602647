"""
🚀 CORE AGENT APPLICATION (DAY 03: CHATBOT VS REACT AGENT)
Thực thi so sánh giữa Chatbot Baseline (Cấp 2) và ReAct Agent kết nối MCP Server (Cấp 3).
"""

import json
import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from mcp_server import MCPITHelpdeskServer
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_AGENT_SYSTEM_PROMPT,
    MAX_ITERATIONS
)
from providers import get_llm_provider

load_dotenv()

def load_test_cases():
    """Tải danh sách 5 test cases từ config/test_cases.json hoặc config/test_cases.example.json"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    if not os.path.exists(config_path):
        example_path = os.path.join(base_dir, "config", "test_cases.example.json")
        if os.path.exists(example_path):
            print("⚠️ [CONFIG NOTICE]: Chưa thấy file 'config/test_cases.json'. Đang dùng mẫu 'config/test_cases.example.json'.")
            print("👉 Hãy chạy: copy config/test_cases.example.json config/test_cases.json và viết test cases theo đề tài của bạn!\n")
            config_path = example_path
        else:
            config_path = "test_cases.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_waterfall_trace(trace_data: list):
    """Ghi vết log Waterfall Trace Log ra file docs/trace_waterfall.json"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    trace_path = os.path.join(docs_dir, "trace_waterfall.json")
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(trace_data, f, ensure_ascii=False, indent=2)
    print(f"📊 [OBSERVABILITY]: Đã lưu {len(trace_data)} sự kiện Waterfall Trace tại '{trace_path}'!")


def run_baseline_chatbot(user_query: str, provider):
    """Chạy Chatbot gốc (Cấp 2) không có công cụ gọi Tool"""
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot phản hồi:\n{response}")



def run_react_agent(user_query: str, provider, mcp_server: MCPITHelpdeskServer) -> list:
    """
    [REACT AGENT LOOP] Thực thi vòng lặp Thought -> Action -> Observation
    với MCP Server cho hệ thống IT Helpdesk.

    Trả về danh sách trace log của phiên thực thi.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")

    step = 0
    trace_logs = []
    tools_list = mcp_server.list_tools()

    while step < MAX_ITERATIONS:
        step += 1
        step_start_time = time.time()

        print(
            f"\n--- 🔄 Vòng lặp ReAct Loop "
            f"(Step {step}/{MAX_ITERATIONS}) ---"
        )

        # Gọi LLM với Native Tool Calling Specs
        llm_response = provider.generate_with_tools(
            user_query,
            tools_list,
            system_prompt=REACT_AGENT_SYSTEM_PROMPT
        )

        latency_ms = round(
            (time.time() - step_start_time) * 1000,
            2
        )

        thought = llm_response.get(
            "thought",
            "Đang suy luận..."
        )

        print(f"🧠 [Thought]: {thought}")

        # ==========================================================
        # TRƯỜNG HỢP 1: LLM trả lời trực tiếp
        # ==========================================================
        if llm_response.get("type") == "text":
            final_content = llm_response.get("content", "")

            print(f"🏁 [Final Answer]: {final_content}")

            trace_logs.append({
                "step": step,
                "query": user_query,
                "action_type": "FINAL_ANSWER",
                "thought": thought,
                "output": final_content,
                "latency_ms": latency_ms
            })

            break

        # ==========================================================
        # TRƯỜNG HỢP 2: LLM đề xuất gọi Tool
        # ==========================================================
        elif llm_response.get("type") == "tool_call":

            tool_name = llm_response.get("tool_name")
            arguments = llm_response.get("arguments", {})

            print(
                f"🛠️ [Action Proposed]: "
                f"{tool_name}({arguments})"
            )

            # ------------------------------------------------------
            # Thực thi Tool qua MCP Server
            # ------------------------------------------------------
            mcp_result = mcp_server.call_tool(
                tool_name,
                arguments
            )

            obs_data = mcp_result.get("result", {})

            # ------------------------------------------------------
            # Observation rỗng
            # ------------------------------------------------------
            if not obs_data:
                print(
                    "👁️ [Observation từ MCP Server]: {}"
                )

                print(
                    "⚠️ [CHÚ Ý]: MCP Server trả về kết quả rỗng!"
                )

                final_answer = (
                    "Chưa thể xử lý yêu cầu vì MCP Server "
                    "không trả về dữ liệu."
                )

            else:
                obs_str = json.dumps(
                    obs_data,
                    ensure_ascii=False
                )

                print(
                    f"👁️ [Observation từ MCP Server]: "
                    f"{obs_str}"
                )

                # ==================================================
                # XỬ LÝ KẾT QUẢ TOOL
                # ==================================================

                status = obs_data.get("status")

                # --------------------------------------------------
                # SUCCESS
                # --------------------------------------------------
                if status == "SUCCESS":

                    # ==============================================
                    # Ticket Query
                    # ==============================================
                    if tool_name == "ticket_query":

                        ticket = obs_data.get("data", {})

                        if ticket:
                            final_answer = (
                                f"Ticket {ticket.get('ticket_id', '')}: "
                                f"{ticket.get('issue_type', '')}. "
                                f"Trạng thái: "
                                f"{ticket.get('status', '')}. "
                                f"Mức độ ưu tiên: "
                                f"{ticket.get('priority', '')}. "
                                f"Mô tả: "
                                f"{ticket.get('description', '')}. "
                                f"Được phân công cho: "
                                f"{ticket.get('assigned_team', '')}."
                            )
                        else:
                            final_answer = (
                                "Đã tìm thấy ticket nhưng "
                                "không có dữ liệu chi tiết."
                            )

                    # ==============================================
                    # Create Ticket
                    # ==============================================
                    elif tool_name == "create_ticket":

                        final_answer = (
                            f"Đã tạo ticket hỗ trợ IT thành công. "
                            f"Mã ticket: "
                            f"{obs_data.get('ticket_id', '')}. "
                            f"Loại sự cố: "
                            f"{obs_data.get('issue_type', '')}. "
                            f"Mức độ ưu tiên: "
                            f"{obs_data.get('priority', '')}. "
                            f"Trạng thái: "
                            f"{obs_data.get('status', '')}."
                        )

                    # ==============================================
                    # Tool khác
                    # ==============================================
                    else:
                        final_answer = (
                            "Đã hoàn tất xử lý qua MCP Server: "
                            + json.dumps(
                                obs_data,
                                ensure_ascii=False
                            )
                        )

                # --------------------------------------------------
                # NOT FOUND
                # --------------------------------------------------
                elif status == "NOT_FOUND":

                    final_answer = obs_data.get(
                        "message",
                        "Không tìm thấy thông tin yêu cầu."
                    )

                # --------------------------------------------------
                # EXECUTION ERROR / UNKNOWN TOOL / OTHER
                # --------------------------------------------------
                else:

                    final_answer = (
                        "Không thể hoàn tất yêu cầu. "
                        "Phản hồi từ công cụ: "
                        + json.dumps(
                            obs_data,
                            ensure_ascii=False
                        )
                    )

            # ======================================================
            # GHI TRACE TOOL EXECUTION
            # ======================================================

            trace_logs.append({
                "step": step,
                "query": user_query,
                "action_type": "TOOL_EXECUTION",
                "tool_name": tool_name,
                "arguments": arguments,
                "observation": obs_data,
                "latency_ms": latency_ms
            })

            # ======================================================
            # FINAL ANSWER
            # ======================================================

            print(
                "🧠 [Thought]: "
                "Đã nhận được Observation từ MCP Server. "
                "Tổng hợp kết quả."
            )

            print(
                f"🏁 [Final Answer]: {final_answer}"
            )

            trace_logs.append({
                "step": step + 1,
                "query": user_query,
                "action_type": "FINAL_ANSWER",
                "thought": (
                    "Tổng hợp kết quả từ MCP Server "
                    "thành công."
                ),
                "output": final_answer,
                "latency_ms": 10.0
            })

            break

    return trace_logs


if __name__ == "__main__":
    print("==========================================================")
    print("🏫 VINUNI AI COURSE - DAY 03 LAB: CHATBOT VS REACT AGENT")
    print("==========================================================")
    import streamlit as st
    provider = get_llm_provider()
    mcp_server = MCPITHelpdeskServer()
    
    print(f"🔌 LLM Provider: {provider.__class__.__name__}")
    print(f"🌐 MCP Server: {mcp_server.server_name}\n")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases thử nghiệm.\n")
    
    if "--interactive" in sys.argv:
        print("🎮 [INTERACTIVE MODE] Trò chuyện trực tiếp với ReAct Agent:")
        print("💡 Gợi ý câu hỏi thử nghiệm:")
        print("- Câu hỏi chung: 'Tôi không thể kết nối Wi-Fi, tôi nên kiểm tra những gì?'")
        print("- Tra cứu ticket: 'Hãy tra cứu thông tin ticket IT với mã INC2026001'")
        print("- Tạo ticket: 'Tôi không thể đăng nhập vào VPN. Hãy tạo một yêu cầu hỗ trợ IT cho tôi.'")
        print("- Multi-step: 'Tôi không thể đăng nhập VPN. Hãy kiểm tra xem đã có ticket nào đang xử lý cho sự cố này chưa. Nếu chưa có, hãy tạo một ticket mới.'")
        print("- Gõ 'exit' hoặc 'quit' để kết thúc phiên trò chuyện.\n")
        while True:
            try:
                user_input = input("👤 Người dùng hỏi: ").strip()
                if not user_input or user_input.lower() in ["exit", "quit"]:
                    print("👋 Tạm biệt! Kết thúc phiên trò chuyện.")
                    break
                logs = run_react_agent(user_input, provider, mcp_server)
                save_waterfall_trace(logs)
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Đã thoát phiên tương tác.")
                break
    elif "--all" in sys.argv:
        print("🚀 [TEST SUITE MODE] Kiểm tra 5 Test Cases:")
        completed_count = 0
        todo_count = 0
        all_traces = []
        
        for tc in tests:
            print(f"\n==================================================")
            print(f"🧪 [{tc['id']}] Loại test: {tc['type']} (Độ phức tạp: {tc['complexity']})")
            print(f"📌 Kỳ vọng: {tc['expected_behavior']}")
            
            if tc["question"].strip().startswith("TODO"):
                print(f"⏸️ [CHƯA KÍCH HOẠT - ĐANG LÀ TODO]:")
                print(f"   {tc['question']}")
                print(f"   👉 Hãy mở file 'config/test_cases.json' để viết câu hỏi thực tế cho Test Case này!")
                todo_count += 1
            else:
                logs = run_react_agent(tc["question"], provider, mcp_server)
                all_traces.extend(logs)
                completed_count += 1
                
        print(f"\n==================================================")
        print(f"📊 [KẾT QUẢ TEST SUITE]: Đã thực thi {completed_count}/{len(tests)} Test Cases | {todo_count} Test Cases đang chờ điền câu hỏi (TODO)")
        if all_traces:
            save_waterfall_trace(all_traces)
        print(f"💡 Để trò chuyện trực tiếp từng câu: Chạy 'python src/app.py --interactive'")
    else:
        # Chế độ mặc định khi chỉ gõ 'python src/app.py'
        print("ℹ️ HƯỚNG DẪN SỬ DỤNG CHƯƠNG TRÌNH:")
        print("  1. Chat trực tiếp liên tục:   python src/app.py --interactive")
        print("  2. Chạy toàn bộ Test Cases:    python src/app.py --all\n")
        
        sample_query = tests[1]["question"]
        print(f"--- 🏁 DEMO CHẠY THỬ 1 TEST CASE MẪU (TC02: Tra cứu học vụ) ---")
        logs = run_react_agent(sample_query, provider, mcp_server)
        save_waterfall_trace(logs)
        print("\n💡 Hãy thử ngay lệnh: python src/app.py --interactive để chat trực tiếp!")
