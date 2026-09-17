# Python Data Processing Pipeline

## Project Overview

This project is a Python-based data processing pipeline that reads raw data from a CSV file, cleans and transforms the data, and generates a structured output CSV file.

The pipeline also includes logging and configuration management to make the project easier to maintain and monitor.

## Features

- Read data from CSV files
- Handle missing values
- Convert data types
- Handle invalid data
- Transform data
- Generate structured output
- Add salary categories
- Maintain pipeline logs
- Use JSON configuration
- Simple and modular Python code

## Project Structure

```text
yuvtech/
│
├── input.csv
├── output.csv
├── README.md
│
├── config/
│   └── config.json
│
├── logs/
│   └── pipeline.log
│
└── src/
    ├── reader.py
    ├── cleaner.py
    ├── transformer.py
    ├── pipeline.py
    └── logger.py