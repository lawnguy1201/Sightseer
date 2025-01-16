from collections import defaultdict
import numpy as np
import plotly.graph_objs as go

class ThreeDGraphs:
    """
    The ThreeDGraphs class creates 3d graphs using plotly api

    Author: lawnguy
    """

    def __init__(self, x_cord, y_cord, z_cord, name, a_color, unique_names, pat=None, banners=False,
                 large_DataSet=False, include_pat_=False):

        self.__x, self.__y, self.__z = x_cord, y_cord, z_cord
        self.__name, self.__color = name, a_color

        #if were not using pat change it so no error
        self.__pat = pat if pat is not None else ["None"] * len(x_cord)
        self.__unique_names = unique_names

        self.__hover_text = self.__generate_hover_text(banners, include_pat=include_pat_)
        self.__fig = go.Figure()

        # large dataset we dont want to use filters to not bloat up the file size
        if not large_DataSet:
            self.__filtered_data = {
                unique_name: {
                    'x': [self.__x[i] for i, name in enumerate(self.__name) if name == unique_name],
                    'y': [self.__z[i] for i, name in enumerate(self.__name) if name == unique_name],
                    'z': [self.__y[i] for i, name in enumerate(self.__name) if name == unique_name],
                    'text': [self.__hover_text[i] for i, name in enumerate(self.__name) if name == unique_name]
                }
                for unique_name in self.__unique_names
            }
            self.__filtered_data['all'] = {
                'x': self.__x,
                'y': self.__z,
                'z': self.__y,
                'text': self.__hover_text
            }
        else:
            self.__filtered_data = {'all': {}}

    def __generate_hover_text(self, banners, include_pat):
        """
        The __generate_hover_text() function is a helper function to create the hovertext
        :param banners: bool values should be removed
        :param include_pat: should be removed bool value
        :return: the hover template for later on
        """
        #genral template used for the hovertext for later on pretty optimized
        hover_template = (
            lambda n, x, y, z, c,
                   p: f"Msg: {n}<br>X: {x}<br>Y: {y}<br>Z: {z}<br>Glow Ink: {c}<br>Sign Color: {p or 'None'}"
            if not banners else
            lambda n, x, y, z, c, p: f"Name: {n}<br>X: {x}<br>Y: {y}<br>Z: {z}<br>Color: {c}<br>Pat: {p or 'None'}"
        )
        return [
            hover_template(n, x, y, z, c, p)
            for n, x, y, z, c, p in zip(self.__name, self.__x, self.__y, self.__z, self.__color, self.__pat)
        ]

    def scatter_Plot(self):
        """
        The scatter_plot() function creates the scatter plot
        :return:
        """
        try:
            print('Start of the Scatter Plot')
            self.__fig = go.Figure(data=[go.Scatter3d(
                x=self.__x,
                #y and z are switched to make the graph less of a mind fuck to look at
                y=self.__z,
                z=self.__y,
                mode='markers',
                text=self.__hover_text,
                hoverinfo="text",
                marker=dict(
                    size=8,
                    color=self.__y,
                    colorscale='rdbu',
                    opacity=0.8,
                    showscale=True,
                    colorbar=dict(
                        title='Y-Level',
                        titleside='top'
                    )
                )
            )])

            print("filter buttons begin")

            # Add filter buttons only if not a large dataset
            updatemenus = []
            if self.__filtered_data.get('all'):
                filter_buttons = [
                    dict(
                        args=[{
                            'x': [self.__filtered_data[unique_name]['x']],
                            'y': [self.__filtered_data[unique_name]['y']],
                            'z': [self.__filtered_data[unique_name]['z']],
                            'text': [self.__filtered_data[unique_name]['text']]
                        }],
                        label=unique_name,
                        method="update"
                    )
                    for unique_name in self.__unique_names
                ]

                filter_buttons.insert(0, dict(
                    args=[{
                        'x': [self.__filtered_data['all']['x']],
                        'y': [self.__filtered_data['all']['y']],
                        'z': [self.__filtered_data['all']['z']],
                        'text': [self.__filtered_data['all']['text']]
                    }],
                    label='all',
                    method='update'
                ))

                print("Filter Buttons Inserted")

                updatemenus.append(
                    dict(
                        buttons=filter_buttons,
                        direction='down',
                        pad={'r': 10, 't': 10},
                        showactive=True,
                        x=0.5,
                        xanchor='left',
                        y=1.15,
                        yanchor='top',
                        name='Filters'
                    )
                )

            #add the buttons to the graph
            print("Start adding buttons to the Graph")
            buttons_types = [
                dict(
                    args=['type', 'scatter3d'],
                    label='3d-Plot',
                    method='restyle'
                ),
                dict(
                    args=['type', 'scatter2d'],
                    label='2d-Plot',
                    method='restyle'
                ),
                dict(
                    args=['type', 'heatmap'],
                    label='heatmap',
                    method='restyle'
                ),
                dict(
                    args=['type', 'mesh3d'],
                    label='Mesh 3d Plot',
                    method='restyle'
                )
            ]

            updatemenus.append(
                dict(
                    buttons=buttons_types,
                    direction='down',
                    pad={'r': 10, 't': 10},
                    showactive=True,
                    x=0.1,
                    xanchor='left',
                    y=1.15,
                    yanchor='top',
                    name='Plot Type: '
                )
            )

            #add the text to the side
            annotations = [
                dict(text="Plot Types:",
                     showarrow=False,
                     x=0.024,
                     y=1.13,
                     yref="paper",
                     align="left")
            ]
            #if we have the filter buttons we need to add this text to the side
            if self.__filtered_data.get('all'):
                annotations.append(
                    dict(text='Filters:',
                         showarrow=False,
                         x=0.455,
                         y=1.13,
                         yref='paper',
                         align='left')
                )

            # Add the layout
            print("Start to update the layout")
            self.__fig.update_layout(
                template='plotly_dark',
                updatemenus=updatemenus,
                annotations=annotations,
                scene=dict(
                    xaxis_title='X Axis',
                    yaxis_title='z Axis',
                    zaxis_title='y Axis',
                ),
                width=1200,
                height=800,
                margin=dict(r=60, l=60, b=60, t=60)
            )
            print("Done with graph")
        except Exception as e:
            raise RuntimeError(f"Error creating the first plot: {e}")

    def show(self, html_Name=None):
        """
        the show function shows the graph and creates a html file
        :param html_Name: the name of the html
        :return: None
        """
        self.__fig.show()
        self.__fig.write_html(html_Name)