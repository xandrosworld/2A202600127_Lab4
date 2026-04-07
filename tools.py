from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ============================================================

FLIGHTS_DB: dict[tuple[str, str], list[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",      "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "07:30", "arrival": "09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "13:00", "arrival": "14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "15:00", "arrival": "16:00", "price": 650_000,   "class": "economy"},
    ],
}

HOTELS_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",   "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",    "rating": 4.5},
        {"name": "Sala Danang Beach",    "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",    "rating": 4.3},
        {"name": "Fivitel Danang",       "stars": 3, "price_per_night": 650_000,   "area": "Sơn Trà",   "rating": 4.1},
        {"name": "Memory Hostel",        "stars": 2, "price_per_night": 250_000,   "area": "Hải Châu",  "rating": 4.6},
        {"name": "Christina's Homestay","stars": 2, "price_per_night": 350_000,   "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",  "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",    "rating": 4.4},
        {"name": "Sol by Meliá",    "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort",   "stars": 3, "price_per_night": 800_000,   "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000,   "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",        "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central",  "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000,   "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room",  "stars": 2, "price_per_night": 180_000,   "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        # Tra cứu FLIGHTS_DB với key (origin, destination)
        flights = FLIGHTS_DB.get((origin, destination))

        # Nếu không tìm thấy, thử tra ngược chiều (destination, origin)
        if not flights:
            flights = FLIGHTS_DB.get((destination, origin))

        # Nếu vẫn không có → thông báo rõ ràng
        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        # Format danh sách chuyến bay dễ đọc, giá tiền có dấu chấm phân cách
        result = f"Chuyến bay từ {origin} đến {destination}:\n"
        for i, f in enumerate(flights, 1):
            price_fmt = f"{f['price']:,}".replace(",", ".")
            result += (
                f"  {i}. {f['airline']} | {f['departure']} -> {f['arrival']} | "
                f"{price_fmt}d | {f['class']}\n"
            )
        return result.strip()

    except Exception as e:
        return f"Lỗi khi tìm chuyến bay: {str(e)}. Vui lòng thử lại."


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        hotels = HOTELS_DB.get(city)

        if not hotels:
            return (
                f"Không tìm thấy khách sạn tại {city}. "
                f"Hệ thống hiện hỗ trợ: Đà Nẵng, Phú Quốc, Hồ Chí Minh."
            )

        # Lọc theo max_price_per_night
        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

        if not filtered:
            budget_fmt = f"{max_price_per_night:,}".replace(",", ".")
            return (
                f"Không tìm thấy khách sạn tại {city} với giá dưới {budget_fmt}d/đêm. "
                f"Hãy thử tăng ngân sách!"
            )

        # Sắp xếp theo rating giảm dần
        filtered.sort(key=lambda h: h["rating"], reverse=True)

        result = f"Khách sạn tại {city}:\n"
        for i, h in enumerate(filtered, 1):
            price_fmt = f"{h['price_per_night']:,}".replace(",", ".")
            stars_str = "*" * h["stars"]
            result += (
                f"  {i}. [{stars_str}] {h['name']} | {h['area']} | "
                f"{price_fmt}d/dem | Rating: {h['rating']}/5\n"
            )
        return result.strip()

    except Exception as e:
        return f"Lỗi khi tìm khách sạn: {str(e)}. Vui lòng thử lại."


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_dict: dict[str, int] = {}
        for item in expenses.split(","):
            item = item.strip()
            if ":" not in item:
                continue
            name, amount_str = item.split(":", 1)
            expense_dict[name.strip()] = int(amount_str.strip())

        # Tính tổng chi phí
        total_expense: int = sum(expense_dict.values())

        # Tính số tiền còn lại
        remaining: int = total_budget - total_expense

        # Format bảng chi tiết
        budget_fmt = f"{total_budget:,}".replace(",", ".")
        result = f"Ngan sach: {budget_fmt}d\n"
        result += "-" * 35 + "\n"
        result += "Bang chi phi:\n"
        for name, amount in expense_dict.items():
            amount_fmt = f"{amount:,}".replace(",", ".")
            display_name = name.replace("_", " ").title()
            result += f"  - {display_name}: {amount_fmt}d\n"

        total_fmt = f"{total_expense:,}".replace(",", ".")
        result += "-" * 35 + "\n"
        result += f"Tong chi: {total_fmt}d\n"

        if remaining >= 0:
            remaining_fmt = f"{remaining:,}".replace(",", ".")
            result += f"Con lai: {remaining_fmt}d"
        else:
            over_fmt = f"{abs(remaining):,}".replace(",", ".")
            result += f"VUOT NGAN SACH: {over_fmt}d! Can dieu chinh lai."

        return result

    except Exception as e:
        return (
            f"Lỗi khi tính ngân sách: {str(e)}. "
            f"Vui lòng kiểm tra định dạng (VD: 've_may_bay:1000000,khach_san:500000')."
        )


# ============================================================
# WEATHER_DB — Dữ liệu thời tiết theo tháng cho từng thành phố
# ============================================================

WEATHER_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {"months": [1, 2, 12], "condition": "Mưa nhiều, trời lạnh",        "temp_min": 18, "temp_max": 23, "recommend": "Mang áo ấm, áo mưa. Tránh các hoạt động biển."},
        {"months": [3, 4, 5],  "condition": "Nắng đẹp, ít mưa",            "temp_min": 24, "temp_max": 32, "recommend": "Thời điểm lý tưởng để đi biển và tham quan."},
        {"months": [6, 7, 8],  "condition": "Nắng nóng, đôi khi có giông", "temp_min": 27, "temp_max": 36, "recommend": "Tắm biển sáng sớm, tránh nắng trưa. Mang kem chống nắng."},
        {"months": [9, 10, 11],"condition": "Mưa bão mùa thu",             "temp_min": 22, "temp_max": 28, "recommend": "Theo dõi dự báo thời tiết. Có thể có bão lớn tháng 10-11."},
    ],
    "Phú Quốc": [
        {"months": [11, 12, 1, 2, 3, 4], "condition": "Khô ráo, nắng đẹp, biển trong xanh", "temp_min": 25, "temp_max": 33, "recommend": "Mùa đỉnh cao — thời tiết hoàn hảo để tắm biển và lặn san hô."},
        {"months": [5, 6, 7, 8, 9, 10],  "condition": "Mùa mưa, biển động",                 "temp_min": 24, "temp_max": 31, "recommend": "Khách sạn rẻ hơn nhưng biển thường đục, sóng to. Phù hợp khám phá nội địa."},
    ],
    "Hồ Chí Minh": [
        {"months": [12, 1, 2, 3, 4], "condition": "Mùa khô, ít mưa, nắng nhiều", "temp_min": 24, "temp_max": 35, "recommend": "Thời điểm tốt nhất để tham quan thành phố. Mang kính mát, kem chống nắng."},
        {"months": [5, 6, 7, 8, 9, 10, 11], "condition": "Mùa mưa, mưa chiều thường xuyên", "temp_min": 24, "temp_max": 33, "recommend": "Mang ô/áo mưa. Mưa thường chỉ 1-2 tiếng buổi chiều, buổi sáng vẫn đẹp."},
    ],
    "Hà Nội": [
        {"months": [10, 11, 12, 1, 2], "condition": "Mùa đông, se lạnh, hanh khô",      "temp_min": 13, "temp_max": 21, "recommend": "Mang áo khoác. Tháng 12-1 là mùa đông lạnh nhất."},
        {"months": [3, 4],             "condition": "Xuân, mưa phùn, ẩm ướt",           "temp_min": 17, "temp_max": 24, "recommend": "Tiết xuân dễ chịu, nên thăm các lễ hội truyền thống."},
        {"months": [5, 6, 7, 8, 9],   "condition": "Mùa hè, nắng nóng oi bức, mưa rào","temp_min": 26, "temp_max": 38, "recommend": "Hè Hà Nội rất nóng. Nên tham quan sáng sớm hoặc chiều mát."},
    ],
}

# ============================================================
# ACTIVITIES_DB — Hoạt động & địa điểm tham quan tại từng thành phố
# ============================================================

ACTIVITIES_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {"name": "Bãi biển Mỹ Khê",        "category": "thiên nhiên",  "price": 0,          "duration": "Cả ngày", "description": "Bãi biển đẹp nhất Đà Nẵng, nước trong xanh, cát trắng mịn."},
        {"name": "Cầu Rồng",               "category": "văn hóa",     "price": 0,          "duration": "1-2 tiếng", "description": "Cây cầu biểu tượng phun lửa & nước vào tối cuối tuần."},
        {"name": "Bán đảo Sơn Trà",        "category": "thiên nhiên",  "price": 0,          "duration": "Nửa ngày", "description": "Ngắm toàn cảnh Đà Nẵng, gặp đàn khỉ hoang dã, chụp ảnh đẹp."},
        {"name": "Phố cổ Hội An",          "category": "văn hóa",     "price": 120_000,    "duration": "Cả ngày",  "description": "Cách Đà Nẵng 30km, phố cổ lung linh về đêm với đèn lồng."},
        {"name": "Ba Na Hills",            "category": "vui chơi",    "price": 750_000,    "duration": "Cả ngày",  "description": "Khu du lịch trên núi, cầu Vàng nổi tiếng thế giới, cáp treo dài nhất."},
        {"name": "Ăn hải sản Mỹ Khê",     "category": "ẩm thực",     "price": 200_000,    "duration": "1-2 tiếng", "description": "Tôm hùm, mực nướng, cá biển tươi sống ngay bờ biển."},
        {"name": "Chợ Hàn",               "category": "ẩm thực",     "price": 50_000,     "duration": "1-2 tiếng", "description": "Chợ truyền thống, thử bánh mì, mì Quảng, bún chả cá."},
    ],
    "Phú Quốc": [
        {"name": "Lặn ngắm san hô",        "category": "thiên nhiên",  "price": 350_000,    "duration": "Nửa ngày", "description": "Lặn scuba hoặc snorkeling tại Hòn Thơm, san hô đa dạng."},
        {"name": "Bãi Sao",               "category": "thiên nhiên",  "price": 0,          "duration": "Cả ngày",  "description": "Bãi biển đẹp nhất Phú Quốc, nước trong vắt như pha lê."},
        {"name": "VinWonders Phú Quốc",   "category": "vui chơi",    "price": 600_000,    "duration": "Cả ngày",  "description": "Công viên giải trí lớn nhất ĐNA: roller coaster, show nhạc nước."},
        {"name": "Chợ đêm Dương Đông",    "category": "ẩm thực",     "price": 100_000,    "duration": "2-3 tiếng","description": "Ghẹ, nhum biển nướng, gỏi cá trích, nước mắm Phú Quốc nổi tiếng."},
        {"name": "Câu cá & ngắm hoàng hôn","category": "thiên nhiên", "price": 200_000,    "duration": "Nửa ngày", "description": "Tour câu cá kết hợp ngắm hoàng hôn, bia lạnh trên biển."},
        {"name": "Nhà tù Phú Quốc",       "category": "văn hóa",     "price": 20_000,     "duration": "1-2 tiếng","description": "Di tích lịch sử thời chiến tranh, hiểu thêm về lịch sử VN."},
    ],
    "Hồ Chí Minh": [
        {"name": "Dinh Độc Lập",          "category": "văn hóa",     "price": 40_000,     "duration": "1-2 tiếng","description": "Di tích lịch sử quan trọng, tham quan hầm ngầm và phòng họp thời chiến."},
        {"name": "Bảo tàng Chứng tích Chiến tranh","category": "văn hóa", "price": 40_000, "duration": "2-3 tiếng","description": "Bảo tàng ghi lại lịch sử chiến tranh VN, nhiều hiện vật quý giá."},
        {"name": "Phố đi bộ Nguyễn Huệ", "category": "văn hóa",     "price": 0,          "duration": "2-3 tiếng","description": "Trung tâm thành phố, cafe bệt, biểu diễn nghệ thuật đường phố về đêm."},
        {"name": "Cù Lao Thới Sơn",      "category": "thiên nhiên",  "price": 150_000,    "duration": "Cả ngày",  "description": "Tour miền Tây 1 ngày: chèo xuồng, thăm vườn trái cây, ăn cơm dừa."},
        {"name": "Phố Tây Bùi Viện",     "category": "vui chơi",    "price": 100_000,    "duration": "Buổi tối", "description": "Phố bar sầm uất nhất SG, gặp gỡ khách Tây, uống bia hơi."},
        {"name": "Bánh mì Huỳnh Hoa",    "category": "ẩm thực",     "price": 50_000,     "duration": "30 phút",  "description": "Bánh mì nổi tiếng nhất SG, luôn có hàng dài nhưng xứng đáng chờ."},
    ],
}


@tool
def get_weather(city: str, month: int) -> str:
    """
    Xem thông tin thời tiết tại một thành phố theo tháng.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh', 'Hà Nội')
    - month: tháng trong năm (1-12)
    Trả về điều kiện thời tiết, nhiệt độ và lời khuyên phù hợp.
    """
    try:
        if month < 1 or month > 12:
            return "Tháng không hợp lệ. Vui lòng nhập từ 1 đến 12."

        weather_list = WEATHER_DB.get(city)
        if not weather_list:
            supported = ", ".join(WEATHER_DB.keys())
            return f"Chưa có dữ liệu thời tiết cho {city}. Hỗ trợ: {supported}."

        # Tìm bản ghi thời tiết phù hợp với tháng
        for w in weather_list:
            if month in w["months"]:
                return (
                    f"Thoi tiet tai {city} thang {month}:\n"
                    f"  Tinh trang: {w['condition']}\n"
                    f"  Nhiet do: {w['temp_min']}-{w['temp_max']}°C\n"
                    f"  Loi khuyen: {w['recommend']}"
                )

        return f"Không tìm thấy dữ liệu thời tiết cho {city} tháng {month}."

    except Exception as e:
        return f"Lỗi khi tra cứu thời tiết: {str(e)}. Vui lòng thử lại."


@tool
def search_activities(city: str, category: str = "") -> str:
    """
    Tìm kiếm các hoạt động và địa điểm tham quan tại một thành phố.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - category: loại hoạt động để lọc — 'thiên nhiên', 'văn hóa', 'vui chơi', 'ẩm thực'.
      Để trống để xem tất cả.
    Trả về danh sách hoạt động với mô tả, thời gian và chi phí ước tính.
    """
    try:
        activities = ACTIVITIES_DB.get(city)
        if not activities:
            supported = ", ".join(ACTIVITIES_DB.keys())
            return f"Chưa có dữ liệu hoạt động cho {city}. Hỗ trợ: {supported}."

        # Lọc theo category nếu có
        if category:
            filtered = [a for a in activities if a["category"] == category.lower().strip()]
            if not filtered:
                available = list({a["category"] for a in activities})
                return (
                    f"Không tìm thấy hoạt động loại '{category}' tại {city}. "
                    f"Các loại có sẵn: {', '.join(available)}."
                )
        else:
            filtered = activities

        result = f"Hoat dong & dia diem tai {city}:\n"
        for i, a in enumerate(filtered, 1):
            price_str = "Mien phi" if a["price"] == 0 else f"{a['price']:,}d".replace(",", ".")
            result += (
                f"  {i}. [{a['category'].upper()}] {a['name']}\n"
                f"     - Mo ta: {a['description']}\n"
                f"     - Thoi gian: {a['duration']} | Chi phi: {price_str}\n"
            )
        return result.strip()

    except Exception as e:
        return f"Lỗi khi tìm hoạt động: {str(e)}. Vui lòng thử lại."
