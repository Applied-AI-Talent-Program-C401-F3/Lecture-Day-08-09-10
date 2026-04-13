# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Hoàng Quốc Hùng  
**Vai trò trong nhóm:** Retrieval Owner  
**Ngày nộp:** 13/04/2026  
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong lab Day 08, tôi phụ trách vai trò Retrieval Owner với trọng tâm ở Sprint 1 và Sprint 3. Ở Sprint 1, tôi làm việc với phần index để rà lại chất lượng chunking và metadata, đảm bảo các chunk không bị cắt giữa điều khoản quan trọng và có đủ trường `source`, `section`, `effective_date` phục vụ truy xuất và trích dẫn. Ở Sprint 3, tôi triển khai và thử nghiệm các chiến lược retrieval gồm dense, sparse (BM25) và hybrid, sau đó kết hợp thêm rerank để giảm nhiễu khi đưa context vào prompt. Tôi phối hợp với Documentation Owner để ghi lại tuning log theo A/B rule, đồng thời trao đổi với Eval Owner để đọc scorecard và xác định nguyên nhân sai nằm ở retrieval hay generation. Phần việc của tôi là cầu nối trực tiếp giữa indexing và answer quality.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Điều tôi hiểu rõ nhất là faithfulness của hệ thống RAG phụ thuộc rất mạnh vào retrieval quality. Trước khi làm lab, tôi thường có xu hướng đổ lỗi cho prompt hoặc model khi câu trả lời sai. Sau khi chạy scorecard, tôi thấy nhiều lỗi xuất phát từ việc evidence đúng không vào top-k, tức vấn đề nằm ở truy xuất hơn là sinh câu trả lời. Tôi cũng hiểu rõ hơn khi nào dense hiệu quả và khi nào hybrid cần thiết. Dense mạnh ở ngữ nghĩa tổng quát, nhưng yếu ở truy vấn chứa mã lỗi, alias hoặc từ khóa kỹ thuật cứng. Sparse BM25 bắt keyword tốt, nhưng nếu dùng riêng thì dễ thiếu ngữ cảnh. Hybrid giúp cân bằng hai phía. Ngoài ra, metadata tốt không chỉ để citation mà còn giúp debug nhanh vì biết chính xác model đang dựa vào nguồn nào.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

Khó khăn lớn nhất là kiểm soát thí nghiệm để không vi phạm A/B rule. Ban đầu tôi muốn đổi nhiều thứ cùng lúc như tăng top_k_search, bật rerank và chuyển hybrid để cải thiện nhanh. Tuy nhiên cách này khiến nhóm không thể biết chính xác yếu tố nào tạo ra cải thiện. Sau khi trao đổi lại, tôi tách thí nghiệm theo hướng kỷ luật hơn: đổi retrieval mode trước, giữ các biến còn lại ổn định. Điều làm tôi ngạc nhiên là chỉ cần thay dense bằng hybrid đã cải thiện rõ ở nhóm câu hỏi có keyword cứng mà không làm tụt đáng kể các câu ngữ nghĩa tự nhiên. Tôi cũng mất thời gian ở bước xử lý query tiếng Việt có ký hiệu kỹ thuật, vì tokenization không tốt sẽ làm sparse retrieval bắt sai cụm từ và tăng noise ở bước rerank.

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** "ERR-403-AUTH nghĩa là gì và cần xử lý thế nào theo tài liệu nội bộ?"

**Phân tích:**

Ở baseline dense, câu hỏi này có rủi ro trả lời thiếu chắc chắn vì chuỗi `ERR-403-AUTH` là token kỹ thuật, không mang nhiều ngữ nghĩa tự nhiên. Dense retrieval có thể lấy các đoạn liên quan đến xác thực nói chung nhưng bỏ sót đoạn có đúng mã lỗi hoặc quy trình xử lý cụ thể. Khi chunk đúng không được đưa vào top context, model dễ suy diễn thêm, làm giảm Faithfulness và Completeness.

Sau khi chuyển sang hybrid, phần sparse retrieval giúp bắt chính xác keyword mã lỗi, còn dense giữ vai trò bổ sung ngữ cảnh. Kết hợp hai luồng bằng fusion giúp tăng xác suất lấy đúng evidence ngay từ bước retrieve. Khi context vào prompt đúng hơn, câu trả lời có citation rõ ràng và ổn định hơn ở các truy vấn kỹ thuật. Trường hợp này cho thấy failure mode chính nằm ở retrieval thay vì generation: prompt không đổi, model không đổi, nhưng chất lượng tăng khi evidence được chọn tốt hơn. Đây là lý do tôi đề xuất giữ hybrid cho nhóm truy vấn chứa alias, mã lỗi, tên viết tắt.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Nếu có thêm thời gian, tôi sẽ chạy một vòng A/B tách riêng cho rerank: giữ nguyên retrieval mode hybrid và các tham số top-k, chỉ bật/tắt rerank để đo tác động thật sự đến faithfulness. Tôi cũng muốn chuẩn hóa tokenization cho truy vấn kỹ thuật (mã lỗi, dấu gạch nối, viết tắt) để sparse retrieval ổn định hơn. Cuối cùng, tôi sẽ bổ sung alias metadata cho các tài liệu đổi tên nhằm giảm lỗi ở các câu hỏi dùng thuật ngữ cũ.
