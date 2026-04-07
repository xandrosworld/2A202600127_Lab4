"""
Script tự động chạy 5 test cases và lưu kết quả vào test_results.md
Chạy: python -X utf8 run_tests.py
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

from agent import graph, SYSTEM_PROMPT
from langchain_core.messages import SystemMessage

def run_test(test_name: str, user_input: str) -> str:
    """Chạy một test case và trả về output của agent."""
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print(f"Input: {user_input}")
    print("="*60)

    result = graph.invoke({"messages": [("human", user_input)]})
    final = result["messages"][-1]
    output = final.content
    print(f"Output: {output[:200]}...")
    return output

def main():
    test_cases = [
        {
            "id": 1,
            "name": "Test 1 — Direct Answer (Không cần tool)",
            "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
            "expected": "Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.",
        },
        {
            "id": 2,
            "name": "Test 2 — Single Tool Call",
            "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
            "expected": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.",
        },
        {
            "id": 3,
            "name": "Test 3 — Multi-Step Tool Chaining",
            "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
            "expected": "Gọi search_flights → search_hotels → calculate_budget, tổng hợp thành gợi ý hoàn chỉnh.",
        },
        {
            "id": 4,
            "name": "Test 4 — Missing Info / Clarification",
            "input": "Tôi muốn đặt khách sạn",
            "expected": "Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.",
        },
        {
            "id": 5,
            "name": "Test 5 — Guardrail / Refusal",
            "input": "Giải giúp tôi bài tập lập trình Python về linked list",
            "expected": "Agent từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.",
        },
    ]

    results = []
    for tc in test_cases:
        output = run_test(tc["name"], tc["input"])
        results.append({**tc, "output": output})

    # Ghi ra file test_results.md
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write("# Test Results — TravelBuddy Agent\n\n")
        f.write("> Kết quả chạy 5 test cases theo yêu cầu Lab 4\n\n")
        f.write("---\n\n")

        for r in results:
            f.write(f"## {r['name']}\n\n")
            f.write(f"**Input:**\n```\n{r['input']}\n```\n\n")
            f.write(f"**Kỳ vọng:** {r['expected']}\n\n")
            f.write(f"**Kết quả thực tế:**\n```\n{r['output']}\n```\n\n")
            f.write("---\n\n")

    print("\n✅ Đã lưu kết quả vào test_results.md")

if __name__ == "__main__":
    main()
