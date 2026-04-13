# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Thái Doãn Minh Hải
**Vai trò trong nhóm:** Indexing Owner
**Ngày nộp:** 13.04.2026
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong lab này, tôi chủ yếu phụ trách Sprint 1 và một phần Sprint 2, tập trung vào xây dựng pipeline indexing cho hệ thống RAG. Cụ thể, tôi implement file index.py để đọc dữ liệu tài liệu (txt), thực hiện chunking văn bản, sau đó tạo embedding cho từng chunk và lưu vào ChromaDB. Tôi cũng đảm bảo metadata như source, section được lưu đầy đủ để phục vụ bước retrieval và citation sau này.

Ngoài ra, tôi phải đảm bảo embedding model dùng trong indexing giống với retrieval để tránh mismatch. Công việc của tôi là nền tảng cho toàn bộ pipeline: nếu indexing không tốt thì retrieve sẽ sai, dẫn đến LLM trả lời không chính xác. Phần của tôi kết nối trực tiếp với rag_answer.py (retrieve) và eval.py (đánh giá kết quả).

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Sau lab này, tôi hiểu rõ hơn về chunking và tầm quan trọng của nó trong RAG. Trước đây tôi nghĩ chỉ cần chia văn bản thành các đoạn nhỏ là đủ, nhưng thực tế chunking ảnh hưởng trực tiếp đến chất lượng retrieval. Nếu chunk quá lớn, embedding sẽ bị “nhiễu” vì chứa nhiều ý; nếu quá nhỏ, sẽ mất context cần thiết để trả lời.

Tôi cũng hiểu rõ hơn về metadata trong retrieval. Không chỉ text, mà việc lưu source, section giúp hệ thống có thể trích dẫn chính xác và hỗ trợ evaluation (context recall). Điều này cho thấy RAG không chỉ là embedding mà còn là thiết kế dữ liệu hợp lý để phục vụ downstream tasks.

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

Điều khiến tôi bất ngờ là dù đã indexing đúng, nhưng kết quả retrieval vẫn không tốt như kỳ vọng. Ban đầu tôi nghĩ chỉ cần embed và lưu vào vector DB là đủ, nhưng thực tế chất lượng retrieval phụ thuộc nhiều vào cách chunking và nội dung chunk.

Một khó khăn lớn là debug khi retrieve không ra đúng tài liệu. Tôi phải kiểm tra lại từ bước: dữ liệu đầu vào, cách split chunk, embedding model, và cả metadata. Có trường hợp query đúng nhưng không match vì wording khác (synonym), điều này cho thấy hạn chế của dense retrieval.

Giả thuyết ban đầu của tôi là embedding sẽ “hiểu hết ngữ nghĩa”, nhưng thực tế cần thêm hybrid hoặc query transformation để cải thiện.

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

Câu hỏi: SLA xử lý ticket P1 là bao lâu
**Phân tích:**

Ở baseline (dense retrieval), hệ thống có thể retrieve được chunk chứa thông tin SLA P1, tuy nhiên đôi khi kết quả không ổn định nếu chunk chứa nhiều thông tin khác. Khi chunking chưa tối ưu, embedding của đoạn này bị nhiễu, dẫn đến ranking không cao và có thể không nằm trong top_k.

Về generation, LLM trả lời khá đúng khi context đã có thông tin cần thiết. Tuy nhiên, nếu retrieve thiếu chunk chính xác, model có xu hướng trả lời sai hoặc không đủ thông tin.

Sau khi áp dụng variant (ví dụ: hybrid hoặc rerank), kết quả cải thiện rõ rệt. Hybrid giúp bắt được keyword “P1” tốt hơn, trong khi rerank giúp chọn đúng chunk chứa SLA thay vì các chunk liên quan chung chung đến ticket.

Lỗi chính nằm ở bước retrieval (do chunking + ranking) hơn là generation. Điều này cho thấy việc tối ưu retrieval có impact lớn hơn nhiều so với tuning prompt.

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Nếu có thêm thời gian, tôi muốn thử cải tiến chunking strategy, ví dụ chunk theo semantic boundary thay vì split cố định theo độ dài. Ngoài ra, tôi muốn thử query expansion hoặc hybrid retrieval, vì evaluation cho thấy dense retrieval chưa xử lý tốt các query có keyword cụ thể như “P1” hoặc mã lỗi. Những cải tiến này có thể giúp tăng context recall và cải thiện toàn bộ pipeline.

_Lưu file này với tên: `reports/individual/[ten_ban].md`_
_Ví dụ: `reports/individual/nguyen_van_a.md`_
