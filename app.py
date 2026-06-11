# ============================================================
# Streamlit Dashboard
# UAS Teknologi Big Data - TI23A
# NIM  : 230104040203
# Soal : NIM akhir ganjil
# Tema : Smart Retail Visitor Prediction System
# ============================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

VISITOR_TOTAL_PATH = (OUTPUT_DIR / "visitor_total").resolve()
VISITOR_TIME_PATH = (OUTPUT_DIR / "visitor_time").resolve()
ML_VISITOR_PATH = (OUTPUT_DIR / "ml_visitor").resolve()


st.set_page_config(
    page_title="Smart Retail Visitor Prediction",
    page_icon="🛒",
    layout="wide"
)


@st.cache_data
def load_parquet_data():
    visitor_total = pd.read_parquet(VISITOR_TOTAL_PATH)
    visitor_time = pd.read_parquet(VISITOR_TIME_PATH)
    ml_visitor = pd.read_parquet(ML_VISITOR_PATH)

    visitor_time["time_start"] = pd.to_datetime(visitor_time["time_start"])
    visitor_time["time_end"] = pd.to_datetime(visitor_time["time_end"])

    return visitor_total, visitor_time, ml_visitor


def train_linear_regression(zone_ml_data: pd.DataFrame):
    X = zone_ml_data[["hour"]]
    y = zone_ml_data["visitor_count"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def main():
    st.title("Smart Retail Visitor Prediction System")
    st.caption(
        "UAS Teknologi Big Data | TI23A | NIM 230104040203 | "
        "PySpark + Parquet + Linear Regression + Streamlit"
    )

    visitor_total, visitor_time, ml_visitor = load_parquet_data()

    zones = sorted(visitor_total["zone"].unique())

    st.sidebar.header("Filter Dashboard")

    selected_zone = st.sidebar.selectbox(
        "Pilih Zona",
        zones
    )

    prediction_hour = st.sidebar.slider(
        "Pilih Jam untuk Prediksi",
        min_value=0,
        max_value=23,
        value=10
    )

    total_selected = visitor_total.loc[
        visitor_total["zone"] == selected_zone,
        "total_visitor"
    ].iloc[0]

    zone_trend = (
        visitor_time[visitor_time["zone"] == selected_zone]
        .sort_values("time_start")
        .copy()
    )

    zone_ml = (
        ml_visitor[ml_visitor["zone"] == selected_zone]
        .sort_values("hour")
        .copy()
    )

    model = train_linear_regression(zone_ml)

    predicted_visitor = float(
        model.predict(pd.DataFrame({"hour": [prediction_hour]}))[0]
    )

    predicted_visitor = max(0, predicted_visitor)

    busiest_row = zone_trend.loc[zone_trend["visitor_count"].idxmax()]

    busiest_time_text = (
        busiest_row["time_start"].strftime("%H:%M")
        + " - "
        + busiest_row["time_end"].strftime("%H:%M")
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Pengunjung Zona",
        f"{int(total_selected):,}".replace(",", ".")
    )

    col2.metric(
        "Prediksi Pengunjung",
        f"{predicted_visitor:.0f}",
        help="Hasil prediksi berdasarkan model Linear Regression"
    )

    col3.metric(
        "Jam Tersibuk",
        busiest_time_text
    )

    st.subheader(f"Tren Pengunjung Zona {selected_zone} per 15 Menit")

    fig_trend = px.line(
        zone_trend,
        x="time_start",
        y="visitor_count",
        markers=True,
        title=f"Tren Pengunjung {selected_zone}",
        labels={
            "time_start": "Waktu Mulai",
            "visitor_count": "Jumlah Pengunjung"
        }
    )

    fig_trend.update_layout(
        xaxis_title="Waktu",
        yaxis_title="Visitor Count"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Dataset AI dan Hasil Prediksi Linear Regression")

    col4, col5 = st.columns([1, 2])

    with col4:
        st.write("Data AI berdasarkan hour")
        st.dataframe(zone_ml, use_container_width=True)

        st.write("Persamaan model")
        st.code(
            f"visitor_count = ({model.coef_[0]:.4f} × hour) + ({model.intercept_:.4f})",
            language="text"
        )

    with col5:
        prediction_table = pd.DataFrame({
            "hour": list(range(24))
        })

        prediction_table["predicted_visitor_count"] = model.predict(
            prediction_table[["hour"]]
        )

        prediction_table["predicted_visitor_count"] = (
            prediction_table["predicted_visitor_count"].clip(lower=0)
        )

        fig_prediction = px.line(
            prediction_table,
            x="hour",
            y="predicted_visitor_count",
            markers=True,
            title=f"Prediksi Pengunjung Berdasarkan Jam - {selected_zone}",
            labels={
                "hour": "Jam",
                "predicted_visitor_count": "Prediksi Visitor Count"
            }
        )

        st.plotly_chart(fig_prediction, use_container_width=True)

    st.subheader("Analisis Jam Sibuk Pengunjung")

    st.write(
        f"Berdasarkan agregasi tren 15 menit, zona **{selected_zone}** "
        f"memiliki kepadatan tertinggi pada rentang **{busiest_time_text}** "
        f"dengan jumlah **{int(busiest_row['visitor_count'])} pengunjung**. "
        "Rentang waktu ini dapat dijadikan acuan manajemen pusat perbelanjaan "
        "untuk menambah petugas, mengatur antrean, serta mengoptimalkan layanan "
        "pada area yang mengalami lonjakan pengunjung."
    )

    st.subheader("Ringkasan Total Semua Zona")

    fig_total = px.bar(
        visitor_total.sort_values("total_visitor", ascending=False),
        x="zone",
        y="total_visitor",
        title="Total Pengunjung Tiap Zona",
        labels={
            "zone": "Zona",
            "total_visitor": "Total Pengunjung"
        }
    )

    st.plotly_chart(fig_total, use_container_width=True)


if __name__ == "__main__":
    main()