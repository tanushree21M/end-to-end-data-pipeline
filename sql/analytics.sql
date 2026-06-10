-- ============================================================
-- Analytics Queries — Business Insights
-- Run these after pipeline loads data
-- ============================================================

-- 1. Overall Pipeline Summary
SELECT
    COUNT(*)                                         AS total_orders,
    SUM(revenue)                                     AS total_revenue,
    ROUND(AVG(amount), 2)                            AS avg_order_value,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_orders,
    COUNT(CASE WHEN status = 'pending'   THEN 1 END) AS pending_orders
FROM fct_orders;

-- 2. Top 5 Customers by Revenue
SELECT
    name, city, total_orders, total_revenue, customer_segment
FROM dim_customer_summary
ORDER BY total_revenue DESC
LIMIT 5;

-- 3. Monthly Revenue Trend
SELECT
    order_month,
    COUNT(*)     AS total_orders,
    SUM(revenue) AS monthly_revenue,
    ROUND(AVG(amount), 2) AS avg_order_value
FROM fct_orders
GROUP BY order_month
ORDER BY order_month;

-- 4. Revenue by City
SELECT
    u.city,
    COUNT(o.order_id)  AS total_orders,
    SUM(o.revenue)     AS total_revenue
FROM fct_orders o
JOIN dim_users u ON o.user_id = u.user_id
GROUP BY u.city
ORDER BY total_revenue DESC;

-- 5. Customer Segments
SELECT
    customer_segment,
    COUNT(*)           AS total_customers,
    SUM(total_revenue) AS segment_revenue
FROM dim_customer_summary
GROUP BY customer_segment;
