import pandas as pd
import plotly.graph_objs as go

class ThreeDGraphsAnimated:
    """
    The ThreeDGraphsAnimated graph class creates the 3d animated graphs

    Author: lawnguy
    """
    def __init__(self, data, large_dataset=False):
        """
        :param data: DataFrame
        :param large_dataset: Boolean to help not bloat
        """
        self.__data = data.copy()
        self.__data['z'] = pd.to_numeric(self.__data['z'], errors='coerce')
        self.__data['y'] = pd.to_numeric(self.__data['y'], errors='coerce')
        self.__data['date'] = pd.to_datetime(self.__data['date'], errors='coerce')
        self.__unique_dates = sorted(self.__data['date'].dropna().unique())
        self.__fig = go.Figure()
        self.__large_dataset = large_dataset

    def __generate_hover_text(self, frame_data):
        """
        Helper function to create hover text and date
        :param frame_data: the frame data for each frame
        :return: the template of the hover data filled with data
        """
        return [
            f"X: {x}<br>Y: {z}<br>Z: {y}<br>Msg: {msg}<br>Glow Ink: {glow}<br>Sign Color: {color}<br>Date: {date}"
            for x, y, z, msg, glow, color, date in zip(
                frame_data['x'], frame_data['z'], frame_data['y'],
                frame_data['mgs'], frame_data['Glow Ink'], frame_data['Sign Color'], frame_data['date']
            )
        ]

    def create_animation(self):
        """
        Create a 3D scatter plot
        """


        try:
            #starting frame of the animations
            initial_date = self.__unique_dates[0]
            initial_data = self.__data[self.__data['date'] == initial_date]
            self.__add_frame(initial_data, add_as_trace=True)

            #the loop to create all the frames
            frames = [
                go.Frame(
                    data=[self.__create_scatter3d(
                        self.__data[self.__data['date'] == date] if self.__large_dataset else
                        self.__data[self.__data['date'] <= date]
                    )],
                    name=str(date),
                    layout=go.Layout(
                        annotations=[
                            dict(
                                x=0.5, y=0.0, xref="paper", yref="paper",
                                text=f"Date: {date.strftime('%Y-%m-%d')}",
                                showarrow=False,
                                font=dict(size=14, color="white")
                            )
                        ]
                    )
                )
                for date in self.__unique_dates
            ]
            self.__fig.frames = frames

            # Add animation controls and layout
            self.__fig.update_layout(
                updatemenus=[self.__create_animation_controls()],
                template="plotly_dark",
                scene=dict(
                    xaxis_title="X Axis",
                    yaxis_title="Z Axis",
                    zaxis_title="Y Axis",
                ),
                title="codysmile11 OW Signs 3D Animated By Day Placed",
                title_x=0.5,
                width=1000,
                height=700,
                margin=dict(r=60, l=60, b=60, t=60),
                annotations=[
                    dict(
                        x=0.5, y=1.1, xref="paper", yref="paper",
                        text=f"Date: {initial_date.strftime('%Y-%m-%d')}",
                        showarrow=False,
                        font=dict(size=14, color="white")
                    )
                ]
            )

        except Exception as e:
            raise RuntimeError(f"Error while creating animation: {e}")

    def __create_scatter3d(self, frame_data):
        """
        __create_scatter3d helper function to help create the scatter plots of each frame
        :param frame_data: each frames and the data inside
        :return: all of the scatter plot info like z y x data and makers hover text ect.
        """
        return go.Scatter3d(
            x=frame_data['x'],
            y=frame_data['z'],
            z=frame_data['y'],
            mode='markers',
            text=self.__generate_hover_text(frame_data),
            hoverinfo="text",
            marker=dict(
                size=8,
                color=frame_data['y'],
                colorscale='rdbu',
                showscale=True,
                opacity=0.8,
                colorbar=dict(title="Y-Values", titleside="top")
            )
        )

    def __add_frame(self, frame_data, add_as_trace=False):
        """
        the __add_frame is a helper functions to add a new frame
        :param frame_data: the frame data
        :param add_as_trace: a bool to create a continues graph or not new frame
        :return: the scatter plot for the frame
        """

        scatter = self.__create_scatter3d(frame_data)
        if add_as_trace:
            self.__fig.add_trace(scatter)
        return scatter

    def __create_animation_controls(self):
        """
        __create_animation_controls() helper function that help create the play and puase controlls
        :return: None
        """

        return dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(
                    label="Play",
                    method="animate",
                    args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                ),
                dict(
                    label="Pause",
                    method="animate",
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]
                )
            ]
        )

    def show(self, html_name=None):
        """
        show() function shows and creates and html file
        """
        self.__fig.show()
        if html_name:
            self.__fig.write_html(html_name)