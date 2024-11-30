import os
import pandas as pd
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load environment variables
load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("API_KEY"))

def convert_schema_to_sqlite(sql_schema):
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"You are an expert at converting different SQL syntaxes like 'MySQL', 'MS SQL', 'Snowflake', "
        f"'DB2', 'Hive', 'Spark', 'Redshift', 'PL/SQL', 'Clickhouse' to SQLite DBMS syntax. "
        f"Convert the following SQL schema into SQLite3 syntax, fixing any syntax errors if there are any:\n\n"
        f"{sql_schema}\n\nJust provide pure SQLite syntax code, nothing else written, ALSO take care that the sql code should not have ``` in beginning or end and sql word in output."
    )

    try:
        response = model.generate_content([prompt])
        sqlite_syntax = response.text  # Adjust indexing and key based on actual response structure
        return sqlite_syntax.strip()  # Remove any leading/trailing whitespace
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def create_sqlite_db(sqlite_schema):
    # Define the path to the SQLite file
    db_path = 'C:/Users/pranj/Downloads/Text-to-SQL-project-using-Google-Gemini-Pro-LLM-master/data/database1.db'
    
    # Remove the existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to the new database and create tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(sqlite_schema)  # Execute the schema
    conn.commit()
    conn.close()

    return db_path


def combine_files_into_db(file_paths, output_db_path):
    conn = sqlite3.connect(output_db_path)
    cursor = conn.cursor()

    for file_path in file_paths:
        # Handle .db file
        if file_path.name.endswith('.db'):
            # Save the uploaded .db file to a temporary location
            temp_db_path = os.path.join(tempfile.gettempdir(), file_path.name)
            with open(temp_db_path, 'wb') as temp_file:
                temp_file.write(file_path.read())
            
            # Now connect and backup from this temporary file
            with sqlite3.connect(temp_db_path) as db_conn:
                db_conn.backup(conn)

        # Handle .csv file
        elif file_path.name.endswith('.csv'):
            df = pd.read_csv(file_path)
            table_name = file_path.name.replace('.csv', '')
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        # Handle .xlsx file
        elif file_path.name.endswith('.xlsx'):
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df.to_sql(sheet_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()



def get_table_and_column_names(db_path):
    """
    Retrieve table names and their corresponding column names from a SQLite database.
    
    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        dict: A dictionary where the keys are table names and the values are lists of column names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Create a dictionary to store table and column names
    db_structure = {}

    for table in tables:
        table_name = table[0]
        
        # Query to get column names for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        
        # Extract column names from the result
        column_names = [column[1] for column in columns_info]
        
        # Store table name and its columns in the dictionary
        db_structure[table_name] = column_names

    # Close the database connection
    conn.close()
    
    return db_structure


def generate_sql_from_question(question, schema):
    # for written sql schema
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"Given the following database schema: \n\n{schema}\n\n and the question: \n{question}."
        f"\n\n\n\nGenerate the appropriate SQL query in SQLite syntax only. Just provide pure SQLite syntax code, nothing else written."
        f"\n\nALSO take care that the sql code should not have ``` in beginning or end and sql word in output."
        f"\n\nProvide me the SQL query for the question asked according to the database described."
    )

    try:
        response = model.generate_content([prompt])
        sql_query = response.text
        return sql_query.strip()
    except Exception as e:
        st.error(f"Error generating SQL from question: {e}")
        return None


def generate_sqlquery_from_question(question, db_structure):
    # for sql db, csv, xlsx files.
    # Format the db_structure into a readable schema format for the prompt
    schema = "The database contains the following tables and columns:\n"
    for table, columns in db_structure.items():
        schema += f"Table: {table}\n"
        schema += "Columns: " + ", ".join(columns) + "\n"
    
    # Use the schema information in the prompt for the LLM
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"Given the following database schema:\n{schema}\n"
        f"and the question:\n{question},\n"
        f"generate the appropriate SQL query in SQLite syntax only. "
        f"Just provide pure SQLite syntax code, nothing else written. "
        f"ALSO take care that the SQL code should not have '```' at the beginning or end, and no 'sql' keyword in the output."
    )

    try:
        response = model.generate_content([prompt])
        sql_query = response.text
        return sql_query.strip()
    except Exception as e:
        st.error(f"Error generating SQL from question: {e}")
        return None


def execute_sql_query(query, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Optional: Convert result to pandas DataFrame for better display
    columns = [description[0] for description in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    
    # plot_df(df)

    conn.close()
    return df


def plot_df(df):
    # df_json=df.to_json(orient='split', index=False)
    df_json=df.to_json()
    dff=json.dumps(df_json)
    # st.write(df_json)
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"You are data visualization genius who can determine best visualizations with a dataset just by looking at it."
        " Given a dataset with the (schema)name of column mentioned, and also the data of the table, analyze the dataset intelligently to determine some insightful visualizations(the graphs which could be plotted with the column of this dataset) with this data."
        "\n\nNOTE: Analyze it yourself do not show the analysis part in the response."
        "\n\nNOTE: limit the visualizations to just the columns given in dataset"
        "Here is a dataset:\n\n" + dff + 
        "\n\nNow after analyzing those possibility, just provide me a pure python code in a single piece to show all these visualizations related to the dataset"
        "\n\nALSO remove ''' from beginning or the ending of code and just provide pure python script"
        "\n\nALSO there is no need of this type data importing line df = pd.read_json(df_json) to use the dataset, the data is already stored in dataframe named df"
        "\n\nALSO use the streamlit commands to show the graph/visualizations like st.pyplot(plt) for every plot generated"
    )
    try:
        response = model.generate_content([prompt])
        generated_code = response.text  # The response should contain the Python code for visualizations
        cleaned_code = '\n'.join(generated_code.strip().split('\n')[1:-1])
        # # Print the generated Python code for debugging (optional)
        print(f"Generated python code:\n {cleaned_code}")
        #print(f"Prompt is :\n {prompt}")
        # Execute the generated Python code to create the visualizations
        exec(cleaned_code)  # Use exec to run the acquired Python code
    except SyntaxError as se:
        st.error(f"Syntax error in generated code: {se}")
    except Exception as e:
        st.error(f"Error generating visualization code: {e}")


# Streamlit layout
st.title("Text-to-Visualization")

# Option to input SQL schema or upload files
option = st.selectbox("Choose input type:", ("Upload Database Files", "Input SQL Schema"))

if option == "Input SQL Schema":
    sql_schema = st.text_area("Enter SQL Schema", height=300)
else:
    db_files = st.file_uploader("Upload database files", type=["db", "csv", "xlsx"], accept_multiple_files=True)

# Input natural language question
question = st.text_input("Enter your natural language question")

# Submit button
if st.button("Generate SQL Query"):
    if option == "Input SQL Schema" and sql_schema and question:
        # Convert schema to SQLite
        sqlite_schema = convert_schema_to_sqlite(sql_schema)
        #st.write(f"SQLite syntax:\n{sqlite_schema}")
        if sqlite_schema:  # Check if schema conversion was successful
            create_sqlite_db(sqlite_schema)
            
            # Generate SQL query
            sql_query = generate_sql_from_question(question, sqlite_schema)
            if sql_query:  # Check if SQL query generation was successful
                st.write(f"Generated SQL Query: {sql_query}")
                print("Generated SQL Query:", sql_query)
                # Execute query and display result
                db_path = 'C:/Users/pranj/Downloads/Text-to-SQL-project-using-Google-Gemini-Pro-LLM-master/data/database1.db'
                result_df = execute_sql_query(sql_query, db_path)
                st.dataframe(result_df)
                plot_df(result_df)
    
    elif db_files and question:
        output_db_path = 'C:/Users/pranj/Downloads/Text-to-SQL-project-using-Google-Gemini-Pro-LLM-master/data/database2.db'
        combine_files_into_db(db_files, output_db_path)

        db_structure = get_table_and_column_names(output_db_path)
        
        sql_query = generate_sqlquery_from_question(question, db_structure)

        if sql_query:  # Check if SQL query generation was successful
            st.write(f"Generated SQL Query: {sql_query}")
            # Execute query and display result
            result_df = execute_sql_query(sql_query, output_db_path)
            st.dataframe(result_df)
            plot_df(result_df)