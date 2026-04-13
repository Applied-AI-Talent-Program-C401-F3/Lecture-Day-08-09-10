# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Lương Trung Kiên  
**Vai trò trong nhóm:**  Eval Owner
**Ngày nộp:** 13/04/2026  
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

> Mô tả cụ thể phần bạn đóng góp vào pipeline:
> - Em làm sprint 4.
> - Hoàn thành file eval.py, quyết định chọn variant 
> - Là phần hoàn thành của pipeline RAG.

_________________

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)
> Sau khi hoàn thành lab, tôi hiểu rõ hơn về cách hoạt động của pipeline RAG, đặc biệt là hai khái niệm chunking và retrieval. Trước đây, tôi nghĩ chỉ cần đưa toàn bộ tài liệu vào model là đủ, nhưng thực tế việc chia nhỏ văn bản (chunking) ảnh hưởng rất lớn đến chất lượng truy xuất. Nếu chunk quá lớn, thông tin sẽ bị loãng; nếu quá nhỏ, ngữ cảnh bị mất. Ngoài ra, tôi cũng hiểu rõ hơn sự khác biệt giữa sparse retrieval (BM25) và dense retrieval (embedding), và vì sao nên kết hợp cả hai để tận dụng ưu điểm của từng phương pháp. Nhờ đó, tôi thấy pipeline RAG không chỉ là “gọi model”, mà là một hệ thống cần thiết kế cẩn thận để đảm bảo câu trả lời chính xác.
> Evaluation loop giúp ta đánh giá được kĩ lưỡng các khía cạnh khác nhau của các chiến lược, từ đó giúp ta chọn được các chiến lược phù hợp cho từng bài toán.

_________________

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

> Điều khiến tôi bất ngờ là pipeline hoạt động không tốt ngay từ lần chạy đầu tiên, dù code không có lỗi rõ ràng. Kết quả retrieval đôi khi trả về các đoạn không liên quan, khiến câu trả lời của model bị sai hoặc thiếu chính xác. Ban đầu, tôi nghĩ vấn đề nằm ở model, nhưng sau khi kiểm tra kỹ, tôi nhận ra nguyên nhân chính là do cách chunking và truy vấn chưa phù hợp. Lỗi mất nhiều thời gian debug nhất là việc truy xuất không đúng ngữ cảnh, đặc biệt khi query chứa từ khóa hiếm hoặc dạng viết khác. Tôi cũng nhận ra rằng việc đánh giá (evaluation) pipeline quan trọng không kém việc xây dựng nó, vì nếu không kiểm tra kỹ, rất khó phát hiện lỗi tiềm ẩn.

_________________

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)


**Câu hỏi:** 
>[gq07] Công ty sẽ phạt bao nhiêu nếu team IT vi phạm cam kết SLA P1?
>Answer: Tôi không biết....
>Faithful: 1 | Relevant: 1 | Recall: None | Complete: 1

**Phân tích:**
>Với câu hỏi [gq07] “Công ty sẽ phạt bao nhiêu nếu team IT vi phạm cam kết SLA P1?”, cả baseline và variant đều trả lời “Tôi không biết”, với các chỉ số Faithful = 1, Relevant = 1, Complete = 1, nhưng Recall = None. Điều này cho thấy hệ thống đã xử lý đúng theo hướng “không bịa thông tin” (faithful), tuy nhiên lại không truy xuất được dữ liệu cần thiết để trả lời câu hỏi. Nguyên nhân chính nhiều khả năng nằm ở retrieval, không phải generation. Model đã hành xử đúng khi không thấy thông tin liên quan trong context. Việc Recall = None cho thấy pipeline không tìm được chunk nào chứa thông tin về mức phạt SLA P1, có thể do dữ liệu chưa được index đầy đủ, chunking làm mất thông tin quan trọng, hoặc truy vấn chưa match với cách diễn đạt trong tài liệu (ví dụ khác cách gọi “phạt”, “penalty”, “SLA violation”). Variant không cải thiện so với baseline, chứng tỏ thay đổi (có thể ở retrieval strategy hoặc prompt) chưa giải quyết đúng vấn đề cốt lõi. Để cải thiện, cần tập trung vào việc tối ưu retrieval, ví dụ: mở rộng query (query rewriting), cải thiện chunking, hoặc bổ sung hybrid search để tăng khả năng recall.
_________________

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Nếu có thêm thời gian, tôi sẽ thử cải thiện chiến lược chunking bằng cách chuyển từ fixed-size sang semantic chunking, vì kết quả evaluation cho thấy nhiều đoạn được retrieve chưa giữ được ngữ cảnh hoàn chỉnh. Ngoài ra, tôi cũng muốn thử hybrid retrieval (kết hợp BM25 và embedding) một cách có trọng số thay vì đơn giản ghép kết quả, vì hiện tại một số query chứa từ khóa quan trọng vẫn chưa được ưu tiên đúng mức. Những cải tiến này kỳ vọng sẽ giúp tăng độ chính xác của câu trả lời.
_________________
