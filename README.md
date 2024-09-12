# Human Language to SQL Query Translator

This project allows users to input queries in natural language (via text or voice) and translates them into SQL queries. It then executes these queries on a MySQL database and displays the results.

## Features

- Text input for natural language queries
- Voice input for natural language queries (with speech-to-text conversion)
- SQL query generation from natural language
- Execution of generated SQL queries on a MySQL database
- Display of query results in a Streamlit interface

## Prerequisites

- Python 3.7+
- MySQL database
- Streamlit
- PyTorch
- Whisper
- Vanna
- mysql-connector-python

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Melsa16/Voice-to-SQL.git
   cd Voice-to-SQL
   ```

2. Install the required packages:
   ```
   pip install whisper streamlit torch pandas audiorecorder vanna mysql-connector-python
   ```
  Note: You may need to install additional dependencies depending on your system configuration.

3. Set up your configuration:
   - Copy `sql_vanna_config_template.py` to `sql_vanna_config.py`
   - Fill in your MySQL and Vanna API credentials in `sql_vanna_config.py`

## Usage

1. Start the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Choose between text input or voice input for your query.

3. Enter your query in natural language.

4. View the generated SQL query and the results of its execution.

## Configuration

This project uses a `sql_vanna_config.py` file to store sensitive information. Make sure to keep this file secure and never commit it to version control. A template (`sql_vanna_config_template.py`) is provided for reference.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
