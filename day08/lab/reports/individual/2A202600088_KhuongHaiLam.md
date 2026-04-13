# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Khương Hải Lâm
**Vai trò trong nhóm:** Documentation Owner  
**Ngày nộp:** 13/04/2026
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong lab này, tôi đảm nhận vai trò Documentation Owner, tập trung chính vào Sprint 3 và 4. Tôi chịu trách nhiệm ghi chép Tuning Log và thực hiện AB testing để tối ưu hóa pipeline. Cụ thể, tôi đã thiết lập và so sánh Baseline (Dense retrieval, chunk 300, top_k 10) với Variant 1 (Hybrid retrieval, overlap tăng lên 60, top_k 15 và bật Rerank). 

Tôi đã trực tiếp tham gia vào việc phân tích các lỗi từ scorecard của Baseline để đưa ra quyết định chuyển sang Hybrid retrieval nhằm giải quyết các câu hỏi chứa mã lỗi (như ERR-403) và các tên gọi cũ (Approval Matrix). Công việc của tôi kết nối chặt chẽ với Retrieval Owner để điều chỉnh tham số và giúp cả nhóm hiểu rõ tại sao Variant lại cho kết quả tốt hơn thông qua các chỉ số định lượng như Faithfulness và Context Recall.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Sau lab này, tôi hiểu rõ hơn về hai concept quan trọng: **Hybrid Retrieval** và **Evaluation Loop (LLM-as-Judge)**.

- **Hybrid Retrieval:** Tôi nhận ra rằng Dense retrieval (vector search) tuy mạnh về hiểu ngữ nghĩa nhưng lại rất dễ bỏ lỡ các từ khóa chính xác hoặc mã lỗi đặc thù. Việc kết hợp với Sparse retrieval (BM25) giúp hệ thống "vừa hiểu nghĩa, vừa bắt đúng chữ", đặc biệt quan trọng trong các tài liệu kỹ thuật và chính sách có nhiều thuật ngữ cố định.
- **Evaluation Loop:** Trước đây tôi nghĩ việc đánh giá model chỉ là đọc thử vài câu. Qua lab, tôi thấy sức mạnh của việc dùng LLM để chấm điểm tự động dựa trên các metric như Faithfulness và Completeness. Nó giúp quy trình tuning trở nên khoa học hơn; thay vì đoán mò, chúng tôi nhìn vào điểm số để biết chính xác phần nào trong pipeline (indexing, retrieval hay generation) đang bị hỏng.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

Điều làm tôi ngạc nhiên nhất là hiện tượng "ảo giác" (hallucination) xảy ra ngay cả khi đã cung cấp context. Trong câu hỏi q10 về quy trình VIP, Baseline ban đầu có điểm Faithfulness rất thấp (1/5) vì model cố gắng suy luận ra một quy trình không hề tồn tại trong tài liệu thay vì từ chối trả lời. Giả thuyết ban đầu của tôi là chỉ cần top_k đủ lớn là model sẽ trả lời đúng, nhưng thực tế context quá dài đôi khi làm model bị "lost in the middle".

Khó khăn lớn nhất là việc cân bằng giữa các tham số. Khi tăng top_k để tăng Recall, tôi lại gặp vấn đề về độ nhiễu (noise) trong prompt khiến Completeness giảm xuống. Việc debug các lỗi này mất nhiều thời gian vì phải chạy lại toàn bộ scorecard để thấy được tác động thực sự của một thay đổi nhỏ trong chunking hay overlap.

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** "Contractor từ bên ngoài công ty có thể được cấp quyền Admin Access không? Nếu có, cần bao nhiêu ngày và có yêu cầu đặc biệt gì?" (ID: gq05)

**Phân tích:**
Trong bản Baseline, câu hỏi này đạt điểm Faithfulness rất thấp (1/5) mặc dù Relevance đạt 5/5. Lỗi nằm ở bước **Indexing và Retrieval**. Tài liệu "Access Control SOP" chia thông tin thành các Section khác nhau: Section 1 nói về đối tượng áp dụng (bao gồm contractor), còn Section 2 nói về yêu cầu cho Admin Access (Level 4). 

Ở Baseline, do top_k_select chỉ là 3, hệ thống chỉ lấy được các đoạn văn về quy trình cấp quyền Admin nhưng bỏ lỡ đoạn nói về "đối tượng áp dụng" ở đầu tài liệu. Do đó, model đã trả lời sai là contractor không được cấp quyền hoặc trả lời thiếu căn cứ. 

Khi chuyển sang Variant với **Hybrid Retrieval** và tăng **top_k_search lên 15**, hệ thống đã bắt được từ khóa "contractor" từ Section 1 hiệu quả hơn. Kết hợp với bước **Rerank**, đoạn văn chứa thông tin về đối tượng áp dụng được đẩy lên trên, giúp model có đủ bằng chứng để khẳng định contractor "CÓ" quyền và liệt kê đủ 3 yêu cầu: IT Manager/CISO phê duyệt, 5 ngày xử lý và training bắt buộc. Điểm Faithfulness ở Variant đã tăng lên tuyệt đối 5/5.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Nếu có thêm thời gian, tôi sẽ thử nghiệm việc **bổ sung Metadata Filtering** dựa trên `effective_date`. Kết quả eval hiện tại cho thấy model vẫn thỉnh thoảng nhầm lẫn giữa các phiên bản chính sách cũ và mới (như ở câu q01 và q10). Bằng cách ép model lọc metadata trước khi retrieve, tôi có thể đảm bảo 100% thông tin lấy ra là bản mới nhất, từ đó giải quyết triệt để vấn đề "stale documents" mà hiện tại Hybrid retrieval vẫn chưa xử lý được tốt.

---
