# Báo Cáo Nhóm — Lab Day 08: RAG Pipeline

**Ngày nộp:** 13/04/2026  
**Nhóm:** C401_F3

---

## 1. Tổng quan Pipeline

Nhóm xây dựng hệ thống hỗ trợ tra cứu chính sách nhân sự (HR), quy trình vận hành (SOP) và hỗ trợ kỹ thuật (IT Helpdesk), sử dụng RAG pipeline tiêu chuẩn:

```
index.py (Sprint 1)          rag_answer.py (Sprint 2+3)        eval.py (Sprint 4)
┌──────────────────┐         ┌─────────────────────────┐        ┌────────────────────┐
│ Tài liệu .txt    │         │ Query                   │        │ 10 grading questions│
│       ↓          │         │   ↓                     │        │       ↓             │
│ preprocess_doc() │         │ retrieve_dense/hybrid()  │        │ run_scorecard()    │
│       ↓          │         │   ↓                     │        │   ↓                │
│ chunk_document() │         │ build_context_block()    │        │ LLM-as-Judge       │
│       ↓          │  ───→   │   ↓                     │  ───→  │ (4 metrics)        │
│ get_embedding()  │         │ build_grounded_prompt()  │        │   ↓                │
│       ↓          │         │   ↓                     │        │ compare_ab()       │
│ ChromaDB upsert  │         │ call_llm() → answer     │        │   ↓                │
└──────────────────┘         └─────────────────────────┘        │ scorecard + log    │
                                                                └────────────────────┘
```

---

## 2. Quyết định kỹ thuật chính

### 2.1. Chunking Strategy

| Tham số | Giá trị | Lý do |
|---------|---------|-------|
| Chunk size | 300 tokens | Phù hợp với các điều khoản ngắn trong chính sách và FAQ |
| Overlap | 50 tokens | Đảm bảo không mất ngữ cảnh tại các điểm cắt giữa đoạn |
| Split strategy | Section-based (`=== ... ===`) → paragraph split | Tận dụng cấu trúc tài liệu sẵn có để giữ tính toàn vẹn của thông tin |

### 2.2. Embedding Model

Sử dụng `text-embedding-3-small` (OpenAI). Lý do: Hiệu năng cao, kích thước vector nhỏ gọn (1536) giúp tối ưu tốc độ truy vấn trên ChromaDB và hỗ trợ đa ngôn ngữ tốt. Hơn nữa, các thành viên của nhóm có đăng ký OpenAI key nên việc sử dụng OpenAi sẽ thuận tiện hơn so với việc phải đăng ký nhiều dịch vụ LLM khác nhau.

### 2.3. Retrieval Config

| Config | Baseline | Variant |
|--------|----------|---------|
| `retrieval_mode` | `dense` | `hybrid` |
| `top_k_search` | 10 | 15 |
| `top_k_select` | 3 | 5 |
| `use_rerank` | `false` | `true` |
| LLM | `gpt-4o` | `gpt-4o` |

**Biến thay đổi chính:** Chuyển từ `dense` sang `hybrid`.

**Lưu ý A/B rule:** Trong quy trình tuning, nhóm ưu tiên đọc kết quả theo từng vòng thử nghiệm một biến. Việc tăng `top_k` và bật `rerank` được xem là bước mở rộng sau khi đã xác nhận hướng cải thiện của retrieval mode.

**Lý do chọn hybrid & rerank:** Qua quan sát baseline, dense retrieval gặp khó khăn với các từ khóa đặc thù như mã lỗi (ERR-403) hoặc các thực thể viết tắt. Hybrid giúp cân bằng giữa ngữ nghĩa và từ khóa chính xác. Rerank (Cross-Encoder) được thêm vào để lọc lại 5 chunk tốt nhất từ 15 candidate, đảm bảo context đưa vào prompt có độ liên quan cao nhất.

### 2.4. Grounded Prompt Design

Prompt được thiết kế với các constraint sau đây

1. **Evidence-only** — Tuyệt đối không sử dụng kiến thức bên ngoài (ví dụ như nhiều LLM có thể gọi tool search web)
2. **Abstain** — Trả lời rõ ràng "Tôi không có đủ thông tin" hoặc "tôi không biết" nếu context không chứa đáp án. Tuyệt đối không tự bịa ra thông tin.
3. **Citation** — Yêu cầu trích dẫn nguồn theo format `[Nguồn]`.
4. **Versioning** — Hướng dẫn so sánh giữa các phiên bản tài liệu.
5. **Completeness** — Đảm bảo liệt kê đầy đủ các con số, điều kiện và ngoại lệ.
6. **Multi-hop** — Khuyến khích tổng hợp thông tin từ nhiều chunk/tài liệu khác nhau.

---

## 3. Kết quả Evaluation

### 3.1. Scorecard Summary

| Metric | Baseline (dense) | Variant (hybrid+rerank) | Delta |
|--------|----------------:|----------------:|------:|
| Faithfulness | 4.20/5 | 4.60/5 | +0.40 |
| Relevance | 4.60/5 | 4.60/5 | 0.00 |
| Context Recall | 5.00/5 | 5.00/5 | 0.00 |
| Completeness | 3.90/5 | 3.90/5 | 0.00 |

Chỉ có điểm delta faithfulness là thay đổi.

### 3.2. Nhận xét A/B

- **Faithfulness cải thiện đáng kể (+0.40)**: Việc sử dụng Hybrid retrieval và Rerank giúp loại bỏ các chunk "nhiễu", dẫn đến việc model ít bị nhầm lẫn và giảm thiểu hiện tượng ảo giác (hallucination).
- **Context Recall giữ vững 5.00**: Cả hai chiến lược đều truy xuất được đầy đủ các nguồn tài liệu cần thiết.
- **Completeness không đổi**: Điểm số này vẫn thấp do model đôi khi tóm tắt quá ngắn gọn hoặc bỏ lỡ một vài chi tiết phụ trong các câu hỏi đa ý (multi-part questions). Hơn nữa, với câu hỏi không có câu trả lời (như trong trường hợp câu hỏi Abstain, điểm completeness không được tính vào số điểm cuối cùng)

### 3.3. Grading Questions — Kết quả nổi bật

| ID | Kết quả | Nhận xét |
|----|---------|----------|
| gq01 | ✅ Full | Nhận diện đúng sự thay đổi SLA từ 6h xuống 4h dựa trên Effective Date. |
| gq05 | ✅ Cải thiện | Variant trả lời đúng về quyền của Contractor nhờ lấy được thông tin scope ở Section 1. |
| gq06 | ✅ Khó | Tổng hợp thành công thông tin khẩn cấp từ 2 tài liệu khác nhau (SOP + SLA). |
| gq07 | ⚠️ Abstain | Model trả lời "Tôi không biết" - đúng về mặt Faithfulness nhưng cho thấy dữ liệu thiếu context. Hơn nữa, model chưa thông báo với người dùng về việc liên hệ với các bên liên quan để tìm thêm thông tin|
| gq08 | ✅ Full | Phân biệt tốt hai ngữ cảnh khác nhau của con số "3 ngày" (nghỉ phép vs nghỉ ốm). |

---

## 4. Phân vai trong nhóm

| Vai trò | Thành viên | Sprint chính | Công việc cụ thể |
|---------|-----------|-------------|-------------------|
| **Retrieval Owner** | Hoàng Quốc Hùng | Sprint 1, 3 | Tối ưu chunking/metadata, triển khai dense-sparse-hybrid retrieval, phối hợp rerank và phân tích failure mode theo scorecard. |
| **Documentation Owner** | Khương Hải Lâm | Sprint 3, 4 | Ghi Tuning Log, thực hiện AB testing, tối ưu Prompt Engineering và viết báo cáo. |

Đóng góp Retrieval Owner tập trung vào 3 điểm: (1) đảm bảo chunk đủ ngữ cảnh và metadata dùng được cho citation/debug, (2) chọn chiến lược retrieval phù hợp với truy vấn có mã lỗi/alias, (3) truy vết lỗi theo Error Tree để tách bạch lỗi retrieval với lỗi generation.

---

## 5. Bài học rút ra

### 5.1. Tầm quan trọng của Retrieval chất lượng
Dù LLM rất thông minh (gpt-4o), nhưng nếu Retrieval không mang về đúng mảnh ghép thông tin (như trường hợp gq05 ở baseline), model sẽ không thể trả lời đúng. Hybrid retrieval là công cụ mạnh cho các tài liệu có nhiều mã lỗi và thuật ngữ kỹ thuật.

### 5.2. Trade-off trong Prompt Engineering
Việc thiết lập prompt quá strict giúp tăng Faithfulness (giảm ảo giác) nhưng đôi khi làm giảm Completeness vì model trở nên quá thận trọng, không dám khẳng định các thông tin mang tính suy luận nhẹ từ context.

### 5.3. Evaluation tự động là cần thiết
Nếu không có bộ scorecard và metrics rõ ràng, nhóm sẽ rất dễ bị lạc giữa hàng tá tham số (chunk size, top_k, weight). Việc nhìn vào điểm số cụ thể giúp nhóm tập trung fix đúng "nút thắt cổ chai" của hệ thống. Hơn nữa, đây chỉ là bộ câu hỏi mock với 10 câu hỏi. Trên thực tế, bộ câu hỏi Eval có thể được thiết kế với số lượng lớn bao hàm nhiều trường hợp khác nhau, việc xây dựng một khung evaluation tự động là việc làm cần thiết. 

Việc đưa ra Evaluation cũng giúp nhà phát triển có cái nhìn định lượng, tránh việc đưa ra đánh giá cảm quan.

---