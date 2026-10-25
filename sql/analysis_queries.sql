-- 1 Overall delivery performance
SELECT COUNT(*) total_deliveries, ROUND(100.0*SUM(status='Delivered')/COUNT(*),2) success_rate_pct FROM deliveries;
-- 2 Average delay by route type
SELECT r.route_type, AVG(d.delay_hours) avg_delay FROM deliveries d JOIN shipments s USING(shipment_id) JOIN routes r USING(route_id) GROUP BY r.route_type;
-- 3 Top drivers by rating
SELECT dr.name, AVG(f.rating) avg_rating, COUNT(*) deliveries FROM drivers dr JOIN shipments s USING(driver_id) JOIN deliveries d USING(shipment_id) LEFT JOIN feedback f USING(delivery_id) GROUP BY dr.driver_id ORDER BY avg_rating DESC LIMIT 10;
-- 4 Warehouse performance
SELECT w.name, AVG(d.delay_hours) avg_delay FROM warehouses w JOIN shipments s USING(warehouse_id) JOIN deliveries d USING(shipment_id) GROUP BY w.name;
-- 5 Monthly trends
SELECT substr(s.shipment_dt,1,7) month, COUNT(*) shipments, AVG(d.delay_hours) avg_delay FROM shipments s JOIN deliveries d USING(shipment_id) GROUP BY month ORDER BY month;
-- 6 Vehicle utilization
SELECT v.vehicle_type, COUNT(s.shipment_id) shipments FROM vehicles v LEFT JOIN shipments s USING(vehicle_id) GROUP BY v.vehicle_type;
-- 7 Rating by delivery status
SELECT d.status, AVG(f.rating) avg_rating FROM deliveries d LEFT JOIN feedback f USING(delivery_id) GROUP BY d.status;
-- 8 Delay by distance category
SELECT CASE WHEN r.distance_km<100 THEN 'Short' WHEN r.distance_km<500 THEN 'Medium' WHEN r.distance_km<1000 THEN 'Long' ELSE 'Very Long' END category, AVG(d.delay_hours) avg_delay FROM routes r JOIN shipments s USING(route_id) JOIN deliveries d USING(shipment_id) GROUP BY category;
-- 9 Driver experience level
SELECT CASE WHEN dr.experience<=2 THEN 'Junior' WHEN dr.experience<=5 THEN 'Mid' WHEN dr.experience<=10 THEN 'Senior' ELSE 'Expert' END level, AVG(f.rating) rating, AVG(d.delay_hours) delay FROM drivers dr JOIN shipments s USING(driver_id) JOIN deliveries d USING(shipment_id) LEFT JOIN feedback f USING(delivery_id) GROUP BY level;
-- 10 Day of week
SELECT strftime('%w',s.shipment_dt) weekday, COUNT(*) shipments, AVG(d.delay_hours) avg_delay FROM shipments s JOIN deliveries d USING(shipment_id) GROUP BY weekday;
