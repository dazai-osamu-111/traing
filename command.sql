-- Thống kê số review qua từng tháng

SELECT YEAR(date_of_experience) AS year, MONTH(date_of_experience) AS month, COUNT(*) AS total_reviews
FROM reviews
GROUP BY YEAR(date_of_experience), MONTH(date_of_experience)
ORDER BY year, month;

-- Tháng có nhiều review nhất

SELECT YEAR(date_of_experience) AS year, MONTH(date_of_experience) AS month, COUNT(*) AS total_reviews
FROM reviews
GROUP BY YEAR(date_of_experience), MONTH(date_of_experience)
ORDER BY total_reviews DESC
LIMIT 1;

-- Thống kê số review theo country

SELECT country, COUNT(*) AS total_reviews
FROM reviews
GROUP BY country
ORDER BY total_reviews DESC;

-- Đối chiếu số lượng review từng tháng qua các năm

SELECT YEAR(date_of_experience) AS year, MONTH(date_of_experience) AS month, COUNT(*) AS total_reviews
FROM reviews
GROUP BY YEAR(date_of_experience), MONTH(date_of_experience)
ORDER BY month, year;