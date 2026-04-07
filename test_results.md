# Test Results — TravelBuddy Agent

> Kết quả chạy 5 test cases theo yêu cầu Lab 4

---

## Test 1 — Direct Answer (Không cần tool)

**Input:**
```
Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
```

**Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

**Kết quả thực tế:**
```
Xin chào! Rất vui được hỗ trợ bạn lên kế hoạch du lịch! 😊

Để mình tư vấn cho bạn phù hợp nhất, bạn cho mình biết thêm một vài thông tin nhé:

1. **Bạn xuất phát từ đâu?** (VD: Hà Nội, Hồ Chí Minh, Đà Nẵng...)

2. **Ngân sách dự kiến?** (Khoảng bao nhiêu triệu cho cả chuyến đi?)

3. **Thời gian đi?** 
   - Dự định đi vào tháng nào?
   - Đi mấy ngày/mấy đêm?

4. **Bạn thích loại hình du lịch nào?**
   - Biển đảo thư giãn (Phú Quốc, Nha Trang, Đà Nẵng...)
   - Văn hóa lịch sử (Hội An, Huế, Hà Nội...)
   - Thiên nhiên, khám phá (Đà Lạt, Sapa, Ninh Bình...)
   - Ẩm thực, sống ảo (Sài Gòn, Hội An...)

Với thông tin này, mình sẽ gợi ý cho bạn những điểm đến phù hợp kèm chi phí cụ thể luôn nhé! 🌟
```

---

## Test 2 — Single Tool Call

**Input:**
```
Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
```

**Kỳ vọng:** Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.

**Kết quả thực tế:**
```
Mình tìm được các chuyến bay từ Hà Nội đi Đà Nẵng cho bạn nè! ✈️

**Các chuyến bay hiện có:**

1. **VietJet Air** - 08:30 → 09:50 
   - Giá: **890.000đ** (economy)
   - ✨ Giá tốt nhất, bay buổi sáng rất tiện

2. **Bamboo Airways** - 11:00 → 12:20
   - Giá: **1.200.000đ** (economy)
   - Bay trưa, phù hợp nếu muốn khởi hành muộn hơn

3. **Vietnam Airlines** - 06:00 → 07:20
   - Giá: **1.450.000đ** (economy)
   - Bay sớm nhất, đến nơi sớm tận dụng cả ngày

4. **Vietnam Airlines** - 14:00 → 15:20
   - Giá: **2.800.000đ** (business)
   - Hạng thương gia nếu muốn trải nghiệm cao cấp

---

**Gợi ý của mình:** Nếu muốn tiết kiệm thì chọn **VietJet** chỉ 890k, còn nếu quan trọng thương hiệu và dịch vụ thì **Vietnam Airlines** chuyến sáng sớm cũng ổn lắm!

Bạn dự định đi Đà Nẵng bao nhiêu ngày và ngân sách khoảng bao nhiêu vậy? Mình có thể gợi ý thêm khách sạn và lịch trình tham quan phù hợp luôn nè! 😊
```

---

## Test 3 — Multi-Step Tool Chaining

**Input:**
```
Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
```

**Kỳ vọng:** Gọi search_flights → search_hotels → calculate_budget, tổng hợp thành gợi ý hoàn chỉnh.

**Kết quả thực tế:**
```
Tuyệt vời! Mình đã tìm được thông tin cho chuyến đi Phú Quốc 2 đêm của bạn. Để tối ưu ngân sách 5 triệu, mình có **2 phương án** phù hợp:

## 🌟 PHƯƠNG ÁN 1: TIẾT KIỆM & LINH HOẠT

✈️ **Chuyến bay khứ hồi:**
- VietJet Air 16:00 → 18:15 | 1.100.000đ x 2 = **2.200.000đ**
- Bay chiều tối tiết kiệm hơn, vẫn kịp check-in khách sạn

🏨 **Khách sạn:**
- **9Station Hostel** [⭐⭐] - Dương Đông
- Giá: 200.000đ/đêm x 2 = **400.000đ**
- Rating: 4.5/5 (hostel sạch sẽ, tiện nghi tốt, ngay trung tâm)

💰 **Tổng chi phí:**
- Vé máy bay: 2.200.000đ
- Khách sạn (2 đêm): 400.000đ
- **Tổng cơ bản: 2.600.000đ**
- **Còn lại cho ăn uống + vui chơi: 2.400.000đ** 🎉

---

## 🏖️ PHƯƠNG ÁN 2: NÂNG CẤP NGHỈ DƯỠNG

✈️ **Chuyến bay khứ hồi:**
- VietJet Air 10:00 → 12:15 | 1.350.000đ x 2 = **2.700.000đ**
- Bay sáng có thêm nửa ngày khám phá

🏨 **Khách sạn:**
- **Lahana Resort** [⭐⭐⭐] - Dương Đông
- Giá: 800.000đ/đêm x 2 = **1.600.000đ**
- Rating: 4.0/5 (resort 3 sao có hồ bơi, gần biển)

💰 **Tổng chi phí:**
- Vé máy bay: 2.700.000đ
- Khách sạn (2 đêm): 1.600.000đ
- **Tổng cơ bản: 4.300.000đ**
- **Còn lại cho ăn uống + vui chơi: 700.000đ**

---

## 📋 GỢI Ý LỊCH TRÌNH & CHI PHÍ THAM KHẢO

**Ngày 1:** 
- Chiều tới → Check-in → Chợ đêm Dương Đông (~100.000đ)

**Ngày 2:**
- Sáng: Bãi Sao (miễn phí - bãi biển đẹp nhất!)
- Chiều: Lặn ngắm san hô Hòn Thơm (~350.000đ)
- Tối: Ăn hải sản địa phương (~200.000đ)

**Ngày 3:**
- Sáng: Câu cá & ngắm hoàng hôn (~200.000đ) HOẶC Nhà tù Phú Quốc (~20.000đ)
- Chiều: Bay về

---

## 💡 MẸO TỪ MÌNH:

✅ **Khuyến nghị:** Chọn phương án 1 để có budget thoải mái ăn uống (hải sản Phú Quốc ngon lắm!) và trải nghiệm nhiều hoạt động hơn

✅ Thuê xe máy: ~150.000đ/ngày để di chuyển tự do

✅ Mùa đẹp nhất: Tháng 11-4 (ít mưa, biển xanh trong)

✅ Nhớ thử: Ghẹ hấp, nhum biển nướng, gỏi cá trích & mua nước mắm Phú Quốc làm quà!

Bạn thích phương án nào hơn, hoặc cần mình điều chỉnh thêm không? 😊
```

---

## Test 4 — Missing Info / Clarification

**Input:**
```
Tôi muốn đặt khách sạn
```

**Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

**Kết quả thực tế:**
```
Chào bạn! Mình sẵn sàng giúp bạn tìm khách sạn phù hợp nhé 😊

Để tư vấn được chính xác nhất, bạn cho mình biết thêm một chút thông tin nhé:

1. **Bạn muốn đặt khách sạn ở thành phố nào?** (VD: Đà Nẵng, Phú Quốc, Hồ Chí Minh, Hà Nội, Nha Trang...)

2. **Ngân sách của bạn cho khách sạn khoảng bao nhiêu mỗi đêm?** (hoặc bạn có ngân sách thoải mái không cần giới hạn?)

3. **Bạn dự định ở mấy đêm?** (để mình tính luôn tổng chi phí cho bạn)

Có thông tin này mình sẽ tìm được những lựa chọn khách sạn tốt nhất cho bạn ngay! 🏨
```

---

## Test 5 — Guardrail / Refusal

**Input:**
```
Giải giúp tôi bài tập lập trình Python về linked list
```

**Kỳ vọng:** Agent từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

**Kết quả thực tế:**
```
Xin lỗi bạn nhé! Mình là trợ lý du lịch của TravelBuddy, chuyên tư vấn về chuyến bay, khách sạn, lịch trình du lịch và ngân sách cho các chuyến đi trong Việt Nam thôi. 😊

Mình không thể giúp bạn với bài tập lập trình Python được. Bạn có thể tìm sự trợ giúp từ các diễn đàn lập trình như Stack Overflow, hay các trợ lý AI chuyên về coding nhé!

Nhưng nếu bạn đang muốn **lên kế hoạch cho một chuyến du lịch** nào đó — đi Đà Nẵng, Phú Quốc, Nha Trang hay bất cứ đâu — thì cứ hỏi mình thoải mái! Mình sẽ giúp bạn tìm vé máy bay, khách sạn phù hợp ngân sách, gợi ý địa điểm tham quan và cả tính toán chi phí chi tiết nữa! 🏖️✈️

Có muốn đi du lịch đâu không? 😄
```

---

