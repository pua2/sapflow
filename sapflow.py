import pandas as pd
import datetime as dt

#parser = lambda date: pd.datetime.strptime(date, '%d/%m/%Y -%H:%M:%S')

path = "data/sapflow/"

weather_csv = pd.read_csv(f'{path}all_weather.csv', low_memory=False, parse_dates=[["Date","Time"]])
sapflow_csv = pd.read_csv(f'{path}all_sapflow.csv', low_memory=False, parse_dates=[["Date","Time"]])

weather_csv["Date_Time"] = weather_csv["Date_Time"].dt.strftime('%d/%m/%Y %H:%M')
sapflow_csv["Date_Time"] = sapflow_csv["Date_Time"].dt.strftime('%d/%m/%Y %H:%M')

weather_csv = weather_csv[["Date_Time", "Solar Radiation (W/m^2)", "Air Temperature (deg.C)", "Corrected RH (%)", "Wind Speed (m/s)"]]
weather_csv.rename(columns = {"Date_Time":"datetime", "Solar Radiation (W/m^2)":"solar_rad","Air Temperature (deg.C)":"air_temp","Corrected RH (%)":"RH","Wind Speed (m/s)":"wind_speed"}, inplace=True)

sapflow_csv = sapflow_csv[["Date_Time", "Uncorrected Out (cm/hr)", "Uncorrected In (cm/hr)"]]
sapflow_csv.rename(columns ={"Date_Time":"datetime", "Uncorrected Out (cm/hr)":"outer_sapflow", "Uncorrected In (cm/hr)":"inner_sapflow"}, inplace=True)

merged=pd.merge(weather_csv, sapflow_csv, on='datetime', how='inner')

merged=merged.drop_duplicates()

df_outer = merged.drop("inner_sapflow", axis=1)
df_inner = merged.drop("outer_sapflow", axis=1)

merged.to_csv(f'{path}merged.csv', index =False)
df_outer.to_csv(f'{path}df_outer.csv', index =False)
df_inner.to_csv(f'{path}df_inner.csv', index =False)

#weather_csv.to_csv("weather.csv", index =False)
#sapflow_csv.to_csv("sapflow.csv", index =False)
