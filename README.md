Stock Market Data Engineering Pipeline
Overview

This project processes daily stock market data and converts it into monthly summaries for 10 different tickers. It then calculates a set of technical indicators on top of the monthly data.

The input dataset contains daily trading information — open, high, low, close, adjusted close, volume, and ticker. The pipeline loads and prepares the data, resamples daily records into monthly records, computes technical indicators using the monthly values, and writes one output CSV file per ticker.

Built as a Data Engineering assignment, the project focuses on:

Daily-to-monthly data transformation
Correct monthly OHLC aggregation
Rolling and exponential calculations using Pandas
Processing each ticker independently
Modular Python code structure
Output validation and automated testing
Assignment Objective

Take a two-year daily stock dataset and produce monthly data with the following technical indicators:

Simple Moving Averages (SMA)
Exponential Moving Averages (EMA)
Donchian Channels
Bollinger Bands
Z-Score

The pipeline flow looks like this:

Daily CSV Data
      │
      ▼
Load the data
      │
      ▼
Convert and sort dates
      │
      ▼
Process each ticker separately
      │
      ▼
Aggregate daily data into monthly data
      │
      ▼
Calculate technical indicators
      │
      ▼
Create one CSV per ticker
      │
      ▼
Validate the generated files
Stocks Covered

The dataset contains these 10 tickers:

AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA

The input covers two years of daily data, so each ticker produces 24 monthly records.

Input Data

The pipeline reads from:

data/output_file.csv

The input CSV contains the following columns:

Column	Description
date	Trading date
volume	Daily trading volume
open	Opening price
high	Highest price during the day
low	Lowest price during the day
close	Closing price
adjclose	Adjusted closing price
ticker	Stock symbol
Data Processing Steps
1. Load the Data

The pipeline reads the CSV file using Pandas and loads it into a DataFrame.

2. Prepare the Data

The date column is converted to Pandas datetime format. The data is then sorted by ticker and date. Sorting is important because the project performs time-series and rolling calculations.

3. Process Each Ticker

Each ticker is processed separately. This allows the pipeline to generate one output file per stock.

Monthly Aggregation

Daily records are resampled into monthly records using the following rules:

Field	Monthly Calculation
Open	Open price from the first trading day of the month
High	Maximum daily High during the month
Low	Minimum daily Low during the month
Close	Close price from the last trading day of the month
Adj Close	Adjusted close from the last trading day of the month
Volume	Sum of daily volume during the month

The important point here is that Open and Close are not averages. Monthly Open is the first trading day's opening price, and Monthly Close is the last trading day's closing price.

Technical Indicators

All technical indicators are calculated after converting daily data into monthly data. This means the rolling windows below represent months, not individual trading days.

Simple Moving Average (SMA)

Two SMAs are calculated from the monthly closing price:

SMA_10 — average of the previous 10 monthly closing prices
SMA_20 — average of the previous 20 monthly closing prices
Exponential Moving Average (EMA)

Two EMAs are calculated using Pandas ewm():

EMA_10 — 10-month span
EMA_20 — 20-month span
Donchian Channels

The assignment provides the following type of calculation:

h.rolling(n).max()
l.rolling(n).min()

Since the assignment does not specify the value of n, a 20-month lookback window is used. Three columns are generated:

Column	Calculation
Donchian_Upper	Rolling maximum of the monthly High over 20 months
Donchian_Lower	Rolling minimum of the monthly Low over 20 months
Donchian_Middle	(Donchian Upper + Donchian Lower) / 2

Note: The Donchian Upper uses the monthly High column, not the Close. The Donchian Lower uses the monthly Low column, not the Close. This matches the standard Donchian Channel definition and the assignment's h.rolling(n).max() / l.rolling(n).min() formula.

Bollinger Bands

Bollinger Bands are calculated using a 20-month rolling window and a 2× standard deviation multiplier:

Column	Calculation
BB_Middle	20-month rolling mean of Close
BB_Upper	BB Middle + 2 × rolling standard deviation
BB_Lower	BB Middle − 2 × rolling standard deviation
Z-Score

The Z-Score is calculated using a 20-month rolling window:

Z-Score = (Close − Rolling Mean) / Rolling Standard Deviation
Handling Initial NaN Values

Some indicators need a certain number of previous observations before they can produce a result. For example, a 20-month SMA needs 20 monthly closing prices. This means the first 19 months do not have enough historical data, and those cells are NaN.

These NaN values are intentionally kept. The rows are not removed and the values are not imputed. This is because the assignment requires exactly 24 monthly rows for every ticker, so dropping incomplete rows would change the row count.

For reference:

Indicator	First valid value appears at
SMA_10	Month 10
SMA_20	Month 20
Donchian Channels	Month 20
Bollinger Bands	Month 20
Z-Score	Month 20
EMA_10 / EMA_20	Month 1 (Pandas ewm() can compute from partial data)
Output

The pipeline generates 10 separate CSV files, stored inside output/:

result_AAPL.csv
result_AMD.csv
result_AMZN.csv
result_AVGO.csv
result_CSCO.csv
result_MSFT.csv
result_NFLX.csv
result_PEP.csv
result_TMUS.csv
result_TSLA.csv

Each file contains exactly 24 rows, representing the 24 months in the input period.

Output Columns
Column	Description
date	End-of-month date
ticker	Stock symbol
open	First trading day's Open
high	Maximum High during the month
low	Minimum Low during the month
close	Last trading day's Close
adjclose	Last trading day's adjusted close
volume	Total monthly trading volume
SMA_10	10-month Simple Moving Average of Close
SMA_20	20-month Simple Moving Average of Close
EMA_10	10-month Exponential Moving Average of Close
EMA_20	20-month Exponential Moving Average of Close
Donchian_Upper	Highest monthly High in the 20-month window
Donchian_Lower	Lowest monthly Low in the 20-month window
Donchian_Middle	Midpoint of Donchian Upper and Lower
BB_Middle	20-month rolling mean of Close
BB_Upper	Bollinger upper band (middle + 2 × std dev)
BB_Lower	Bollinger lower band (middle − 2 × std dev)
Z_Score	Rolling Z-Score of the monthly Close
Project Structure
assignment_fam/
│
├── data/
│   └── output_file.csv
│
├── output/
│   ├── result_AAPL.csv
│   ├── result_AMD.csv
│   ├── result_AMZN.csv
│   ├── result_AVGO.csv
│   ├── result_CSCO.csv
│   ├── result_MSFT.csv
│   ├── result_NFLX.csv
│   ├── result_PEP.csv
│   ├── result_TMUS.csv
│   └── result_TSLA.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── aggregation.py
│   ├── indicators.py
│   └── pipeline.py
│
├── tests/
│   ├── __init__.py
│   ├── test_aggregation.py
│   ├── test_indicators.py
│   └── test_pipeline.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
What Each File Does
File	Purpose
main.py	Entry point — starts the complete pipeline
src/config.py	Ticker list, SMA/EMA windows, Donchian/Bollinger/Z-Score parameters
src/utils.py	Helper functions for loading, preparing, saving, and validating data
src/aggregation.py	Daily-to-monthly resampling logic
src/indicators.py	SMA, EMA, Donchian, Bollinger, and Z-Score calculations (each in its own function)
src/pipeline.py	Connects all the pieces — loads, prepares, aggregates, calculates, saves, validates
Configuration

All tuneable parameters live in src/config.py:

SMA windows          = 10, 20
EMA windows          = 10, 20
Donchian window      = 20 months
Bollinger window     = 20 months
Bollinger multiplier = 2
Z-Score window       = 20 months

The Donchian, Bollinger, and Z-Score windows are practical assumptions because the assignment does not specify exact values for all of these parameters.

To change any of these, edit src/config.py and rerun the pipeline. No other code changes are needed.

Installation and Setup
Requirements
Python 3.8 or later
pip
Steps

Clone the repository

bash
git clone https://github.com/ArunAllu07/assignment_fam.git
cd assignment_fam

Create a virtual environment (recommended)

bash
python -m venv venv

Activate it:

bash
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

Install the dependencies

bash
pip install -r requirements.txt

The requirements.txt contains:

pandas — data loading, resampling, and indicator calculations
pytest — automated testing (used only for tests, not for the data pipeline itself)
Running the Pipeline

From the project root:

bash
python main.py

The script reads data/output_file.csv, processes every ticker listed in src/config.py, and writes the results to output/. Each ticker gets its own file named result_<TICKER>.csv.

If the pipeline finishes without errors, a validation summary is printed confirming that all output files were created with the expected number of rows.

Running the Tests
bash
python -m pytest -v
What the Tests Cover
Test File	What It Checks
test_aggregation.py	Monthly resampling produces correct OHLCV values from synthetic daily data
test_indicators.py	All expected indicator columns are present after calculation
test_pipeline.py	Each ticker's output file exists, has the right number of rows, and contains the correct columns
Validation

The pipeline validates that every ticker produces exactly 24 rows:

AAPL: 24 rows — PASS
AMD:  24 rows — PASS
AMZN: 24 rows — PASS
AVGO: 24 rows — PASS
CSCO: 24 rows — PASS
MSFT: 24 rows — PASS
NFLX: 24 rows — PASS
PEP:  24 rows — PASS
TMUS: 24 rows — PASS
TSLA: 24 rows — PASS
Technologies Used
Technology	Purpose
Python	Main programming language
Pandas	Data loading, resampling, and calculations
pytest	Automated testing
Git	Version control
GitHub	Code repository

The core data-processing logic uses Pandas only and does not rely on any external technical-analysis library.

Practical Assumptions

The following assumptions were made during implementation:

Technical indicators are calculated after daily data is converted to monthly data.
Donchian Channel uses a 20-month rolling window applied to monthly High and Low.
Bollinger Bands use a 20-month rolling window with a 2× multiplier.
Z-Score uses a 20-month rolling window.
Initial rolling NaN values are retained — rows are not removed because every ticker must contain exactly 24 monthly records.
Monthly volume is calculated as the sum of daily volume.
Monthly adjusted close is taken from the last trading day of the month.
Data is sorted by ticker and date before any time-series calculations.
Possible Improvements
Add validation for duplicate or missing dates in the input data
Allow input and output paths to be passed as command-line arguments
Add logging for pipeline execution steps
Add more unit tests for individual indicator calculations
Add visualizations for the generated monthly data
Set up a CI workflow (GitHub Actions) to run tests automatically on each push

These improvements are outside the basic requirements of the assignment.

Repository

GitHub: https://github.com/ArunAllu07/assignment_fam