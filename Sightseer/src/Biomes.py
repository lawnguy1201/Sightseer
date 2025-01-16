import os
import sqlite3
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
import matplotlib.pyplot as plt
from colorcet import glasbey_category10

class Biomes:
    """
    Biomes class is to work with the large biomes files and data to create graphs

    NOTE* This Class does not work properly
    Needs work on, at this point the biomes bs is not working well for me

    Author lawnguy
    """
    def __init__(self, csv_file, db_file="data.db"):
        self.csv_file = csv_file
        self.db_file = db_file

    def load_csv_to_sqlite(self):
        """
        the load_csv_to_sqlite is meant to create a sqlite db
        :return:
        """
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"CSV file {self.csv_file} does not exist.")

        connection = sqlite3.connect(self.db_file)
        chunk_size = 10 ** 6  # Adjust based on memory capacity

        try:
            for chunk in pd.read_csv(self.csv_file, header=None, chunksize=chunk_size):
                chunk.columns = ['x_coordinate', 'z_coordinate', 'biome']
                chunk.to_sql("biomes", connection, if_exists="append", index=False)
        finally:
            connection.close()

    def fetch_all_data(self):
        """
        the fetch_all_data is a funciton to get teh data that you are looking for
        :return:
        """
        connection = sqlite3.connect(self.db_file)
        try:
            query = "SELECT x_coordinate, z_coordinate, biome FROM biomes"
            return pd.read_sql_query(query, connection)
        finally:
            connection.close()

    def generate_datashader_image(self, output_image):
        """
        generate_datashader_image funtion is used to creat a datashader image to help handle the large
        amount of data fast and better then plotly

        :param output_image: the name of the image
        :return:
        """
        print("Fetching data from SQLite...")
        df = self.fetch_all_data()

        print("Creating Datashader canvas...")
        cvs = ds.Canvas(plot_width=1000, plot_height=1000)
        agg = cvs.points(df, x="x_coordinate", y="z_coordinate", agg=ds.count_cat("biome"))

        print("Shading the data...")
        biome_colors = glasbey_category10  # Predefined color palette for categories
        img = tf.shade(agg, color_key=dict(zip(df['biome'].unique(), biome_colors)))

        print("Saving the image...")
        img.to_pil().save(output_image)
        print(f"Image saved to {output_image}")

    def generate_plotly_overlay(self, output_image, output_html):
        """
        Overlay Datashader raster output onto a Plotly figure for interactivity.
        """
        import plotly.graph_objects as go
        from PIL import Image

        img = Image.open(output_image)

        fig = go.Figure()

        #overlay the image
        fig.add_trace(go.Image(z=img))

        fig.update_layout(
            title="Biome Distribution with Datashader",
            xaxis=dict(title="X Coordinate"),
            yaxis=dict(title="Z Coordinate"),
        )

        fig.write_html(output_html)
        fig.show()

        #debug
        print(f"Plotly figure saved to {output_html}")
