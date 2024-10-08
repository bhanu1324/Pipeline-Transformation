# -*- coding: utf-8 -*-
"""Countries Pipeline.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1N_Bkss9iegpHDJaTB5LIa-xqA0JU6lDJ
"""

pip install pyspark pandas sqlalchemy psycopg2-binary

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

# Initialize Spark session
spark = SparkSession.builder.appName("DP - Countries").getOrCreate()

import os

# Define the directory path
directory_path = 'dataset/countries/'

# Create the directory if it doesn't exist
os.makedirs(directory_path)

# Define the path to the dataset
csv_file = '/content/dataset/countries/countries of the world.csv'

# Read the CSV file into a Spark DataFrame
df = spark.read.csv(csv_file, header=True, inferSchema=True)

schema = StructType([
    StructField("Country", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Population", IntegerType(), True),
    StructField("Area (sq. mi.)", DoubleType(), True),
    StructField("Pop. Density (per sq. mi.)", DoubleType(), True),
    StructField("Coastline (coast/area ratio)", DoubleType(), True),
    StructField("Net migration", DoubleType(), True),
    StructField("Infant mortality (per 1000 births)", DoubleType(), True),
    StructField("GDP ($ per capita)", IntegerType(), True),
    StructField("Literacy (%)", DoubleType(), True),
    StructField("Phones (per 1000)", DoubleType(), True),
    StructField("Arable (%)", DoubleType(), True),
    StructField("Crops (%)", DoubleType(), True),
    StructField("Other (%)", DoubleType(), True),
    StructField("Climate", DoubleType(), True),
    StructField("Birthrate", DoubleType(), True),
    StructField("Deathrate", DoubleType(), True),
    StructField("Agriculture", DoubleType(), True),
    StructField("Industry", DoubleType(), True),
    StructField("Service", DoubleType(), True)
])

# Example of casting columns to specific types
df = df.withColumn("Population", col("Population").cast(IntegerType())) \
       .withColumn("GDP ($ per capita)", col("GDP ($ per capita)").cast(IntegerType())) \
       .withColumn("Literacy (%)", col("Literacy (%)").cast(DoubleType()))

# Further transformations if needed
df = df.na.fill(0)  # Replace nulls with 0 for numerical columns

output_path = './datasets/countries/countries_data.parquet'
df.write.parquet(output_path)

# If running locally
!apt update
!apt install -y postgresql
!/etc/init.d/postgresql start
!sudo -u postgres psql -c "CREATE DATABASE countries_db;"
!sudo -u postgres psql -c "CREATE USER developer WITH PASSWORD 'test';"
!sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE countries_db TO developer;"

import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Define connection parameters
host = "localhost"
port = 5432
dbname = "countries_db"
user = "developer"
password = "test"

# Create a connection string
conn_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

# Create SQLAlchemy engine
engine = create_engine(conn_str)

# Convert Spark DataFrame to Pandas DataFrame
df_pandas = df.toPandas()

# Write DataFrame to PostgreSQL table
df_pandas.to_sql('countries', engine, if_exists='replace', index=False)

print("Data written to PostgreSQL table successfully.")


# # Query to fetch data
query = "SELECT * FROM countries;"

# # Fetch data into a DataFrame
df_query = pd.read_sql(query, engine)

# # Display the DataFrame
print(df_query)