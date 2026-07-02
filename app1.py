import streamlit as st
import pandas as pd
import numpy as np

from db_utils import get_all_cities, get_distance, get_carriers
 
@st.cache_data
def load_cities_from_db():
    return get_all_cities()

CITIES = load_cities_from_db()




def calculate_options(from_city, to_city, weight_kg, w_time):
    dist = get_distance(from_city, to_city)
    options = {}
    
    include_express = w_time >= 0.5
    carriers = get_carriers(include_express=include_express)

    for name, base_cost, cost_per_kg, cost_per_km, speed in carriers:
        cost = base_cost + (weight_kg * cost_per_kg) + (dist * cost_per_km)
        
        if name == "ЭкспрессDT":
            time = 1
        else:
            time = max(1, int(dist / speed))
            
        co2 = dist * 0.12 / 1000
        
        options[name] = {"cost": cost, "time": time, "co2": co2}

    return options, dist

 


st.set_page_config(page_title="Система выбора доставки по Татарстану", layout="centered")

st.title("Разработка системы сравнения и выбора оптимального способа доставки посылок")
st.markdown(
    "Сравнение способов доставки с учётом стоимости, времени и веса."
)

col1, col2 = st.columns(2)
with col1:
    from_city = st.selectbox("Город отправления", CITIES, index=0)
with col2:
    to_city = st.selectbox("Город назначения", CITIES, index=1)

weight = st.slider("Вес посылки (кг)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

st.markdown("---")

if from_city == to_city:
    st.warning("Город отправления и назначения совпадают. Доставка не требуется.")
else:
    st.subheader("Задание весов критериев")
    w_cost = st.slider("Вес стоимости", 0.0, 1.0, 0.4)
    w_time = st.slider("Вес времени доставки", 0.0, 1.0, 0.3)
    w_co2 = round(1.0 - w_cost - w_time, 2)
    if w_co2 < 0:
        w_co2 = 0.0
        st.warning("Сумма весов превышает 1. Вес CO₂ установлен в 0.")

    options, dist = calculate_options(from_city, to_city, weight, w_time)
    st.info(f"Расстояние между городами: {dist} км")

    if not options:
        st.error("Нет доступных способов доставки.")
    else:
        df = pd.DataFrame(options).T

        for col in ["cost", "time", "co2"]:
            col_values = df[col].values  
            col_min = np.min(col_values)  
            col_max = np.max(col_values)  
            
            if col_max != col_min:
                df[f"norm_{col}"] = (col_values - col_min) / (col_max - col_min)
            else:
                df[f"norm_{col}"] = 0.0

        
        weights = np.array([w_cost, w_time, w_co2])  
        normalized_values = df[["norm_cost", "norm_time", "norm_co2"]].values  
        
        
        df["score"] = np.round(np.dot(normalized_values, weights), 2)

        best_option = df["score"].idxmin()

        st.subheader("Результаты сравнения")
        display_df = df[["cost", "time", "co2", "score"]].copy()
        display_df.columns = ["Стоимость (₽)", "Время (дни)", "CO₂ (кг)", "Итоговый балл"]
        st.dataframe(display_df.style.format("{:.2f}"))

        st.success(f"Рекомендуемый способ доставки: {best_option}")

        rec = options[best_option]
        st.markdown(
            f"**Характеристики рекомендованного варианта:**\n\n"
            f"- Стоимость: {rec['cost']:.0f} ₽\n"
            f"- Срок доставки: {rec['time']} дн.\n"
            f"- Углеродный след: {rec['co2']:.3f} кг CO₂"
        )

st.markdown("---")
st.caption("ВКР Исмагилов.")