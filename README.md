# HỆ THỐNG PHÁT HIỆN TẤN CÔNG WEB DEFACEMENT (HYBRID ML + ANOMALY DETECTION)

---

## 1. Giới thiệu sơ về đồ án

Đồ án này xây dựng một **hệ thống phát hiện tấn công Web Defacement** dựa trên phân tích log truy cập web, kết hợp **Machine Learning có giám sát (Hybrid ML)** và **Anomaly Detection (không giám sát)**.

Hệ thống mô phỏng một website đơn giản, sinh ra các loại traffic khác nhau (người dùng bình thường, hành vi nghi vấn, và tấn công deface), sau đó:

* Thu thập log truy cập
* Theo dõi tính toàn vẹn file website
* Trích xuất đặc trưng hành vi
* Xây dựng dataset
* Huấn luyện và đánh giá mô hình học máy

Mục tiêu của đồ án không chỉ là phân loại chính xác tấn công đã biết, mà còn **phát hiện sớm các hành vi bất thường** giống như các hệ thống IDS/IPS trong thực tế.

---

## 2. Mục tiêu & kiến trúc hệ thống

### 2.1. Mục tiêu

Đồ án hướng tới các mục tiêu chính sau:

* Mô phỏng kịch bản tấn công Web Defacement thực tế
* Phát hiện và phân loại các loại truy cập:

  * Normal (bình thường)
  * Suspicious (nghi vấn)
  * Deface (tấn công thay đổi nội dung website)
* Kết hợp **Hybrid Machine Learning** và **Anomaly Detection** trong cùng một pipeline
* Hiểu rõ ưu – nhược điểm của từng phương pháp trong bài toán an ninh mạng

### 2.2. Kiến trúc hệ thống

Hệ thống gồm các thành phần chính:

1. **Web Server mô phỏng (Flask)**

   * Phục vụ website đơn giản (`index.html`)
   * Hỗ trợ truy cập bình thường, truy vấn nghi vấn và upload nội dung deface

2. **Traffic Simulation**

   * `normal_traffic.py`: sinh traffic người dùng bình thường
   * `suspicious_chain.py`: sinh chuỗi hành vi nghi vấn (scan, query lạ)
   * `deface_attack.py`: mô phỏng tấn công deface

3. **File Integrity Monitoring**

   * Theo dõi thay đổi nội dung `index.html` bằng hash SHA-256
   * Ghi nhận sự kiện deface thực sự xảy ra

4. **Collector & Feature Engineering**

   * Parse access log
   * Trích xuất đặc trưng hành vi (entropy URL, rate, keyword, chain score…)
   * Gắn nhãn và xây dựng dataset hoàn chỉnh

5. **Hybrid Machine Learning (Supervised)**

   * Phân loại chính xác 3 lớp: normal / suspicious / deface

6. **Anomaly Detection (Unsupervised)**

   * Phân tích hành vi theo session (time-window)
   * Phát hiện các hành vi bất thường chưa được định nghĩa trước

---

## 3. Cách chạy đồ án

### Lưu ý: Cần xóa hết tất cả file trong folder 'data' trước khi thực hiện các bước chạy chương trình.

### Bước 1: Chạy File Integrity Monitor

Mở một terminal và chạy:

```bash
python collector/file_integrity_log.py
```

Chương trình sẽ theo dõi file `data/web/index.html` và ghi log khi có thay đổi.

---

### Bước 2: Chạy Web Server

Mở terminal khác:

```bash
python simulator/web_server.py
```

Web server sẽ chạy tại địa chỉ `http://127.0.0.1:5000`.

---

### Bước 3: Sinh traffic mô phỏng

Chạy lần lượt các file sau:

```bash
python attacker_sim/normal_traffic.py
python attacker_sim/suspicious_chain.py
python attacker_sim/deface_attack.py
```

Các script này sẽ tạo traffic bình thường, nghi vấn và tấn công deface.

---

### Bước 4: Xây dựng dataset

Chạy các bước xử lý dữ liệu:

```bash
python collector/log_parser.py
python collector/build_dataset.py
python collector/attack_chain_features.py
python collector/merge_integrity_feature.py
```

Sau bước này, dataset cuối cùng sẽ nằm trong thư mục `data/final/`.

---

### Bước 5: Huấn luyện & đánh giá mô hình

#### Hybrid Machine Learning (Supervised):

```bash
python ml/deface_ml_hybrid.py
```

#### Anomaly Detection (Session-based):

```bash
python ml/deface_anomaly_detection.py
```

---

## Ghi chú

* Hybrid ML cho kết quả phân loại rất cao khi có nhãn đầy đủ
* Anomaly Detection phản ánh đúng bản chất bài toán IDS (không thể đạt độ chính xác tuyệt đối)
* Hệ thống được thiết kế phục vụ mục đích học tập và nghiên cứu

---

**Kết luận:**

Đồ án đã xây dựng thành công một pipeline phát hiện Web Defacement hoàn chỉnh, kết hợp cả học máy có giám sát và không giám sát, phù hợp với các hệ thống an ninh mạng hiện đại.
