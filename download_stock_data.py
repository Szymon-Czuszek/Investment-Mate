#!/usr/bin/env python
# coding: utf-8

# ###### Importing Python Libraries

# In[1]:


# Standard Libraries
import os
from functools import partial

# Numeric and Data Handling
import numpy as np
import pandas as pd
import yfinance as yf

# Data Visualization
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# GUI Libraries
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, date  # Add this line


# ###### Stock Market Analysis Class

# In[2]:


# Building the StockMarketAnalysis Class
class StockMarketAnalysis:
    """
    Perform analysis on stock market data including candlestick charts, close price evolution,
    volume distribution, and combined graphs.

    Attributes:
    - name (str): Name or identifier for the stock market analysis.
    - data (pd.DataFrame): DataFrame containing stock market data with columns:
      ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Weekday'].

    Methods:
    - __init__(self, name, symbols, start, end): Initialize the StockMarketAnalysis class with data
      downloaded from Yahoo Finance.
    - calculate_median_spread(self): Calculate the median spread between high and low prices.
    - calculate_open_std(self): Calculate the standard deviation of open prices.
    - format_y_labels(self, value, pos): Format y-axis labels for thousands, millions, and billions.
    - plot_candlestick_chart(self, ax=None): Plot a candlestick chart.
    - plot_candlestick_chart_vs_volume(self, ax=None): Plot a candlestick chart with a volume bar chart on a secondary y-axis.
    - calculate_median_spread(self): Calculate the median spread between high and low prices.
    - plot_close_price_evolution(self, ax=None): Plot the evolution of close prices with shaded price range.
    - plot_volume_distribution(self, ax=None): Plot the distribution of trading volume per weekday.
    - plot_combined_graph(self, plot_type="both"): Plot a combination of candlestick, close price, and volume graphs.
    """
    
    def __init__(self, name, symbols, start, end):
        """
        Initialize the StockMarketAnalysis class with data from Yahoo Finance.

        Args:
        - name (str): Name of the stock market analysis instance.
        - symbols (str or list of str): Ticker symbol(s) for the desired stocks.
        - start (str): Start date for fetching stock market data in "YYYY-MM-DD" format.
        - end (str): End date for fetching stock market data in "YYYY-MM-DD" format.
        
        The constructor initializes the StockMarketAnalysis object with specified name and retrieves stock market data
        using Yahoo Finance API based on the provided symbols, start, and end dates.
        The 'symbols' argument can be a single ticker symbol (str) or a list of ticker symbols.
        The retrieved data is stored in a Pandas DataFrame where the index represents the date.
        Additionally, a 'Weekday' column is created by extracting the weekday name from the 'Date' index column.
        The 'Date' column is removed as it's redundant with the index.
        """
        self.name = name
        self.data = yf.download(symbols, start = start, end = end)
        self.data["Date"] = self.data.index
        self.data["Weekday"] = self.data["Date"].apply(lambda x: x.strftime("%A"))
        del self.data["Date"]
        #self.data.set_index("Date", inplace = True)

    def calculate_median_spread(self):
        """
        Calculate the median spread between high and low prices.

        Returns:
        - float: The calculated median spread between high and low prices, rounded to two decimal places.
        
        This method computes the median spread between the high and low prices within the stored stock market data.
        It calculates the median of the 'High' and 'Low' columns separately,
        then finds the spread by subtracting the low median from the high median.
        The resulting median spread is rounded to two decimal places and returned.
        """
        high_median = np.median(self.data["High"])
        low_median = np.median(self.data["Low"])
        spread_median = high_median - low_median
        return round(spread_median, 2)

    def calculate_open_std(self):
        """
        Calculate the standard deviation of open prices.

        Returns:
        - float: The calculated standard deviation of open prices, rounded to two decimal places.
        
        This method computes the standard deviation of the 'Open' prices within the stored stock market data.
        It utilizes NumPy's std function on the 'Open' column, and the resulting standard deviation
        is rounded to two decimal places before being returned.
        """
        open_std = np.std(self.data["Open"])
        return round(open_std, 2)

    def format_y_labels(self, value, pos):
        """
        Format y-axis labels for thousands, millions, and billions.

        Args:
        - value (float): The numeric value of the y-axis label.
        - pos (int): The position of the label.

        Returns:
        - str: The formatted y-axis label.
        
        This method formats y-axis labels based on their magnitude.
        If the value is in billions, it returns the value formatted as 'X.XXB'.
        If the value is in millions, it returns the value formatted as 'X.XXM'.
        If the value is in thousands, it returns the value formatted as 'X.XXK'.
        For values less than 1,000, it returns the value as a string without formatting.
        """
        if value >= 1e9:
            return f"{value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"{value / 1e6:.2f}M"
        elif value >= 1e3:
            return f"{value / 1e3:.2f}K"
        return str(value)

    def plot_candlestick_chart(self, ax = None):
        """
        Plot a candlestick chart.

        Args:
        - ax (matplotlib.axes._subplots.AxesSubplot, optional): Matplotlib AxesSubplot to plot on.
          If not provided, a new subplot is created.

        This method generates a candlestick chart based on the 'Open', 'Close', 'High', and 'Low' prices
        stored in the class's data. Upward price movements are represented in green,
        downward movements in red. The width of each candlestick bar and shadow width are adjustable.
        Y-axis labels are formatted using the 'format_y_labels' method.
        The resulting chart is titled "Candlestick Chart" and includes grid lines.
        X-axis tick labels are rotated for better visibility.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize = (10, 5))
        
        # Style and colors
        col_up = '#4daf4a'  # Green
        col_down = '#e41a1c'  # Red
        alpha = 0.9
        width = 0.4
        shadow_width = 0.04
        
        # Plotting up price movements
        high = self.data[self.data['Close'] >= self.data['Open']]
        ax.bar(high.index,
               high['Close'] - high['Open'],
               width,
               bottom = high['Open'],
               color = col_up,
               alpha = alpha
              )
        ax.bar(high.index,
               high['High'] - high['Close'],
               shadow_width,
               bottom = high['Close'],
               color = col_up,
               alpha = alpha
              )
        ax.bar(high.index,
               high['Low'] - high['Open'],
               shadow_width,
               bottom = high['Open'],
               color = col_up,
               alpha = alpha
              )
        
        # Plotting down price movements
        low = self.data[self.data['Close'] < self.data['Open']]
        ax.bar(low.index,
               low['Close'] - low['Open'],
               width,
               bottom = low['Open'],
               color = col_down,
               alpha = alpha
              )
        ax.bar(low.index,
               low['High'] - low['Open'],
               shadow_width,
               bottom = low['Open'],
               color = col_down,
               alpha = alpha
              )
        ax.bar(low.index,
               low['Low'] - low['Close'],
               shadow_width,
               bottom = low['Close'],
               color = col_down,
               alpha = alpha
              )

        ax.set_title("Candlestick Chart")
        ax.grid(True)

        # Format y-axis labels using FuncFormatter
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_y_labels))

        # Rotate x-axis tick labels
        ax.tick_params(axis = 'x', rotation = 45)

    def plot_candlestick_chart_vs_volume(self, ax = None):
        """
        Plot a candlestick chart with a volume bar chart on a secondary y-axis.

        Args:
        - ax (matplotlib.axes._subplots.AxesSubplot, optional): Matplotlib AxesSubplot to plot on.
          If not provided, a new subplot is created.

        This method generates a candlestick chart with up and down movements represented in black and white,
        respectively. Additionally, it overlays a volume bar chart on a secondary y-axis.
        The width of each candlestick bar and shadow width are adjustable.
        Y-axis labels for the candlestick chart are formatted using the 'format_y_labels' method.
        The resulting chart is titled "Traditional Candlestick Chart vs Volume" and includes grid lines.
        X-axis tick labels are rotated for better visibility.
        Volume bars are colored green for up days and red for down days.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize = (10, 5))

        # Create a secondary y-axis (right) for volume
        ax_volume = ax.twinx()
        
        # Style and colors
        width = 0.4
        shadow_width = 0.04
        
        # Plotting up price movements
        high = self.data[self.data['Close'] >= self.data['Open']]
        ax.bar(high.index,
               high['Close'] - high['Open'],
               width,
               bottom = high['Open'],
               color = 'black'
              )
        ax.bar(high.index,
               high['High'] - high['Close'],
               shadow_width,
               bottom = high['Close'],
               color = 'black'
              )
        ax.bar(high.index,
               high['Low'] - high['Open'],
               shadow_width,
               bottom = high['Open'],
               color = 'black'
              )
        
        # Plotting down price movements
        low = self.data[self.data['Close'] < self.data['Open']]
        ax.bar(low.index,
               low['Close'] - low['Open'],
               width, bottom = low['Open'],
               color = 'white',
               edgecolor = 'black'
              )
        ax.bar(low.index,
               low['High'] - low['Open'],
               shadow_width,
               bottom = low['Open'],
               color = 'white',
               edgecolor = 'black'
              )
        ax.bar(low.index,
               low['Low'] - low['Close'],
               shadow_width,
               bottom = low['Close'],
               color = 'white',
               edgecolor = 'black'
              )

        ax.set_title("Traditional Candlestick Chart vs Volume")
        ax.grid(True)

        # Format y-axis labels for the candlestick chart
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_y_labels))

        # Rotate x-axis tick labels
        ax.tick_params(axis = 'x', rotation = 45)

        # Plot the volume as a bar chart on the secondary y-axis
        volume_colors = ['g' if c >= o else 'r'
                         for c, o in zip(self.data['Close'],
                                         self.data['Open']
                                        )
                        ]
        ax_volume.bar(self.data.index,
                      self.data['Volume'],
                      width = 0.1,
                      color = volume_colors,
                      alpha = 0.3
                     )
        ax_volume.set_ylabel("",
                             color = 'black'
                            )
        ax_volume.tick_params(axis = 'y',
                              labelcolor = 'black'
                             )
        ax_volume.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_y_labels))

    def plot_close_price_evolution(self, ax = None):
        """
        Plot the evolution of close prices with shaded price range.

        Args:
        - ax (matplotlib.axes._subplots.AxesSubplot, optional): Matplotlib AxesSubplot to plot on.
          If not provided, a new subplot is created.

        This method generates a plot showing the evolution of close prices with a shaded range
        between high and low prices. Close prices are represented in purple, and the range is shaded in pink.
        The y-axis labels are formatted using the 'format_y_labels' method.
        The resulting chart is titled "Close Price Evolution" and includes grid lines.
        X-axis tick labels are rotated for better visibility.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize = (10, 5))

            # Format y-axis labels using FuncFormatter
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_y_labels))

        col_spread = '#f781bf'  # Pink
        col_close = '#984ea3'  # Purple

        ax.plot(self.data.index,
                self.data['Close'],
                color = col_close,
                alpha = 0.5,
                label = "Close"
               )
        ax.plot(self.data.index,
                self.data['High'],
                color = col_spread,
                linestyle = ":",
                label = "High"
               )
        ax.plot(self.data.index,
                self.data['Low'],
                color = col_spread,
                linestyle = ":",
                label = "Low"
               )
        ax.fill_between(self.data.index,
                        self.data['High'],
                        self.data['Low'],
                        color = col_spread,
                        alpha = 0.1
                       )
        
        # Format y-axis tick labels using the format_y_labels function
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(self.format_y_labels))

        ax.set_title("Close Price Evolution")
        ax.grid(True)

        # Rotate x-axis tick labels
        ax.tick_params(axis = 'x', rotation = 45)

    def plot_volume_distribution(self, ax = None):
        """
        Plot the distribution of trading volume per weekday.

        Args:
        - ax (matplotlib.axes._subplots.AxesSubplot, optional): Matplotlib AxesSubplot to plot on.
          If not provided, a new subplot is created.

        This method generates a bar plot showing the distribution of trading volume for each weekday.
        Weekdays are ordered from Monday to Friday.
        The y-axis labels are formatted using the 'format_y_labels' method.
        The resulting chart is titled "Volume Distribution per Weekday" and includes grid lines.
        X-axis tick labels are not rotated.
        White lines are added between grid lines for better visibility.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize = (10, 5))

        weekdays = ["Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday"
                   ]

        # Group data by weekday and calculate the total volume for each weekday
        volume_by_weekday = self.data.groupby("Weekday")["Volume"].sum().reindex(weekdays)

        # Plot a histogram of the volume distribution per weekday
        volume_by_weekday.plot(kind = "bar",
                               ax = ax,
                               color = 'blue',
                               alpha = 0.5
                              )

        # Format y-axis tick labels using the format_y_labels function
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(self.format_y_labels))

        ax.set_title("Volume Distribution per Weekday")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.yaxis.grid(True)

        # Rotate x-axis tick labels
        ax.tick_params(axis = 'x', rotation = 0)

        # Add white lines between grid lines
        for position in ax.get_ygridlines():
            position.set_color('white')
            position.set_linewidth(2)
            
    def plot_combined_graph(self, plot_type = "both"):
        """
        Plot a combination of candlestick, close price, and volume graphs.

        Args:
        - plot_type (str, optional): Type of graphs to include. Options are "candlestick", "close_price",
          "candlestick_vs_volume", "volume_distribution", or "both". Default is "both".

        This method generates a combination of candlestick, close price evolution, and volume distribution graphs
        arranged in a 2x2 grid of subplots.
        The `plot_type` parameter allows specifying which types of graphs to include:
        - "candlestick": Candlestick chart showing price movements.
        - "close_price": Evolution of close prices with shaded price range.
        - "candlestick_vs_volume": Candlestick chart with a volume bar chart on a secondary y-axis.
        - "volume_distribution": Distribution of trading volume per weekday.
        - "both": Include all four types of graphs.

        Y-axis labels for Close Price Evolution and Volume Distribution are placed on the right side.
        The major title provides an overall analysis context with the instance's name.
        The layout is adjusted with a wider gap between the left and right side charts for better readability.
        """
        # Creating a 2x2 grid of subplots
        fig, axs = plt.subplots(2, 2, figsize = (14, 10))

        if plot_type == "candlestick" or plot_type == "both":
            self.plot_candlestick_chart(ax = axs[0, 0])
        if plot_type == "close_price" or plot_type == "both":
            self.plot_close_price_evolution(ax = axs[0, 1])
            # Adding y-axis labels for Close Price Evolution on the right side
            axs[0, 1].yaxis.tick_right()
            axs[0, 1].set_ylabel("", rotation = 270, labelpad = 20)
        if plot_type == "candlestick_vs_volume" or plot_type == "both":
            self.plot_candlestick_chart_vs_volume(ax = axs[1, 0])
        if plot_type == "volume_distribution" or plot_type == "both":
            self.plot_volume_distribution(ax = axs[1, 1])
            # Adding y-axis labels for Volume Distribution on the right side
            axs[1, 1].yaxis.tick_right()
            axs[1, 1].set_ylabel("", rotation = 270, labelpad = 20)

        # Major Title
        # Finally, the major title provides an overall analysis context.
        fig.suptitle(self.name, fontsize = 16)

        # Adjusting layout with a wider gap between the left and right side charts
        plt.tight_layout(rect = [0, 0.03, 1, 0.95])
    
        plt.show()
        
# Example usage:
# analysis = StockMarketAnalysis("Stock Data", "your_data.csv")
# analysis.plot_combined_graph(plot_type = "both")


# ###### Financial Instruments Module Class

# In[3]:


class FinancialInstrumentsModule(tk.Frame):
    """
    Tkinter-based GUI module for financial instruments analysis.

    This class represents a Tkinter frame containing various widgets for analyzing financial instruments.
    It includes functionalities for loading financial data, plotting candlestick charts, plotting close price evolution,
    and displaying information or error messages. The class utilizes the StockMarketAnalysis class for handling financial data.

    Attributes:
    - master: The Tkinter master widget.
    - analysis: An instance of the StockMarketAnalysis class for financial data analysis.
    - symbols (list): A list to store financial instrument symbols.
    - start_date: The selected start date for data analysis.
    - end_date: The selected end date for data analysis.
    - start_date_cal: Tkinter DateEntry widget for selecting the start date.
    - end_date_cal: Tkinter DateEntry widget for selecting the end date.
    - plot_frame: Tkinter frame for displaying Matplotlib plots.

    Methods:
    - load_symbols_from_file(file_path): Load financial instrument symbols from an Excel file.
    - create_widgets(): Create and configure Tkinter widgets for the GUI.
    - show_date_entry(): Enable date entry widgets and display information about the selected financial instrument.
    - load_data(): Load financial data for the selected instrument within the specified date range.
    - plot_candlestick(): Plot a candlestick chart for the selected financial instrument within the specified date range.
    - plot_close_evolution(): Plot the evolution of close prices for the selected financial instrument within the specified date range.
    - show_plot(figure): Display a Matplotlib figure within the Tkinter plot frame.
    - show_info_message(message): Display an information message using Tkinter messagebox.
    - show_error_message(message): Display an error message using Tkinter messagebox.
    """
    
    def __init__(self, master = None):
        """
        Initialize the FinancialInstrumentsModule class.

        Args:
        - master (tk.Tk, optional): The root Tkinter window. If not provided, a new window is created.
        """
        super().__init__(master)
        self.master = master
        self.pack()

        # Create a single instance of StockMarketAnalysis
        self.analysis = None

        # Initialize an empty list to store symbols from the file
        self.symbols = []

        # Load symbols from the Excel file
        file_path = os.path.join(os.getcwd(), "ISZ.xlsm")  # Your file path here
        self.load_symbols_from_file(file_path)

        self.start_date = None
        self.end_date = None
        self.start_date_cal = None
        self.end_date_cal = None
        self.plot_frame = None

        self.create_widgets()
        
    def load_symbols_from_file(self, file_path):
        """
        Load symbols from an Excel file and populate the 'symbols' attribute.

        Args:
        - file_path (str): The path to the Excel file containing symbols.

        This method attempts to load symbols from the 'Symbols' sheet of an Excel file located at the specified 'file_path'.
        The loaded symbols are assumed to be in a column named 'symbols'.
        The 'symbols' attribute of the FinancialInstrumentsModule instance is then updated with the loaded symbols as a list.

        In case of an error during loading, an exception is caught, and an error message is printed.
        """
        try:
            # Load the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path, sheet_name = 'Symbols')  # Load 'Symbols' sheet

            # Assuming the symbols are in a column named 'symbols'
            self.symbols = df['Symbols'].tolist()

        except Exception as e:
            print(f"Error loading symbols from file: {e}")
            # You might want to handle errors loading the file here

    def create_widgets(self):
        """
        Create and arrange Tkinter widgets for the GUI.

        This method initializes and arranges Tkinter widgets for the FinancialInstrumentsModule GUI.
        It creates labels, dropdowns, date entry widgets, and buttons for selecting financial instruments,
        choosing start and end dates, loading data, and triggering various plot actions.
        The widgets are organized within the Tkinter Frame.

        The 'instrument_var' attribute is created as a Tkinter StringVar and associated with a dropdown widget.
        The 'start_date_cal' and 'end_date_cal' attributes are associated with Tkinter DateEntry widgets for date selection.
        Action buttons for loading data, plotting candlestick charts, and plotting close price evolution are created.

        Note: This method checks if widgets have already been created to avoid duplicating them.
        """
        # Check if widgets have already been created
        if hasattr(self, 'instrument_var'):
            return

        label = tk.Label(self, text="Select a financial instrument:")
        label.pack(pady=10)

        self.instrument_var = tk.StringVar()
        self.instrument_var.set(self.symbols[0])
        instrument_dropdown = ttk.Combobox(self,
                                           textvariable = self.instrument_var,
                                           values = self.symbols
                                          )
        instrument_dropdown.pack(pady = 10)

        # Remove the Load Data button
        # load_button = tk.Button(self, text="Load Data", command=self.show_date_entry)
        # load_button.pack(pady=10)

        self.start_date_label = tk.Label(self,
                                         text = "Start Date:"
                                        )
        self.start_date_label.pack(pady = 5)
        self.start_date_cal = DateEntry(self,
                                        width = 12,
                                        background = 'darkblue',
                                        foreground = 'white',
                                        date_pattern = 'dd.mm.yyyy',
                                        state = 'normal'
                                       )
        self.start_date_cal.pack(pady = 5)

        self.end_date_label = tk.Label(self,
                                       text = "End Date:"
                                      )
        self.end_date_label.pack(pady = 5)
        self.end_date_cal = DateEntry(self,
                                      width = 12,
                                      background = 'darkblue',
                                      foreground = 'white',
                                      date_pattern = 'dd.mm.yyyy',
                                      state = 'normal'
                                     )
        self.end_date_cal.pack(pady = 5)

        load_data_button = tk.Button(self,
                                     text = "Load Data",
                                     command = self.load_data
                                    )
        load_data_button.pack(pady = 10)

        action_buttons_frame = tk.Frame(self)
        action_buttons_frame.pack(pady = 10)

        plot_candlestick_button = tk.Button(action_buttons_frame,
                                            text = "Plot Candlestick",
                                            command = self.plot_candlestick
                                           )
        plot_candlestick_button.pack(side = tk.LEFT, padx = 5)

        plot_close_evolution_button = tk.Button(action_buttons_frame,
                                                text = "Plot Close Evolution",
                                                command = self.plot_close_evolution
                                               )
        plot_close_evolution_button.pack(side = tk.LEFT,
                                         padx = 5
                                        )

        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack()

    def show_date_entry(self):
        """
        Enable date entry widgets and display information about the selected financial instrument.

        This method retrieves the selected financial instrument from the dropdown widget.
        If a valid instrument is selected, it enables the 'start_date_cal' and 'end_date_cal' DateEntry widgets.
        Additionally, it displays an information message indicating the selected instrument.

        Note: The information message is displayed using the 'show_info_message' method.
        """
        selected_instrument = self.instrument_var.get()
        if selected_instrument:
            self.start_date_cal.config(state = 'normal')
            self.end_date_cal.config(state = 'normal')
            self.show_info_message(f"Selected instrument: {selected_instrument}")

    def load_data(self):
        """
        Load financial data for the selected instrument within the specified date range.

        This method retrieves the selected financial instrument, start date, and end date from the respective widgets.
        It attempts to create or update an instance of the StockMarketAnalysis class with the selected instrument and date range.
        If the StockMarketAnalysis instance doesn't exist, a new instance is created. If it already exists, the instance is updated.

        The 'show_info_message' method is called to display a success message upon successful data loading.
        In case of an error during data loading, the 'show_error_message' method is called to display an error message.

        Note: The start and end dates are retrieved using the 'get_date' method of the DateEntry widgets.
        """
        selected_instrument = self.instrument_var.get()
        self.start_date = self.start_date_cal.get_date()
        self.end_date = self.end_date_cal.get_date()
        try:
            # Check if analysis instance exists
            if not self.analysis:
                self.analysis = StockMarketAnalysis(selected_instrument,
                                                    selected_instrument,
                                                    str(self.start_date),
                                                    str(self.end_date)
                                                   )
            else:
                # Update existing instance with new data
                self.analysis = None
                self.analysis = StockMarketAnalysis(selected_instrument,
                                                    selected_instrument,
                                                    str(self.start_date),
                                                    str(self.end_date)
                                                   )

            self.show_info_message("Data loaded successfully.")
        except Exception as e:
            self.show_error_message(f"Error loading data: {str(e)}")

    def plot_candlestick(self):
        """
        Plot a candlestick chart for the selected financial instrument within the specified date range.

        This method checks if both the start and end dates are available before attempting to create a new
        StockMarketAnalysis instance and plot a candlestick chart using Matplotlib. The created figure is displayed
        using the 'show_plot' method.

        If successful, an information message is displayed indicating the creation of the candlestick plot.
        In case of an error during plot creation, the 'show_error_message' method is called to display an error message.

        If the start and end dates are not available, an error message is displayed prompting the user to load data first.
        """
        if self.start_date is not None and self.end_date is not None:
            selected_instrument = self.instrument_var.get()
            try:
                analysis = StockMarketAnalysis(selected_instrument,
                                               selected_instrument,
                                               str(self.start_date),
                                               str(self.end_date)
                                              )
                figure, ax = plt.subplots(figsize = (10, 5))
                analysis.plot_candlestick_chart(ax = ax)
                self.show_plot(figure)
                self.show_info_message("Candlestick plot created.")
            except Exception as e:
                self.show_error_message(f"Error creating candlestick plot: {str(e)}")
        else:
            self.show_error_message("Please load data first.")

    def plot_close_evolution(self):
        """
        Plot the evolution of close prices for the selected financial instrument within the specified date range.

        This method checks if both the start and end dates are available before attempting to create a new
        StockMarketAnalysis instance and plot the evolution of close prices using Matplotlib. The created figure is displayed
        using the 'show_plot' method.

        If successful, an information message is displayed indicating the creation of the close evolution plot.
        In case of an error during plot creation, the 'show_error_message' method is called to display an error message.

        If the start and end dates are not available, an error message is displayed prompting the user to load data first.
        """
        if self.start_date is not None and self.end_date is not None:
            selected_instrument = self.instrument_var.get()
            try:
                analysis = StockMarketAnalysis(selected_instrument,
                                               selected_instrument,
                                               str(self.start_date),
                                               str(self.end_date)
                                              )
                figure, ax = plt.subplots(figsize = (10, 5))
                analysis.plot_close_price_evolution(ax = ax)
                self.show_plot(figure)
                self.show_info_message("Close evolution plot created.")
            except Exception as e:
                self.show_error_message(f"Error creating close evolution plot: {str(e)}")
        else:
            self.show_error_message("Please load data first.")

    def show_plot(self, figure):
        """
        Display a Matplotlib figure within the Tkinter plot frame.

        This method takes a Matplotlib figure as input and displays it within the Tkinter plot frame.
        It first clears any existing widgets within the plot frame. Then, it creates a new Tkinter canvas
        embedded with the provided figure and packs it into the plot frame.

        Args:
        - figure (matplotlib.figure.Figure): The Matplotlib figure to be displayed.

        Note: The Matplotlib figure should be created using 'plt.subplots' or an equivalent method.
        """
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master = self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

    def show_info_message(self, message):
        """
        Display an information message using Tkinter messagebox.

        This method takes a message as input and displays it as an information message using Tkinter's 'showinfo' method.

        Args:
        - message (str): The information message to be displayed.
        """
        tk.messagebox.showinfo("Info", message)

    def show_error_message(self, message):
        """
        Display an error message using Tkinter messagebox.

        This method takes an error message as input and displays it as an error message using Tkinter's 'showerror' method.

        Args:
        - message (str): The error message to be displayed.
        """
        tk.messagebox.showerror("Error", message)


# ###### Download Stock Data Module Class

# In[4]:


class DownloadStockDataModule(tk.Frame):
    """
    GUI module for downloading stock data using Yahoo Finance API.

    This class represents a tkinter Frame designed for downloading stock data. It includes entry widgets for entering
    the stock ticker, start and end dates, specifying the file path, and buttons for browsing and initiating the download.

    Methods:
    - __init__(self, master=None): Initializes the GUI elements within the frame.
    - browse_file_path(self): Opens a file dialog to browse and set the file path for saving the downloaded data.
    - download_data(self): Downloads stock data based on user input and saves it to the specified CSV file.
    - save_data_to_csv(self, data, file_path, ticker): Saves stock data to a CSV file, handling existing files.
    - show_info_message(self, message): Displays an information message box.
    - show_error_message(self, message): Displays an error message box.
    """
    
    def __init__(self, master = None):
        """
        Initialize the DownloadStockDataModule class.

        This method sets up the GUI components for downloading stock data. It creates and configures Tkinter labels,
        entry widgets, date entry widgets, and buttons for specifying the ticker, date range, file path, and initiating
        the data download process.

        Args:
        - master: The Tkinter master widget.

        Note:
        - The default file path is set to the current working directory with the file name "ISZ.csv".
        - The 'browse_file_path' method is bound to the 'Browse' button.
        - The 'download_data' method is bound to the 'Download Data' button.
        """
        super().__init__(master)
        self.master = master
        self.pack()

        self.ticker_label = tk.Label(self,
                                     text = "Enter Ticker:"
                                    )
        self.ticker_label.pack(pady = 5)

        self.ticker_entry = tk.Entry(self)
        self.ticker_entry.pack(pady = 5)

        self.start_date_label = tk.Label(self,
                                         text = "Start Date:"
                                        )
        self.start_date_label.pack(pady = 5)

        self.start_date_cal = DateEntry(self,
                                        width = 12,
                                        background = 'darkblue',
                                        foreground = 'white',
                                        date_pattern = 'dd.mm.yyyy'
                                       )
        self.start_date_cal.pack(pady = 5)

        self.end_date_label = tk.Label(self,
                                       text = "End Date:"
                                      )
        self.end_date_label.pack(pady = 5)

        self.end_date_cal = DateEntry(self,
                                      width = 12,
                                      background = 'darkblue',
                                      foreground = 'white',
                                      date_pattern = 'dd.mm.yyyy'
                                     )
        self.end_date_cal.pack(pady = 5)

        self.file_path_label = tk.Label(self,
                                        text = "File Path:"
                                       )
        self.file_path_label.pack(pady = 5)

        self.file_path_entry = tk.Entry(self,
                                        width = 40
                                       )
        self.file_path_entry.insert(0, os.path.join(os.getcwd(), "ISZ.csv"))  # Default file path with .csv extension
        self.file_path_entry.pack(pady = 5)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file_path)
        self.browse_button.pack(pady = 5)

        self.download_button = tk.Button(self, text="Download Data", command=self.download_data)
        self.download_button.pack(pady = 10)

    def browse_file_path(self):
        """
        Open a file dialog to browse and select a destination file path.

        This method activates a file dialog to allow the user to browse and select a destination file path for
        downloading stock data. If a file path is selected, it updates the corresponding entry widget with the selected path.

        Note:
        - The file dialog is configured to default to a CSV file with the extension ".csv".
        - If a file path is selected, the entry widget is updated with the selected path.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def download_data(self):
        """
        Download stock data for the specified ticker and date range to a CSV file.

        This method retrieves the ticker, start date, end date, and file path from the corresponding entry widgets.
        It then attempts to download stock data using the Yahoo Finance API within the specified date range.
        The downloaded data is saved to a CSV file at the specified file path.

        The method handles specific exceptions for TickerError (failed download) and general exceptions.
        If the download is successful, it displays an information message; otherwise, it shows an error message.

        Note:
        - The ticker is converted to uppercase for consistency.
        """
        ticker = self.ticker_entry.get().upper()
        start_date = self.start_date_cal.get_date()
        end_date = self.end_date_cal.get_date()
        file_path = self.file_path_entry.get()

        try:
            data = yf.download(ticker,
                               start = start_date,
                               end = end_date
                              )

            # Save data to a new CSV file or append to an existing file
            self.save_data_to_csv(data,
                                  file_path,
                                  ticker
                                 )

            self.show_info_message(f"Data for {ticker} downloaded and saved successfully.")
        except yf.TickerError as e:
            # Handle the specific TickerError for failed download
            error_message = f"Failed to download data for {ticker}: {str(e)}"
            self.show_error_message(error_message)
        except Exception as e:
            # Handle other exceptions
            error_message = f"Error downloading data: {str(e)}"
            self.show_error_message(error_message)

    def save_data_to_csv(self, data, file_path, ticker):
        """
        Save stock data to a CSV file, handling existing files and appending data.

        This method checks if the specified CSV file already exists. If the file exists, it reads the existing data,
        checks for the presence of the 'Source' column, and either adds the column and saves the updated data or appends
        the new data with the 'Source' column. If the file does not exist, it directly saves the data to the specified file.

        Parameters:
        - data (pd.DataFrame): The stock data to be saved.
        - file_path (str): The path to the CSV file.
        - ticker (str): The ticker symbol representing the data source.

        Note:
        - The 'Source' column is added or updated to identify the source of the data.
        """
        # Check if the file exists
        if os.path.exists(file_path):
            existing_data = pd.read_csv(file_path)
            # Check if the 'Source' column is present
            if 'Source' not in existing_data.columns:
                existing_data['Source'] = ticker
                existing_data.to_csv(file_path,
                                     index = False
                                    )
            else:
                # Append the data with the 'Source' column
                data['Source'] = ticker
                existing_data = pd.concat([existing_data, data],
                                          ignore_index = True
                                         )
                existing_data.to_csv(file_path,
                                     index = False
                                    )
        else:
            # If the file does not exist, save the data directly
            data['Source'] = ticker
            data.to_csv(file_path, index = False)

    def show_info_message(self, message):
        """
        Display an information message box.

        This method creates and displays an information message box with the specified message.

        Parameters:
        - message (str): The message to be displayed in the information message box.
        """
        tk.messagebox.showinfo("Info", message)

    def show_error_message(self, message):
        """
        Display an error message box.

        This method creates and displays an error message box with the specified message.

        Parameters:
        - message (str): The message to be displayed in the error message box.
        """
        tk.messagebox.showerror("Error", message)


# ###### Comparative Analysis Module Class

# In[5]:


class ComparativeAnalysisModule:
    """
    A class for conducting comparative analysis of closing prices for two stock tickers.

    This class provides a GUI interface for the user to input start and end dates, along with two stock tickers.
    It utilizes the yfinance library to download historical stock data for the specified tickers within the given date range.
    The class then plots the closing prices of both tickers on a logarithmic scale, allowing for visual comparison.

    Attributes:
    - master: The master widget that serves as the parent of this module.

    Methods:
    - __init__(self, master): Initializes the ComparativeAnalysisModule instance.

    - create_widgets(self): Creates and arranges the widgets for entering date ranges and stock tickers.

    - plot_data(self): Plots the comparative analysis of closing prices for the specified stock tickers within the given date range.
      Utilizes yfinance for data retrieval and Matplotlib for plotting.
    """
    
    def __init__(self, master):
        """
        Initialize the ComparativeAnalysisModule.

        Parameters:
        - master: The master window in which the module will be created.
        """
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets for the comparative analysis module.

        This method creates and configures DateEntry widgets for start and end dates, Entry widgets for entering
        stock tickers, and a Button to trigger data download and plot. It packs the widgets onto the grid within the
        master window.

        Widgets:
        - Start Date Entry (DateEntry): Widget for selecting the start date.
        - End Date Entry (DateEntry): Widget for selecting the end date.
        - Ticker 1 Entry (Entry): Widget for entering the first stock ticker.
        - Ticker 2 Entry (Entry): Widget for entering the second stock ticker.
        - Plot Button (Button): Button for triggering data download and plot.
        """
        # DateEntry widgets for start and end dates
        start_date_label = tk.Label(self.master,
                                    text = "Start Date:"
                                   )
        self.start_date_entry = DateEntry(self.master,
                                          width = 12,
                                          background = 'darkblue',
                                          foreground = 'white',
                                          borderwidth = 2,
                                          date_pattern = 'dd.mm.yyyy'
                                         )
        end_date_label = tk.Label(self.master,
                                  text = "End Date:"
                                 )
        self.end_date_entry = DateEntry(self.master,
                                        width = 12,
                                        background = 'darkblue',
                                        foreground = 'white',
                                        borderwidth = 2,
                                        date_pattern = 'dd.mm.yyyy'
                                       )

        # Entry widgets for entering stock tickers
        self.ticker1_entry = tk.Entry(self.master,
                                      width = 10
                                     )
        self.ticker2_entry = tk.Entry(self.master,
                                      width = 10
                                     )

        # Button to trigger data download and plot
        plot_button = tk.Button(self.master,
                                text = "Plot",
                                command = self.plot_data
                               )

        # Pack widgets onto the grid
        start_date_label.grid(row = 0,
                              column = 0,
                              padx = 10,
                              pady = 10
                             )
        self.start_date_entry.grid(row = 0,
                                   column = 1,
                                   padx = 10,
                                   pady = 10
                                  )
        end_date_label.grid(row = 1,
                            column = 0,
                            padx = 10,
                            pady = 10
                           )
        self.end_date_entry.grid(row = 1,
                                 column = 1,
                                 padx = 10,
                                 pady = 10
                                )
        tk.Label(self.master,
                 text = "Ticker 1:").grid(row = 2,
                                          column = 0,
                                          padx = 10,
                                          pady = 10
                                         )
        self.ticker1_entry.grid(row = 2,
                                column = 1,
                                padx = 10,
                                pady = 10
                               )
        tk.Label(self.master,
                 text = "Ticker 2:").grid(row = 3,
                                          column = 0,
                                          padx = 10,
                                          pady = 10
                                         )
        self.ticker2_entry.grid(row = 3,
                                column = 1,
                                padx = 10,
                                pady = 10
                               )
        plot_button.grid(row = 4,
                         column = 0,
                         columnspan = 2,
                         pady = 10
                        )

    def plot_data(self):
         """
        Plot comparative analysis of closing prices for two stock tickers.

        Retrieves stock tickers, start and end dates from corresponding widgets. Downloads historical stock data
        for the specified tickers within the given date range using yfinance. Plots the closing prices of both
        tickers on a logarithmic scale with different colors.

        Raises:
        - yfinance.TickerError: If there is an issue with downloading data for the specified ticker(s).
        - Exception: For other unexpected errors during the data download and plotting process.
        """
        ticker1 = self.ticker1_entry.get()
        ticker2 = self.ticker2_entry.get()
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")

        # Download data using yfinance
        data1 = yf.download(ticker1,
                            start = start_date,
                            end = end_date
                           )
        data2 = yf.download(ticker2,
                            start = start_date,
                            end = end_date
                           )

        # Plot on a log scale with specified colors
        plt.figure(figsize = (8, 6))
        plt.plot(data1['Close'],
                 label = ticker1,
                 color = 'seagreen'
                )
        plt.plot(data2['Close'],
                 label = ticker2,
                 color = 'magenta'
                )
        plt.yscale('log')  # Log scale
        plt.title(f"Comparative Analysis: {ticker1} vs {ticker2}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price (log scale)")
        plt.legend()
        
         # Tilt x-axis labels in the plot area
        plt.xticks(rotation = 45)

        # Embed the plot in the tkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(),
                                   master = self.master
                                  )
        canvas.draw()
        canvas.get_tk_widget().grid(row = 5,
                                    column = 0,
                                    columnspan = 2,
                                    padx = 10,
                                    pady = 10
                                   )


# ###### Stock Portfolio Analysis Module Class

# In[6]:


class StockPortfolioAnalysis(tk.Frame):
    """
    A class for analyzing a stock portfolio and displaying relevant information and plots.

    This class loads portfolio data from an Excel file, preprocesses the data, calculates profit/loss for each ticker,
    identifies open and closed positions, displays portfolio summary information, and plots the stock prices of all tickers
    within the portfolio using the Matplotlib library.

    Attributes:
    - master: The master widget that serves as the parent of this module.

    Methods:
    - __init__(self, master=None): Initializes the StockPortfolioAnalysis instance, loads data, preprocesses it,
      calculates profit/loss, shows portfolio summary, and plots all tickers.

    - process_duplicated_tickers(self): Processes duplicated tickers by sorting the data and creating a 'Dup' column.

    - calculate_profit_loss(self): Calculates profit/loss for each ticker by fetching historical data from Yahoo Finance.

    - show_portfolio_info(self): Displays profit/loss and position status for each ticker in the portfolio.

    - plot_all_tickers(self): Plots the stock prices of all tickers within the portfolio using Matplotlib.
    """
    
    def __init__(self, master = None):
        """
        Initializes the StockPortfolioAnalysis instance, loads portfolio data, preprocesses it, calculates profit/loss,
        shows portfolio summary, and plots all tickers.

        Parameters:
        - master: The master widget that serves as the parent of this module.

        This constructor performs the following tasks:
        1. Calls the constructor of the parent class (tk.Frame) with the specified master widget.
        2. Packs the frame within the parent widget.
        3. Loads portfolio data from an Excel file ('ISZ.xlsm') into a Pandas DataFrame.
        4. Preprocesses the data by filling blank end dates with today's date.
        5. Processes duplicated tickers, indicating sell and buy back transactions.
        6. Calculates profit/loss for each ticker by fetching historical data from Yahoo Finance.
        7. Displays profit/loss and position status for each ticker in the portfolio.
        8. Plots the stock prices of all tickers within the portfolio using Matplotlib.

        Note: The path to the Excel file and sheet name are assumed to be 'ISZ.xlsm' and 'Portfolio', respectively.
        """
        super().__init__(master)
        self.master = master
        self.pack()

        # Load data from Excel file
        self.data = pd.read_excel(os.path.join(os.getcwd(), "ISZ.xlsm"), sheet_name = 'Portfolio')

        # Preprocess data: Fill blank end dates with today's date
        self.data['End Date'].fillna(date.today(), inplace = True)

        # Process duplicated tickers (indicating sell and buy back)
        self.process_duplicated_tickers()

        # Calculate profit/loss for each ticker
        self.calculate_profit_loss()

        # Display profit/loss, open/closed positions on the app
        self.show_portfolio_info()

        # Plot all tickers within the app
        self.plot_all_tickers()

    def process_duplicated_tickers(self):
        """
        Processes duplicated tickers in the portfolio data.

        The method performs the following tasks:
        1. Sorts the portfolio data by 'Ticker' and 'Start Date'.
        2. Identifies duplicated tickers using the Pandas `duplicated` method.
        3. Assigns a cumulative sum to the 'Dup' column to distinguish between different instances of duplicated tickers.
        """
        # Sort data by Ticker and Start Date
        self.data = self.data.sort_values(by = ['Ticker', 'Start Date'])

        # Process duplicated tickers
        self.data['Dup'] = self.data.duplicated(subset = 'Ticker', keep = False)
        self.data['Dup'] = self.data['Dup'].cumsum()

    def calculate_profit_loss(self):
        """
        Calculates profit or loss for each ticker in the portfolio.

        The method performs the following tasks:
        1. Iterates over each row in the portfolio data.
        2. Fetches historical stock data from Yahoo Finance for the specified ticker, start date, and end date.
        3. Calculates the profit or loss as the difference between the closing prices at the start and end dates.
        4. Assigns the calculated profits to the 'Profit/Loss' column in the dataframe.
        5. Identifies open and closed positions in the 'Position' column based on the end date.
        """
        # Calculate profit/loss for each ticker
        profits = []
        for index, row in self.data.iterrows():
            ticker = row['Ticker']
            start_date = row['Start Date']
            end_date = row['End Date']

            # Fetch historical data from Yahoo Finance
            stock_data = yf.download(ticker,
                                     start = start_date,
                                     end = end_date
                                    )

            # Calculate profit/loss
            start_price = stock_data.iloc[0]['Open']
            end_price = stock_data.iloc[-1]['Close']
            profit_loss = end_price - start_price  # Profit/Loss as a number
            profits.append(profit_loss)

        # Assign calculated profits to the dataframe
        self.data['Profit/Loss'] = profits

        # Identify open and closed positions
        self.data['Position'] = 'Closed'
        self.data.loc[self.data['End Date'] == date.today(), 'Position'] = 'Open'

    def show_portfolio_info(self):
        """
        Displays the profit/loss and position status summary for each ticker in the portfolio.

        The method creates a Tkinter label widget and displays the portfolio summary, including ticker symbols,
        profit or loss, and position status (open or closed). The summary is formatted as a string and set as the text
        content of the label.
        """
        # Display profit/loss and position status on the app
        label_text = f"Portfolio Summary:\n{self.data[['Ticker', 'Profit/Loss', 'Position']].to_string(index = False)}"
        label = tk.Label(self.master, text = label_text)
        label.pack()

    def plot_all_tickers(self):
        """
        Plots the stock prices of all tickers in the portfolio using Matplotlib.

        The method utilizes a PortfolioAnalyzer to download historical stock data for each ticker,
        and then creates a Matplotlib figure to visualize the closing prices. The closing prices are
        plotted on the y-axis against the corresponding dates on the x-axis. Gaps in the data are masked
        for a cleaner visualization.
        """
        analyzer = PortfolioAnalyzer(self.data)
        stock_data = analyzer.download_data()
        fig, ax = plt.subplots(figsize = (10, 6))

        # Your existing plotting logic
        for ticker, data in stock_data.items():
            gap_indices = np.isnan(data['Close'])
            ax.plot(data['Close'], label = ticker)
            ax.plot(data['Close'].mask(gap_indices), color = 'none')

        ax.set_title('Portfolio Stock Prices')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master = self.master)
        canvas.draw()
        canvas.get_tk_widget().pack()  # Pack the Matplotlib canvas into your Tkinter GUI


# ###### Portfolio Analyzer Class

# In[7]:


class PortfolioAnalyzer:
    """
    A class for analyzing and plotting stock portfolio data.

    Parameters:
    - file_path (str): The file path of the Excel file containing portfolio data.

    Example:
    ```
    analyzer = PortfolioAnalyzer(file_path = 'portfolio_data.xlsx')
    stock_data = analyzer.download_data()
    analyzer.plot_stock_data(stock_data)
    ```
    """
    
    def __init__(self, file_path):
        """
        Initializes the PortfolioAnalyzer with portfolio data from the specified Excel file.

        Parameters:
        - file_path (str): The file path of the Excel file containing portfolio data.
        """
        self.data = pd.read_excel(file_path, sheet_name = 'Portfolio')

    def download_data(self):
        """
        Downloads historical stock data for each ticker in the portfolio.

        Returns:
        dict: A dictionary containing historical stock data for each ticker.

        Example:
        ```
        analyzer = PortfolioAnalyzer(file_path = 'portfolio_data.xlsx')
        stock_data = analyzer.download_data()
        ```
        """
        unique_tickers = self.data['Ticker'].unique()
        stock_data = {}
        
        start_dates = []
        end_dates = []
        
        for ticker in unique_tickers:
            ticker_data = self.data[self.data['Ticker'] == ticker]
            ticker_stock_data = []
            
            for i in range(len(ticker_data)):
                start_date = ticker_data.iloc[i]['Start Date']
                if pd.isnull(start_date):
                    start_date = pd.to_datetime('today')
                end_date = ticker_data.iloc[i]['End Date'] if not pd.isnull(ticker_data.iloc[i]['End Date'])                     else pd.to_datetime('today')
                
                stock = yf.download(ticker,
                                    start = start_date,
                                    end = end_date
                                   )
                ticker_stock_data.append(stock)
                
                start_dates.append(stock.index.min())
                end_dates.append(stock.index.max())
                
            stock_data[ticker] = pd.concat(ticker_stock_data)
        
        overall_start = min(start_dates)
        overall_end = max(end_dates)
        overall_stock_data = {}
        
        for ticker, data in stock_data.items():
            data = data.reindex(pd.date_range(overall_start, overall_end))
            overall_stock_data[ticker] = data
        
        return overall_stock_data
    
    def plot_stock_data(self, stock_data):
        """
        Plots the historical stock prices for each ticker in the portfolio.

        Parameters:
        - stock_data (dict): A dictionary containing historical stock data for each ticker.

        Example:
        ```
        analyzer = PortfolioAnalyzer(file_path = 'portfolio_data.xlsx')
        stock_data = analyzer.download_data()
        analyzer.plot_stock_data(stock_data)
        ```
        """
        plt.figure(figsize = (10, 6))
        plt.title('Portfolio Stock Prices')
        plt.xlabel('Date')
        plt.ylabel('Price')
        
        plot_handles = []  # to store legend handles for visible lines
        plot_labels = []   # to store legend labels for visible lines
        
        for ticker, data in stock_data.items():
            gap_indices = np.isnan(data['Close'])
            line, = plt.plot(data['Close'], label = ticker)
            plot_handles.append(line)
            plot_labels.append(ticker)
            plt.plot(data['Close'].mask(gap_indices), color = 'none')  # Plot invisible line for gaps
        
        plt.legend(plot_handles, plot_labels)
        plt.show()


# ###### Main Menu Class

# In[8]:


class MainMenu(tk.Tk):
    """
    The main application window for the Financial Analysis App.

    Example:
    ```
    main_app = MainMenu()
    main_app.mainloop()
    ```

    Attributes:
    - notebook (ttk.Notebook): A notebook widget for storing different modules.
    - modules (dict): A dictionary to store instances of opened modules.

    Methods:
    - open_module(module_name): Opens a new module in the notebook.

    Example:
    ```
    main_app = MainMenu()
    main_app.open_module("Preview Data Module")
    ```
    """
    
    def __init__(self):
        """
        Initializes the main application window for the Financial Analysis App.

        Example:
        ```
        main_app = MainMenu()
        main_app.mainloop()
        ```
        """
        super().__init__()

        self.title("Financial Analysis App")

        # Add Notebook for module storage
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill = tk.BOTH, expand = 1)

        # Horizontal buttons for each module
        module_names = [
            "Preview Data Module",
            "Download Data Module",
            "Comparative Analysis Module",
            "Stock Portfolio Analysis"
        ]

        self.modules = {}

        for module_name in module_names:
            module_button = tk.Button(
                self,
                text = module_name,
                command = lambda name = module_name: self.open_module(name)
            )
            module_button.pack(side = tk.LEFT,
                               padx = 10,
                               pady = 10
                              )

    def open_module(self, module_name):
        """
        Opens a new module in the notebook.

        Parameters:
        - module_name (str): The name of the module to be opened.

        Example:
        ```
        main_app = MainMenu()
        main_app.open_module("Preview Data Module")
        ```
        """
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == module_name:
                return

        module_instance = ttk.Frame(self.notebook)
        self.notebook.add(module_instance, text = module_name)

        if module_name == "Preview Data Module":
            financial_instruments_module = FinancialInstrumentsModule(module_instance)
        elif module_name == "Download Data Module":
            download_stock_data_module = DownloadStockDataModule(module_instance)
        elif module_name == "Comparative Analysis Module":
            comparative_analysis_module = ComparativeAnalysisModule(module_instance)
        elif module_name == "Stock Portfolio Analysis":
            stock_portfolio_module = StockPortfolioAnalysis(module_instance)


# ###### Running The App

# In[9]:


class DownloadStockDataModule(tk.Frame):
    """
    A module for downloading stock data and saving it to a CSV file.

    Example:
    ```
    download_module = DownloadStockDataModule()
    download_module.mainloop()
    ```

    Attributes:
    - ticker_label (tk.Label): Label for entering the stock ticker.
    - ticker_entry (tk.Entry): Entry widget for entering the stock ticker.
    - start_date_label (tk.Label): Label for selecting the start date.
    - start_date_cal (DateEntry): DateEntry widget for selecting the start date.
    - end_date_label (tk.Label): Label for selecting the end date.
    - end_date_cal (DateEntry): DateEntry widget for selecting the end date.
    - file_path_label (tk.Label): Label for entering the file path.
    - file_path_entry (tk.Entry): Entry widget for entering the file path.
    - browse_button (tk.Button): Button for browsing and selecting the file path.
    - download_button (tk.Button): Button for initiating the data download.

    Methods:
    - browse_file_path(): Opens a file dialog for browsing and selecting the file path.
    - download_data(): Downloads stock data based on user input and saves it to a CSV file.
    - save_data_to_csv(data, file_path, ticker): Saves stock data to a CSV file.
    - show_info_message(message): Displays an information message.
    - show_error_message(message): Displays an error message.

    Example:
    ```
    download_module = DownloadStockDataModule()
    download_module.download_data()
    ```
    """
    
    def __init__(self, master = None):
        """
        Initializes the main application window for the Financial Analysis App.

        Example:
        ```
        main_app = MainMenu()
        main_app.mainloop()
        ```
        """
        super().__init__(master)
        self.master = master
        self.pack()

        self.ticker_label = tk.Label(self,
                                     text = "Enter Ticker:"
                                    )
        self.ticker_label.pack(pady = 5)

        self.ticker_entry = tk.Entry(self)
        self.ticker_entry.pack(pady = 5)

        self.start_date_label = tk.Label(self,
                                         text = "Start Date:"
                                        )
        self.start_date_label.pack(pady = 5)

        self.start_date_cal = DateEntry(self,
                                        width = 12,
                                        background = 'darkblue',
                                        foreground = 'white',
                                        date_pattern = 'dd.mm.yyyy'
                                       )
        self.start_date_cal.pack(pady = 5)

        self.end_date_label = tk.Label(self,
                                       text = "End Date:"
                                      )
        self.end_date_label.pack(pady = 5)

        self.end_date_cal = DateEntry(self,
                                      width = 12,
                                      background = 'darkblue',
                                      foreground = 'white',
                                      date_pattern = 'dd.mm.yyyy'
                                     )
        self.end_date_cal.pack(pady = 5)

        self.file_path_label = tk.Label(self,
                                        text = "File Path:"
                                       )
        self.file_path_label.pack(pady = 5)

        self.file_path_entry = tk.Entry(self,
                                        width = 40
                                       )
        self.file_path_entry.insert(0, os.path.join(os.getcwd(), "ISZ.csv"))  # Default file path with .csv extension
        self.file_path_entry.pack(pady = 5)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file_path)
        self.browse_button.pack(pady = 5)

        self.download_button = tk.Button(self, text="Download Data", command=self.download_data)
        self.download_button.pack(pady = 10)

    def browse_file_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def download_data(self):
        ticker = self.ticker_entry.get().upper()
        start_date = self.start_date_cal.get_date()
        end_date = self.end_date_cal.get_date()
        file_path = self.file_path_entry.get()

        try:
            data = yf.download(ticker,
                               start = start_date,
                               end = end_date
                              )

            # Save data to a new CSV file or append to an existing file
            self.save_data_to_csv(data,
                                  file_path,
                                  ticker
                                 )

            self.show_info_message(f"Data for {ticker} downloaded and saved successfully.")
        except yf.TickerError as e:
            # Handle the specific TickerError for failed download
            error_message = f"Failed to download data for {ticker}: {str(e)}"
            self.show_error_message(error_message)
        except Exception as e:
            # Handle other exceptions
            error_message = f"Error downloading data: {str(e)}"
            self.show_error_message(error_message)

    def save_data_to_csv(self, data, file_path, ticker):
        # Check if the file exists
        if os.path.exists(file_path):
            existing_data = pd.read_csv(file_path)
            # Check if the 'Source' and 'Date' columns are present
            if 'Source' not in existing_data.columns:
                existing_data['Source'] = ticker
                existing_data['Date'] = data.index.date  # Adding the date column
                existing_data.to_csv(file_path, index = False)
            else:
                # Append the data with the 'Source' and 'Date' columns
                data['Source'] = ticker
                data['Date'] = data.index.date  # Adding the date column
                existing_data = pd.concat([existing_data, data], ignore_index = True)
                existing_data.to_csv(file_path, index = False)
        else:
            # If the file does not exist, save the data directly
            data['Source'] = ticker
            data['Date'] = data.index.date  # Adding the date column
            data.to_csv(file_path, index = False)

    def show_info_message(self, message):
        tk.messagebox.showinfo("Info", message)

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)


# In[10]:


if __name__ == "__main__":
    os.chdir(r"C:\Users\User\FinancialAnalysisApp")
    main_menu = MainMenu()
    main_menu.mainloop()


# ###### The End
