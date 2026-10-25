from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def build_features():
    folder=ROOT/"data/cleaned"
    if not list(folder.glob("*.csv")): folder=ROOT/"data/raw"
    read=lambda n: pd.read_csv(folder/f"logitrack_{n}.csv")
    s=read("shipments"); d=read("deliveries"); r=read("routes"); dr=read("drivers"); v=read("vehicles"); w=read("warehouses"); f=read("feedback")
    s["shipment_dt"]=pd.to_datetime(s.shipment_dt,errors="coerce"); d["actual_dt"]=pd.to_datetime(d.actual_dt,errors="coerce")
    x=s.merge(d,on="shipment_id",how="left").merge(r,on="route_id",how="left").merge(dr,on="driver_id",how="left",suffixes=("","_driver")).merge(v,on="vehicle_id",how="left").merge(w,on="warehouse_id",how="left",suffixes=("","_warehouse")).merge(f,on="delivery_id",how="left")
    x["delivery_days"]=(pd.to_datetime(x.actual_dt)-x.shipment_dt).dt.total_seconds()/86400
    x["is_delayed"]=x.delay_hours.fillna(0)>0
    x["weight_category"]=pd.cut(x.weight_kg,[-1,100,500,1500,float("inf")],labels=["Light","Medium","Heavy","Very Heavy"])
    x["distance_category"]=pd.cut(x.distance_km,[-1,100,500,1000,float("inf")],labels=["Short","Medium","Long","Very Long"])
    x["experience_level"]=pd.cut(x.experience,[-1,2,5,10,float("inf")],labels=["Junior","Mid","Senior","Expert"])
    x["delivery_month"]=x.shipment_dt.dt.to_period("M").astype(str); x["delivery_day_of_week"]=x.shipment_dt.dt.day_name(); x["delivery_hour"]=x.shipment_dt.dt.hour
    return x
if __name__=="__main__": build_features().to_csv(ROOT/"data/cleaned/logitrack_features.csv",index=False)
