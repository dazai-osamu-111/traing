import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector

# Hàm crawl dữ liệu review từ trang web
def crawl_reviews_from_website(url, from_date=None, to_date=None, max_reviews=None):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, "html.parser")
    reviews = []
    count = 0

    # Duyệt qua từng review card
    for review in soup.select("div.styles_reviewCardInner__EwDq2"):
        try:
            # Lấy tên khách hàng
            customer_name = review.select_one("span[data-consumer-name-typography]").get_text(strip=True)

            # Lấy tiêu đề
            title = review.select_one("h2[data-service-review-title-typography]").get_text(strip=True)

            # Lấy nội dung review
            content = review.select_one("p[data-service-review-text-typography]").get_text(strip=True)

            # Lấy đánh giá (rate)
            rate = int(review.select_one("div[data-service-review-rating]")["data-service-review-rating"])

            # Lấy quốc gia
            country_element = review.select_one("div.styles_consumerExtraDetails__fxS4S")
            country = country_element.select("span")[-1].get_text(strip=True)

            # Lấy ngày trải nghiệm và chuyển đổi định dạng
            raw_date = review.select_one("p[data-service-review-date-of-experience-typography]").get_text(strip=True).replace("Date of experience:", "").strip()
            try:
                date_of_experience = datetime.strptime(raw_date, "%B %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                date_of_experience = None

            # Kiểm tra điều kiện ngày nếu from_date và to_date được cung cấp
            if from_date and to_date:
                if not date_of_experience or not (from_date <= date_of_experience <= to_date):
                    continue  # Bỏ qua review nếu không nằm trong khoảng thời gian

            # Thêm dữ liệu vào danh sách
            reviews.append({
                "customer_name": customer_name,
                "title": title,
                "content": content,
                "rate": rate,
                "country": country,
                "date_of_experience": date_of_experience
            })
            count += 1

            # Kiểm tra giới hạn số lượng review
            if max_reviews and count >= max_reviews:
                break

        except Exception as e:
            print(f"Error parsing a review: {e}")

    return reviews

# Hàm lưu dữ liệu vào cơ sở dữ liệu
def save_to_database(reviews):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ducnt_ps",
        database="litextention_training_db"
    )
    cursor = connection.cursor()

    # Tạo bảng nếu chưa tồn tại
    create_table_query = """
    CREATE TABLE IF NOT EXISTS reviews (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(255),
        title VARCHAR(255),
        content TEXT,
        rate INT,
        country VARCHAR(10),
        date_of_experience DATE
    )
    """
    cursor.execute(create_table_query)

    # Lưu dữ liệu vào bảng
    for review in reviews:
        query = """
            INSERT INTO reviews (customer_name, title, content, rate, country, date_of_experience)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (
            review['customer_name'],
            review['title'],
            review['content'],
            review['rate'],
            review['country'],
            review['date_of_experience']
        )
        cursor.execute(query, data)

    connection.commit()
    cursor.close()
    connection.close()

# URL của trang web
url = "https://www.trustpilot.com/review/litextension.com"

# Tham số (tùy chọn): từ ngày, đến ngày, số lượng review
from_date = "2022-01-01"  # Định dạng: YYYY-MM-DD
to_date = "2024-12-31"    # Định dạng: YYYY-MM-DD
max_reviews = 5           # Giới hạn số lượng review (None nếu muốn lấy tất cả)

# Chuyển đổi from_date và to_date sang đối tượng datetime
if from_date:
    from_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%Y-%m-%d")
if to_date:
    to_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%Y-%m-%d")

# Crawl dữ liệu
reviews = crawl_reviews_from_website(url, from_date=from_date, to_date=to_date)

# In ra danh sách review
for i, review in enumerate(reviews, 1):
    print(f"Review {i}: {review}\n")

# Lưu dữ liệu vào database
save_to_database(reviews)
