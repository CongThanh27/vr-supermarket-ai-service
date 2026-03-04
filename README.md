vr-supermarket-ai-service/
├── app/                        # THƯ MỤC LÕI
│   ├── api/                    # Tầng Interface: Nơi định nghĩa các API Endpoints
│   │   ├── routes/             
│   │   │   ├── analyze.py      # Router nhận dữ liệu hành vi từ Unity (VD: tọa độ, số lần chọn sai món)
│   │   │   └── dialogue.py     # Router sinh lời thoại cho NPC trong siêu thị
│   │   └── __init__.py         # Gom các router lại để khai báo gọn gàng trong main.py
│   ├── core/                   # Tầng Cấu hình hệ thống
│   │   ├── config.py           # Load và quản lý biến môi trường (Pydantic BaseSettings) cho DB_URL, MLFLOW_URI...
│   │   └── logger.py           
│   ├── db/                     # Tầng Data Access: Giao tiếp với Cơ sở dữ liệu 
│   │   ├── session.py          # Khởi tạo connection pool tới Database
│   │   └── crud.py             # Các hàm thao tác với DB (Create, Read, Update, Delete) để lưu trữ log chơi game của bệnh nhân
│   ├── models/                 # Tầng Schema: Khai báo cấu trúc dữ liệu
│   │   ├── schemas.py          # Pydantic models: Validate định dạng JSON gửi từ Unity qua (VD: bắt buộc phải có user_id, action_type...)
│   │   └── domain.py           # (Tùy chọn) SQLAlchemy models nếu dùng DB quan hệ để map với các bảng trong DB
│   ├── services/               # Tầng Business Logic: Nơi xử lý nghiệp vụ chính
│   │   ├── ai_logic.py         # Code phân tích: Nhận data từ routes -> gọi ML models hoặc rules -> tính toán điểm số 6 chức năng điều hành (Working Memory, Inhibition...)
│   │   └── __init__.py
│   ├── ml/                     # Tầng Model Serving: Tích hợp với MLflow
│   │   └── model_loader.py     # Script kết nối tới MLflow Registry để kéo phiên bản model 
│   └── main.py                 # File Entry-point: Khởi tạo app FastAPI, cấu hình CORS (cho phép Unity gọi API), và gắn các routers
├── ml_pipeline/                # THƯ MỤC NGHIÊN CỨU: 
│   ├── notebooks/              # Chứa các file Jupyter (.ipynb) để phân tích dữ liệu khám phá (EDA) từ log người chơi
│   ├── experiments/            # Chứa các file Python script (.py) dùng để train các mô hình phân loại (Classification), đánh giá mức độ suy giảm nhận thức
│   └── requirements_ml.txt     # Thư viện riêng cho việc train (scikit-learn, tensorflow/pytorch, pandas...), không cài vào server API cho nhẹ
├── tests/                      # THƯ MỤC KIỂM THỬ: Đảm bảo code không bị lỗi khi nâng cấp
│   ├── test_api.py             # Test các API endpoints xem có trả về đúng mã 200/400 không
│   └── test_services.py        # Test các hàm logic xử lý AI
├── .env.example                
├── .gitignore                  
├── requirements.txt            # Danh sách thư viện 
└── README.md                   

<!-- /usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload -->