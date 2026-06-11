# ============================================================
# UAS Teknologi Big Data - TI23A
# NIM  : 230104040203
# Soal : NIM akhir ganjil
# Tema : Smart Retail Visitor Prediction System
# Pipeline: Generate Data -> Spark Aggregation -> Parquet -> ML Dataset
# ============================================================

import random
from datetime import datetime, timedelta
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    hour,
    sum as spark_sum,
    avg,
    round as spark_round,
    window
)
from pyspark.sql.types import (
    StructType,
    StructField,
    TimestampType,
    StringType,
    IntegerType
)


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

VISITOR_TOTAL_PATH = (OUTPUT_DIR / "visitor_total").resolve()
VISITOR_TIME_PATH = (OUTPUT_DIR / "visitor_time").resolve()
ML_VISITOR_PATH = (OUTPUT_DIR / "ml_visitor").resolve()

ZONES = ["FoodCourt", "FashionArea", "Cinema"]


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("Smart Retail Visitor Prediction System")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark


def generate_visitor_data():
    random.seed(230104040203)

    start_time = datetime(2026, 6, 11, 9, 0, 0)

    rows = []

    for minute in range(180):
        current_time = start_time + timedelta(minutes=minute)

        for zone in ZONES:
            visitor_count = random.randint(10, 500)
            rows.append((current_time, zone, visitor_count))

    return rows


def main():
    spark = create_spark_session()

    schema = StructType([
        StructField("timestamp", TimestampType(), False),
        StructField("zone", StringType(), False),
        StructField("visitor_count", IntegerType(), False),
    ])

    data = generate_visitor_data()
    df = spark.createDataFrame(data, schema=schema)

    print("\n=== SAMPLE DATA VISITOR TRACKING ===")
    df.show(10, truncate=False)

    visitor_total = (
        df.groupBy("zone")
        .agg(spark_sum("visitor_count").alias("total_visitor"))
        .orderBy("zone")
    )

    print("\n=== TOTAL PENGUNJUNG TIAP ZONA ===")
    visitor_total.show(truncate=False)

    visitor_time = (
        df.groupBy("zone", window(col("timestamp"), "15 minutes"))
        .agg(spark_sum("visitor_count").alias("visitor_count"))
        .select(
            "zone",
            col("window.start").alias("time_start"),
            col("window.end").alias("time_end"),
            "visitor_count"
        )
        .orderBy("zone", "time_start")
    )

    print("\n=== TREN PENGUNJUNG TIAP 15 MENIT ===")
    visitor_time.show(20, truncate=False)

    ml_visitor = (
        df.withColumn("hour", hour(col("timestamp")))
        .groupBy("zone", "hour")
        .agg(spark_round(avg("visitor_count"), 2).alias("visitor_count"))
        .orderBy("zone", "hour")
    )

    print("\n=== DATASET AI BERDASARKAN HOUR ===")
    ml_visitor.show(truncate=False)

    visitor_total.write.mode("overwrite").parquet(str(VISITOR_TOTAL_PATH))
    visitor_time.write.mode("overwrite").parquet(str(VISITOR_TIME_PATH))
    ml_visitor.write.mode("overwrite").parquet(str(ML_VISITOR_PATH))

    print("\n=== PARQUET BERHASIL DIBUAT ===")
    print(f"visitor_total : {VISITOR_TOTAL_PATH}")
    print(f"visitor_time  : {VISITOR_TIME_PATH}")
    print(f"ml_visitor    : {ML_VISITOR_PATH}")

    print("\n=== VALIDASI BACA ULANG PARQUET ===")
    print("visitor_total rows:", spark.read.parquet(str(VISITOR_TOTAL_PATH)).count())
    print("visitor_time rows :", spark.read.parquet(str(VISITOR_TIME_PATH)).count())
    print("ml_visitor rows   :", spark.read.parquet(str(ML_VISITOR_PATH)).count())

    spark.stop()


if __name__ == "__main__":
    main()