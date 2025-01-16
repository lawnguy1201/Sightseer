from tempfile import template

import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from Util import Util
import plotly.graph_objs as go
import plotly.express as px


class TwoDGraphs:
    """
    The TwoDGraphs class creates 2d graphs
    Uses mostly matplotlib Not the best use the plotly one

    Author: lawnguy
    """

    def __init__(self, list_of_data=None, keys=None, x_cord=None, y_cord=None, name=None, unique_name=None):
        """
        this is the con for the TwoDGraphs class

        :param list_of_data: a list of values int/float
        :param keys: a list of str of keys from a dic
        """

        self.__data = list_of_data
        self.__keys = keys
        self.__x = x_cord
        self.__y = y_cord
        self.__name = name
        self.__unique = unique_name


        self.__fig = go.Figure()


    # NOTE* this is the best bar chart choice since its most interactive
    def create_plotly_bar_chart(self, html, title, x_text_list, y_text_list):
        """
        Create a bar chart with Plotly and add custom text annotations for x and y axes

        Args:
            html (str): The file name for saving the HTML output
            title (str): The title of the chart
            x_text_list (list): List of labels for x-axis values
            y_text_list (list): List of text annotations for y-axis values
        """
        try:
            #create a bar chart
            fig = px.bar(
                x=self.__keys,
                y=self.__data,
                title=title
            )

            fig.update_traces(
                marker=dict(color='lightblue'),
                text=y_text_list,
                textposition='outside'
            )

            if x_text_list:
                fig.update_layout(
                    template='plotly_dark',
                    xaxis=dict(
                        tickvals=list(range(len(self.__keys))),
                        ticktext=x_text_list
                    )
                )

            # Show and create html
            fig.show()
            fig.write_html(html)

        except Exception as e:
            raise RuntimeError(f"Error creating the bar chart: {e}")

    def create_Percent_Pie_Chart(self, overall):
        """
        the create_Percent_Pie_Chart creates a percent pie chart
        :return: None
        """

        #create a util obk
        utils = Util('', self.__keys, self.__data)
        total = utils.get_Total()

        percent_list = []
        non_big_percent = []
        sums = 0

        #find the percent of each banner
        for item in self.__data:
            percent = (item / total) * 100
            if percent >= 10.00:
                percent_list.append(percent)
            else:
                non_big_percent.append(percent)
                sums += percent

        percent_list.append(sums)

        # make fig obj's
        fig, ax1 = plt.subplots()
        fig.subplots_adjust(wspace=0)

        # pie chart params
        overall_ratios = percent_list
        overall_labels = overall
        angle = -180 * overall_ratios[0]
        wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle, #labels=overall_labels
                            )

        plt.show()

    def Create_non_log_bar(self, yLabel, xLabel, title):
        """
        The Create_non_log_bar function creates a non log bar chart
        :param yLabel: the label for the y
        :param xLabel: the label for the x
        :param title: the title
        :return:
        dic_keys: the list of keys from the dic
        self.__data: the data from the input for some reason
        dic_values: the list of the vlaues
        """
        dic_keys = [str(key) for key in self.__keys]
        dic_values = list(self.__data)

        colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

        try:
            plt.bar(dic_keys, dic_values, color=colors[:len(dic_keys)])
            plt.ylabel(yLabel)
            plt.xlabel(xLabel)
            plt.title(title)
            plt.xticks(rotation=45, ha='right', size=5)
            plt.tight_layout()
            plt.show()


        except Exception as e:
            raise RuntimeError(f"Error in creating non-log bar graph {e}")

        return dic_keys, self.__data, dic_values

    def Create_Bar_Charts(self, yLabel, xLabel, title):
        """
        the Create_Bar_Charts function creates Two bar chart
        :return:
        dic_keys: the keys from the dic in a list of str
        self.__dic_data: a list of values from the dic data list
        dic_values: creates a list from the dic values
        """
        dic_keys = [str(key) for key in self.__keys]
        dic_values = list(self.__data)

        dicts = {'Sign Name': dic_keys,
                 'Amount of Signs': self.__data}

        df = pd.DataFrame(dicts)
        df.to_markdown()
        df.to_csv('OW Banner Dic.csv')
        display(df)

        # For log Scaled Data
        try:
            colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

            plt.bar(dic_keys, dic_values, color=colors[:len(dic_keys)])
            plt.yscale('log')
            plt.ylabel(yLabel)
            plt.xlabel(xLabel)
            plt.title(title)
            plt.xticks(rotation=45, ha='right', size=5)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            raise RuntimeError(f"Error Creating scaled bar graph {e}")

        return dic_keys, self.__data, dic_values