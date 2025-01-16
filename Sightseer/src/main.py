"""
This program is to create classes and functions to visualize the data from the
Goneax the minecraft data miner

Author: lawnguy
"""

import pandas as pd
import re

from ThreeDSigns import ThreeDSigns
from ThreeDGraphsAnimated import ThreeDGraphsAnimated
from TwoDGraphs import TwoDGraphs
from Util import Util


def getBannerData(filename):
    """
    The getBannerData() function obtains and creates a list for all cols in the csv file

    :param filename: The filename you want to look for
    :return:
    banner_x_cord.astype(int): a list of x cords as an int
    banner_y_cord.astype(int): a list of y cords as an int
    banner_z_cord.astype(int): a list of z cords as an in t
    name: list of the custom name of the banner
    color_and_Pattern: a list of the color and pattern of the banner
    name.unique(): a list of all the unique names
    """
    try:

        pd.set_option('display.max_rows', None)

        # open up the file with latin-1 encoding and read the lines/rows
        with open(filename, 'r', encoding='Latin-1') as file:
            lines = file.readlines()

        modified_lines = []
        for line in lines:
            columns = line.strip().split(',')

            #Note if you get an error hear increase the 22 to +- 10 above the number of the error
            #just creates padding since pandas csv needs to be tabular
            if len(columns) < 22:
                columns.extend(['<NA>'] * (22 - len(columns)))

            modified_lines.append(','.join(columns))

        #create new csv
        with open('temp_modified_file.csv', 'w', encoding='Latin-1') as file:
            file.writelines("\n".join(modified_lines))

        df = pd.read_csv('temp_modified_file.csv',on_bad_lines='warn', header=None, dtype='string', encoding='Latin-1')

        #check if its tabular
        if len(df) < 22:
            raise ValueError(f"The DataFrame has {len(df)} rows, but at least 22 rows are required.")

        print(df.info())
        print(df.head())
        print(df.head(10))

        # if the cell starts with <na> or nan its the end of the row move on
        #this puts the [] of color and patterns together
        col_pat = []
        for _, row in df.iterrows():
            row_col_pat = []

            for col in range(5, len(row)):
                cell = str(row[col])
                if cell.startswith('<NA>') or cell.startswith('nan'):
                    continue
                else:
                    row_col_pat.append(cell)

            col_pat.append(" ".join(row_col_pat))

        banner_x_cord = df[0]
        banner_y_cord = df[1]
        banner_z_cord = df[2]
        banner_names = df[3].fillna('No Name')

        #create a dic for the new dataframe
        cleaned_data = {
            "x": banner_x_cord,
            "y": banner_y_cord,
            "z": banner_z_cord,
            "name": banner_names,
            "Color and Pattern": col_pat,
        }

        new_df = pd.DataFrame(cleaned_data, dtype='string')
        new_df.to_html("OW Cleaned Banner Data.html")

        x = new_df['x']
        y = new_df['y']
        z = new_df['z']
        name = new_df['name']
        color_and_Pattern = new_df['Color and Pattern']

        new_df.info()

    #if we fuck up and fail return nothing since we failed
    except Exception as e:
        print(f"Failed to Create DataFrame: {e}")
        return None, None, None, None, None, None

    return banner_x_cord.astype(int), banner_y_cord.astype(int), banner_z_cord.astype(
        int), name, color_and_Pattern, name.unique()


def get_Sign_data(filename):
    """
    The get_sign_data() function gets the signs data and removes all of the tags and unwanted info
    creates a new df of just signs and an html of the signs
    :param filename: the file being looked at
    :return:
    new_df: the new data frame
    x.astype(int): a list of the x col
    y.astype(int): a list of the y col
    z.astype(int): a list of the z col
    msg: a list of all of the messages
    glow: a list of the glow ink status
    color: a list of all the colors
    msg.unique(): a list of all of the unigue messages
    glow.unique(): a list of all the unique glow ink
    color.unique(): a list of all the unique colors
    """
    # *NOTE Pandas is fucking up x y z cords
    # nvm found the issue

    try:
        #same as above
        with open(filename, 'r', encoding='Latin-1') as file:
            lines = file.readlines()

        modified_lines = []
        for line in lines:
            columns = line.strip().split(',')

            if len(columns) < 100:
                columns.extend(['<NA>'] * (100 - len(columns)))

            modified_lines.append(','.join(columns))

        with open('temp_modified_file.csv', 'w', encoding='Latin-1') as file:
            file.writelines("\n".join(modified_lines))

        df = pd.read_csv('temp_modified_file.csv', header=None, dtype='string', encoding='Latin-1')
        print(df.head(10))  # Preview first few rows
        df.info()
        df.astype(str)


        print('Finished loading in first data set\nstarting String man')
        # took too many fucking hrs to figure this out
        #remove all the tags and other bullshit from the file
        df.replace('{"type":"ListTag"', '', inplace=True, regex=True)
        df.replace(r'\\"text\\":\\"\\\"\}"', '', inplace=True, regex=True)
        df.replace('value:{"type":"StringTag"', '', inplace=True, regex=True)
        df.replace(r'\\\\""', '', inplace=True, regex=True)
        df.replace(r']\}\}', '', inplace=True, regex=True)
        df.replace(r'list:\\', '', inplace=True, regex=True)
        df.replace(r'{\\extra\\":', '', inplace=True, regex=True)
        df.replace(r'[\\]', '', inplace=True, regex=True)
        df.replace('list:[""""]', '', inplace=True, regex=True)
        df.replace(r'{\"type":"CompoundTag"', '', inplace=True, regex=True)
        df.replace(r'{\"type":"ByteTag"', '', inplace=True, regex=True)
        df.replace(r'{\"type":"StringTag"', '', inplace=True, regex=True)
        df.replace(r'}\}\}', '', inplace=True, regex=True)
        df.replace(r'value:{\"messages":', '', inplace=True, regex=True)
        df.replace(r'list:[\""""]', '', inplace=True, regex=True)
        df.replace(r'}', '', inplace=True, regex=True)
        df.replace(r'list:[\"{\"extra":]', '', inplace=True, regex=True)
        df.replace('list:', '', inplace=True, regex=True)
        df.replace('""""', '', inplace=True, regex=True)
        df.replace(r'\[', '', inplace=True, regex=True)
        df.replace(r'\]', '', inplace=True, regex=True)
        df.replace(r'"{\"extra":', '', inplace=True, regex=True)

        print('Done With String man\nremove rows')
        # remove the last rows 32 onward since it repeats data and does not have anything of meaning
        df = df.iloc[:, :32]

        # Note need to clean up the file even more
        # remove all white space ect.

        # get x y z from the original data frame
        x_cord = df[0]
        y_cord = df[1]
        z_cord = df[2]

        print('Start cleaning up empty row ')
        glow_ink = []
        messages = []
        ink_color= []
        for _, row in df.iterrows():

            row_messages = []
            glow_ink_row = []
            ink_color_row = []
            seen_messages = set()

            for col in range(3, len(row)):
                cell = str(row[col])

                # if the cell does not start with any of the other cells it must be a msg, get the info
                if (not cell.startswith("has_glowing_text:") and not cell.startswith("color:")
                        and not cell.startswith('value:') and not cell.startswith('<NA>') and cell != 'nan'):
                    cleaned_message = cell.strip('"').strip()
                    if cleaned_message not in seen_messages:
                        row_messages.append(cleaned_message)
                        seen_messages.add(cleaned_message)

                # get the glow ink text 0 false 1 for true
                if cell.startswith("has_glowing_text:"):
                    combined_glow_ink = cell
                    if col + 1 < len(row):
                        next_cell = str(row[col + 1]).strip()
                        if next_cell.startswith("value:"):
                            combined_glow_ink += f" {next_cell}"
                    glow_ink_row.append(combined_glow_ink)

                # get the colors of the signs
                if cell.startswith("color:"):
                    combined_color = cell
                    if col + 1 < len(row):
                        next_cell = str(row[col + 1]).strip()
                        if next_cell.startswith("value:"):
                            combined_color += f" {next_cell}"
                    ink_color_row.append(combined_color)

            # combine and remove "" from the cells into one multi dem array
            ink_color.append(" ".join(ink_color_row))
            glow_ink.append(" ".join(glow_ink_row))
            messages.append(" ".join(row_messages))



        #creating a dic for the new data frame
        cleaned_data = {
            "x": x_cord,
            "y": y_cord,
            "z": z_cord,
            "mgs": messages,
            "Glow Ink": glow_ink,
            "Sign Color": ink_color
        }
        print('Create new dataframe')
        # creates a new data frame to make everything nice and org
        new_df = pd.DataFrame(cleaned_data, dtype='string')
        new_df.to_html("Cleaned Sign Data OW.html")


        x = new_df['x']
        y = new_df['y']
        z = new_df['z']
        msg = new_df['mgs']
        glow = new_df['Glow Ink']
        color = new_df['Sign Color']

        new_df.info()
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None, None, None, None

    return new_df, x.astype(int), y.astype(int), z.astype(int), msg, glow, color, msg.unique(), glow.unique(), color.unique()

def get_Cody_Signs_sorted(df):
    """
    the get_Cody_Signs_sorted, sorts the df into only cody smiles signs and then sorts it based off of date placed
    Also creates the 3d animated graph
    :param df: The data frame for signs
    :return: None
    """
    df.info()

    #look at the msgs col and and use regex to search for the date on the cody signs
    #create new col for the date
    df['date'] = df['mgs'].apply(lambda x: re.search(r'\d{1,2} \w+ \d{4}', x).group(0) if re.search(r'\d{1,2} \w+ \d{4}', x) else None)
    df['date'] = pd.to_datetime(df['date'], format='%d %b %Y', errors='coerce')

    #sort the df but date oldest to youngest
    df_sorted = df.sort_values(by='date')
    cody = df_sorted[df_sorted['mgs'].str.contains('codysmile11', na=False)]

    print(cody)
    cody.to_html('Cody_Signs_Sorted OW.html')

    #create animated graph
    threeD = ThreeDGraphsAnimated(cody, large_dataset=False)
    threeD.create_animation()
    threeD.show('End 3d Animated Cody Signs Accumulative.html')

    sign = ThreeDSigns(cody)
    sign.scatter_plot()
    sign.show('Only Cody Signs End.html')

def main():
    """
    This is the main
    """

    #filenames go here DONT USE THE SAME ONE I DID WONT WORK
    filename_banners = 'FilesBanners.csv'
    filename_signs = 'FilesSignsV2.csv'
    filename_Biome = 'D:/FilesBiomes.csv'
    filename_test = 'test.csv'
    spawn_banners = 'FileslampBanners.csv'
    spawn_Signs = 'FileslampSignsV2.csv'

    """
    =====================
           Signs
    ====================
    """

    #df, sign_x, sign_y, sign_z, msg, glow, sign_color, unique_msg, unique_glow, unique_color = get_Sign_data(spawn_Signs)

    #get_Cody_Signs_sorted(df)



    #sign_utils_color = Util(filename_signs, msg)
    #sign_data_msg, sign_keys_msg = sign_utils_color.unique_word_counter()


    #glows = TwoDGraphs(sign_data_msg, sign_keys_msg)
    #glows.create_plotly_bar_chart('OW_banners_name_Bar.html', "Amount of Colors Signs Vs. Non-Colored Signs", sign_keys_msg, sign_data_msg)

    #sign_utils_glow = Util(filename_signs, glow.astype(str))
    #sign_data_glow, sign_keys_glow = sign_utils_glow.unique_word_counter()

    #color = TwoDGraphs(sign_data_glow, sign_keys_glow)
    #color.create_plotly_bar_chart('End_Signs_glow_Bar.html', "Amount of Glow Ink Signs Vs. Non-Glow Ink Signs",
                                 #sign_keys_glow, sign_data_glow)

    #Create most words said from signs
    #sign_data, sign_keys = sign_utils.unique_word_counter()

    #sign_threeD_Graph = ThreeDGraphs(sign_x, sign_y, sign_z, msg, sign_color,pat=glow, unique_names=unique_msg, large_DataSet=True)

    #sign_threeD_Graph.scatter_Plot()
    #sign_threeD_Graph.show('OW 3d_Sign_plot1.4.html')

    title = 'All Signs In 2b End 25k'
    yLabel = 'Amount of Signs'
    xLabel = 'Name of Sign'
    overall = []

    #signs_2dGraph = TwoDGraphs(sign_data, sign_keys)
    #signs_2dGraph.Create_Bar_Charts(yLabel,xLabel,title)
    #signs_2dGraph.Create_non_log_bar(yLabel,xLabel,title)
    #signs_2dGraph.create_Percent_Pie_Chart(overall)


    """
    =====================
         Banners
    ====================
    """


    (banner_x_list, banner_y_list, banner_z_list, banner_names_list,
     banner_color_list, banners_unique_names_only) = getBannerData(filename_banners)

    sign_utils_color = Util(filename_signs, banner_color_list)
    sign_data_msg, sign_keys_msg = sign_utils_color.unique_word_counter()

    glows = TwoDGraphs(sign_data_msg, sign_keys_msg)
    glows.create_plotly_bar_chart('End_banners_color_pat_Bar.html', "Amount of Colors Signs Vs. Non-Colored Signs",
                                  sign_keys_msg, sign_data_msg)

    #utils = Util(filename_banners, banner_names_list)
    #banner_data, banner_keys = utils.unique_word_counter()

    #twoDGraph = TwoDGraphs(banner_data, banner_keys)

    #twoDGraph.Create_Bar_Charts('Amount of Banners', 'Name of Banner', 'All Banner in OW Spawn')
    #twoDGraph.Create_non_log_bar('Amount of Banners', 'Name of Banner', 'All Banner in OW Spawn')
    #twoDGraph.create_Percent_Pie_Chart(['NoName', 'PRThomass Banner', 'Rest'])

    #sign_threeD_Graph = ThreeDGraphs(banner_x_list, banner_y_list, banner_z_list, banner_names_list, banner_color_list, unique_names=banners_unique_names_only,
                                #     large_DataSet=False)

    #sign_threeD_Graph.scatter_Plot()
    #sign_threeD_Graph.show("Banners OW 1.2.html")


if __name__ == "__main__":
    main()

