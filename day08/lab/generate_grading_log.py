import json
import os
from datetime import datetime
from rag_answer import rag_answer

def generate_log():
    # Đảm bảo thư mục logs tồn tại
    os.makedirs("logs", exist_ok=True)
    
    try:
        with open("data/grading_questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file data/grading_questions.json. Hãy chắc chắn rẳng file đã được tải về.")
        return

    log = []
    print(f"Bắt đầu chạy pipeline cho {len(questions)} câu hỏi...")
    
    for q in questions:
        print(f"Đang xử lý câu hỏi: {q['id']}")
        try:
            # Chọn cấu hình tốt nhất của bạn ở đây (ví dụ: retrieval_mode="hybrid", use_rerank=True, ...)
            result = rag_answer(q["question"], retrieval_mode="hybrid", use_rerank=True, verbose=False)
            
            log.append({
                "id": q["id"],
                "question": q["question"],
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "chunks_retrieved": len(result.get("chunks_used", [])),
                "retrieval_mode": result.get("config", {}).get("retrieval_mode", "hybrid"),
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"Lỗi khi xử lý câu hỏi {q['id']}: {e}")
            log.append({
                "id": q["id"],
                "question": q["question"],
                "answer": f"PIPELINE_ERROR: {str(e)}",
                "sources": [],
                "chunks_retrieved": 0,
                "retrieval_mode": "hybrid",
                "timestamp": datetime.now().isoformat(),
            })

    # Ghi log ra file
    log_path = "logs/grading_run.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
        
    print(f"\nHoàn thành! Kết quả đã được lưu tại: {log_path}")

if __name__ == "__main__":
    generate_log()
