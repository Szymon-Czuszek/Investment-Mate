# 📊 Investment Mate - Investment Analysis Tool

Investment Mate is a powerful investment analysis tool designed to enhance decision-making processes for traders and investors. This comprehensive suite of functionalities focuses on stock analysis, portfolio management, and data visualization, with a primary emphasis on European, S&P 500, and Polish markets.

## 🔍 Key Features

**📈 Stock Analysis Modules:** Conduct detailed analyses of individual stocks, utilizing candlestick and high-low-close charts for comprehensive insights into stock volatility.

```python
# Example code snippet for stock analysis
analysis = StockMarketAnalysis("AAPL", "Apple Inc.", "2022-01-01", "2022-12-31")
analysis.plot_candlestick_chart()
```

**⚖️ Comparative Analysis:** Easily compare two stocks using logarithmic scale charts, aiding in volatility assessment and trend identification.

```python
# Example code snippet for comparative analysis
comparative_module = ComparativeAnalysisModule(master)
comparative_module.create_widgets()
```

**💼 Portfolio Summary:** Effectively manage investment portfolios, summarizing profits/losses for each position through an Excel-based data management system.

```python
# Example code snippet for portfolio summary
portfolio_analyzer = StockPortfolioAnalysis(master)
portfolio_analyzer.show_portfolio_info()
```

**📥 Data Retrieval:** Seamlessly retrieve market data by specifying date ranges and stock tickers, generating CSV files for Excel integration.

```python
# Example code snippet for data retrieval
download_module = DownloadStockDataModule(master)
download_module.download_data()
```

## 🎯 Project Goals

**Efficient Analysis:** Simplify and accelerate the analysis of stock prices and portfolio performance for better decision-making.

**User-Friendly Interface:** Provide an intuitive and user-friendly platform for comprehensive data visualization and analysis.

**Data Accessibility:** Ensure easy access to updated market information for informed investment decisions.

**Continual Improvement:** Foster ongoing development for expanded functionalities and an enhanced user experience.

## 🛣️ Future Roadmap

**Expanded Data Sources:** Integrate with additional financial data platforms to enable more extensive market analysis.

**Diversified Instrument Support:** Extend functionality to analyze various financial instruments beyond stocks.

**Automated Data Updates:** Optimize the data update process for real-time or scheduled updates.

## 🤝 Contribution

Contributions, suggestions, and feedback are highly encouraged to further refine and improve Investment Mate, making it an indispensable tool for investors and traders.

## Get Started

Explore the repository, contribute to its development, or leverage its capabilities to bolster your investment strategies!
