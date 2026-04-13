# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Đặng Tuấn Anh
**Vai trò trong nhóm:** Documentation Owner  
**Ngày nộp:** 13/04/2026  

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong phần Lab này, tôi đảm nhận chính vai trò Documentation Owner. Cụ thể, tôi đã viết file `architecture.md` để mô tả thiết kế tổng quan của hệ thống, bao gồm các quyết định về chunking strategy và cơ chế Hybrid Retrieval kết hợp với Reranking. Nhận thấy nhóm cần một công cụ tự động hóa việc xuất log kết quả theo chuẩn format của file `SCORING.md`, tôi đã chủ động code thêm file script `generate_grading_log.py`. Nhiệm vụ của file script này nối luồng từ lúc tải `grading_questions.json`, gọi hàm `rag_answer`, xử lý các ngoại lệ (`PIPELINE_ERROR`) để không làm sập tiến trình nếu 1 câu bị lỗi, và cuối cùng xuất ra log `logs/grading_run.json`. Công việc của tôi đóng vai trò cầu nối, giúp các bạn code Core Pipeline và Eval Owner dễ dàng chạy lệnh đánh giá và đóng gói bộ hồ sơ kết quả tự động, chính xác.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Tôi hiểu rõ hơn về concept **Hybrid Retrieval** và quy trình **Evaluation Loop**. Ban đầu tôi nghĩ Semantic Search (Dense) là "chìa khóa vạn năng" giải quyết được mọi câu hỏi. Nhưng khi viết tài liệu và xem xét log, tôi nhận ra Dense Search thường bỏ sót những từ khoá chuyên ngành hoặc mã số viết tắt. Hybrid Retrieval (kết hợp Dense và Sparse – BM25) thực sự bù đắp được điểm yếu này bằng việc tính điểm tổng hợp qua Reciprocal Rank Fusion (RRF). 
Bên cạnh đó, mô hình đánh giá LLM-as-Judge làm tôi hiểu rõ cách định lượng các metric như Faithfulness (mức độ bám vào tài liệu) và Context Recall, từ đó dễ dàng thấy điểm mạnh yếu của hệ thống thay vì phải đọc tay hàng trăm câu trả lời.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

Điều khiến tôi tốn nhiều thời gian debug nhất xoay quanh vấn đề **Hallucination** và các fail cases khi chạy hàng loạt câu hỏi ẩn. Khi tôi thử viết script `generate_grading_log.py`, tôi gặp trường hợp một số câu hỏi khiến cho mô hình sinh chữ quá giới hạn token hoặc bị crash ở hàm của Langchain/LlamaIndex. Nếu không có cơ chế `try...except`, tiến trình đang chấm dở 8/10 câu chạy được sẽ bung lỗi mất sạch output. 
Ngoài ra, tôi khá ngạc nhiên về việc câu hỏi `gq07` (thông tin ngoại lệ không có trong hệ thống) làm AI có xu hướng cố gắng đưa ra một đáp án (lúc đầu bị điểm Faithfulness = 1). Việc tinh chỉnh Grounded Prompt "nếu không có thông tin hãy trả lời tôi không biết" là không hề dễ dàng khi LLM luôn luôn có thiên kiến "muốn thể hiện sự hiểu biết".

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** `gq05` (Contractor cần Admin Access — điều kiện?)

**Phân tích:**
Dựa vào Scorecard, ta thấy rất rõ sự cải thiện về chất lượng Context được gọi lên phục vụ quá trình generation.
- **Baseline (Dense-only)**: Trả lời sai trầm trọng về mặt sự thật, điểm **Faithfulness = 1/5**. Nguyên nhân cốt lõi là bước **Retrieval**: mô hình Dense đã bị nhiễu bởi các từ khoá chung chung như "Access" mà không bắt được chính xác danh từ ngách "Contractor". Vì Context đưa lên không chứa đáp án, LLM đã tự động bịa ra một quy trình xin quyền (hallucinate).
- **Variant (Hybrid + Rerank)**: Cấu hình mới giúp đẩy điểm **Faithfulness lên 5/5**. Kỹ thuật Hybrid đã thành công gom đúng đoạn chunk có chứa từ "Contractor", sau đó Cross-encoder reranker đẩy chunk có thông tin quan trọng này lên top 1. Kết quả là LLM không cần xài kiến thức bên ngoài (no hallucination). Tuy điểm Completeness bị rớt nhẹ xuống 3, điều này cho thấy câu trả lời sinh ra có vẻ khá súc tích và cắt đi vài điều kiện phụ rườm rà, song tính "Chính xác về mặt tài liệu" (Faithfulness) vẫn là ưu tiên số 1 của RAG.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Dựa trên việc mức Completeness ở Variant của `gq05` giảm (từ 5 xuống 3), tôi nghĩ nếu có thêm thời gian tôi sẽ cân nhắc ứng dụng **Query Rewriting / Expansion**. Tôi sẽ thêm 1 bước LLM nhỏ để mở rộng hoặc chuẩn hoá các từ khóa (như từ "Contractor" có thể mở rộng thành "External Vendor / Third-party") trước khi đẩy vào không gian tìm kiếm, giúp lấy về đủ các mệnh đề phụ liên quan mà không làm mất đi tính chính xác của chunk chính.

---


