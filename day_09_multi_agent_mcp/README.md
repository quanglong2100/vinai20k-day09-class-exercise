# Ngày 9 — Đa Tác Tử & MCP/A2A

**Chương 2 | Ngày 9 trong 15**

---

## Mục tiêu

Xây dựng hệ thống đa tác tử với Supervisor định tuyến nhiệm vụ đến các Worker agent chuyên biệt. Kết nối công cụ bên ngoài qua MCP server mock. Theo dõi giao tiếp giữa các agent.

---

## Bối Cảnh

### Mô Hình Đa Tác Tử

```
User → SupervisorAgent
           ↓
    [route task to best worker]
           ↓
    WorkerAgent (Research | Writer | Analyst | ...)
           ↓
    [aggregate results]
           ↓
       SupervisorAgent → User
```

### MCP (Model Context Protocol)
MCP là giao thức cho phép AI agent truy cập an toàn vào công cụ và nguồn dữ liệu bên ngoài. Hãy coi nó như hệ thống plugin tiêu chuẩn hóa dành cho AI.

### A2A (Agent-to-Agent)
Giao tiếp trực tiếp giữa các agent sử dụng tin nhắn có cấu trúc.

---

## Nhiệm Vụ

### Nhiệm vụ 1: dataclass `AgentMessage`
Tin nhắn có cấu trúc được truyền giữa các agent.

### Nhiệm vụ 2: `WorkerAgent`
Agent chuyên biệt với lĩnh vực được xác định (specialty). Xử lý `AgentMessage` và trả về `AgentMessage` phản hồi.

### Nhiệm vụ 3: `SupervisorAgent`
Định tuyến nhiệm vụ đến các worker, tổng hợp kết quả, xây dựng trace đầy đủ của toàn bộ giao tiếp giữa các agent.

### Nhiệm vụ 4: `MCPServer` và `MCPClient`
Triển khai mock giao thức MCP để đăng ký và gọi công cụ.

---

## Sản phẩm nộp bài

1. `solution/solution.py` — tất cả các triển khai
2. Hệ thống đa tác tử với 3 worker (Research, Writing, Analysis) chạy 3 nhiệm vụ
3. In trace giao tiếp đầy đủ giữa các agent cho mỗi nhiệm vụ

---

## Chạy kiểm thử

```bash
pytest tests/ -v
```

---

## Hướng dẫn thời gian lab

| Hoạt động | Thời gian | Mô tả |
|-----------|-----------|-------|
| Khởi động | 0:00–0:20 | Đọc `exercises.md` Phần 1 — phác thảo kiến trúc, so sánh các mô hình |
| Lập trình cốt lõi | 0:20–1:20 | Triển khai tất cả TODO trong `template.py` |
| Mở rộng | 1:20–2:20 | Hệ thống domain, so sánh pipeline vs. supervisor, các công cụ MCP |
| Suy ngẫm | 2:20–2:50 | Sơ đồ kiến trúc ASCII + đoạn văn so sánh trong `reflection.md` |
| Dự phòng / Kiểm tra | 2:50–3:00 | Chạy `pytest tests/ -v` lần cuối, dọn dẹp code |

---

## Chấm điểm

| Tiêu chí | Điểm |
|----------|------|
| Tất cả kiểm thử pytest đều pass | 60 |
| Trace chứa toàn bộ lịch sử tin nhắn giữa các agent | 20 |
| Công cụ MCP có thể truy cập từ bên trong WorkerAgent | 10 |
| Chất lượng code và type hints | 10 |
| **Tổng** | **100** |

---

## Danh sách kiểm tra nộp bài

- [ ] `solution/solution.py` — tất cả các triển khai hoàn chỉnh
- [ ] `pytest tests/ -v` — tất cả kiểm thử đều pass (bao gồm kiểm thử mới)
- [ ] `exercises.md` — phác thảo kiến trúc, tất cả bảng, code MCP đã dán vào
- [ ] `reflection.md` — sơ đồ ASCII + đoạn văn so sánh monolithic vs. đa tác tử
- [ ] `PipelineAgent` đã triển khai và kiểm thử
- [ ] `SupervisorAgent.get_worker_stats` đã triển khai và kiểm thử
