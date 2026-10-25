PRAGMA foreign_keys=ON;
-- Tables are loaded from CSVs by src/utils.py. Logical relationships:
-- shipments.warehouse_id -> warehouses.warehouse_id
-- shipments.driver_id -> drivers.driver_id
-- shipments.vehicle_id -> vehicles.vehicle_id
-- shipments.route_id -> routes.route_id
-- deliveries.shipment_id -> shipments.shipment_id
-- feedback.delivery_id -> deliveries.delivery_id
