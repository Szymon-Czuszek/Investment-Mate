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
    
    def __init__(self, name, symbols, start, end):
        """
        Initialize the StockMarketAnalysis class with data from a CSV file.
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
        """
        high_median = np.median(self.data["High"])
        low_median = np.median(self.data["Low"])
        spread_median = high_median - low_median
        return round(spread_median, 2)

    def calculate_open_std(self):
        """
        Calculate the standard deviation of open prices.
        """
        open_std = np.std(self.data["Open"])
        return round(open_std, 2)

    def format_y_labels(self, value, pos):
        """
        Format y-axis labels for thousands, millions, and billions.
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
    def __init__(self, master = None):
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
        try:
            # Load the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path, sheet_name = 'Symbols')  # Load 'Symbols' sheet

            # Assuming the symbols are in a column named 'symbols'
            self.symbols = df['Symbols'].tolist()

        except Exception as e:
            print(f"Error loading symbols from file: {e}")
            # You might want to handle errors loading the file here

    def create_widgets(self):
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
        selected_instrument = self.instrument_var.get()
        if selected_instrument:
            self.start_date_cal.config(state = 'normal')
            self.end_date_cal.config(state = 'normal')
            self.show_info_message(f"Selected instrument: {selected_instrument}")

    def load_data(self):
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
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master = self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

    def show_info_message(self, message):
        tk.messagebox.showinfo("Info", message)

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)


# ###### Download Stock Data Module Class

# In[4]:


class DownloadStockDataModule(tk.Frame):
    def __init__(self, master = None):
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
        tk.messagebox.showinfo("Info", message)

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)


# ###### Comparative Analysis Module Class

# In[5]:


class ComparativeAnalysisModule:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
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
    def __init__(self, master = None):
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
        # Sort data by Ticker and Start Date
        self.data = self.data.sort_values(by = ['Ticker', 'Start Date'])

        # Process duplicated tickers
        self.data['Dup'] = self.data.duplicated(subset = 'Ticker', keep = False)
        self.data['Dup'] = self.data['Dup'].cumsum()

    def calculate_profit_loss(self):
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
        # Display profit/loss and position status on the app
        label_text = f"Portfolio Summary:\n{self.data[['Ticker', 'Profit/Loss', 'Position']].to_string(index = False)}"
        label = tk.Label(self.master, text = label_text)
        label.pack()

    def plot_all_tickers(self):
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
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path, sheet_name = 'Portfolio')

    def download_data(self):
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
    def __init__(self):
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
    def __init__(self, master = None):
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
