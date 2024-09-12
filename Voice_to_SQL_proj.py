import whisper
import streamlit as st
import torch
import pandas as pd
from audiorecorder import audiorecorder
import vanna
from vanna.remote import VannaDefault
import mysql.connector
from sql_vanna_config import DB_CONFIG, VANNA_CONFIG


# Connect to MySQL database
conn = mysql.connector.connect(**DB_CONFIG)

cursor = conn.cursor()
c1 = conn.cursor()

vn = VannaDefault(model=VANNA_CONFIG['model_name'], api_key=VANNA_CONFIG['api_key'])

vn.connect_to_mysql(**DB_CONFIG)
df_collegedb_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

######################### Training the LLM ###########################
# This will break up the information schema into bite-sized chunks that can be referenced by the LLM
#plan = vn.get_training_plan_generic(df_collegedb_schema)
#plan

# Uncomment this and run it to train the model
#vn.train(plan=plan)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model("base.en").to(device)

st.title("Human Language to SQL Query Translator")
st.write("## Select an option: ")

choice = st.radio("",
    ["Voice Input", "Text Input"],
    captions = ["Input via voice to perform queries on table.", "Input via text to perform queries on table."])

if choice=="Text Input":
    tint=st.text_input("Enter Text: "," ")
    if not tint:
        st.write("Please input: ")
        exit(0)
    x=vn.generate_sql(tint)
    st.write(x)
    query=x.replace('\n',' ')

    split_query=x.split()

    if (split_query[0].lower() == "select"):
        cursor.execute(query)
        df=pd.DataFrame (cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        st.dataframe(df, use_container_width=True)
    elif ("CREATE DATABASE" in query):
        cursor.execute(query)
        conn.commit()
        st.write("Database has been created.")
    elif ("USE" in query):
        cursor.execute(query)
        conn.commit()
        st.write("")
    elif ("DROP" in query):
        cursor.execute(query)
        conn.commit()
        st.write("Table has been deleted.")
    else:
        cursor.execute(query)
        conn.commit()

        l1=[]
        retrieve_tables="show tables"
        c1.execute(retrieve_tables) 
        for i in c1:
            l1.append(i[0])
        
        for j in l1:                         #cursor: UPDATE students SET name = 'Joseph' WHERE name = 'Bob';
            if j in query:                      #l1: ['classes', 'colleges', 'professors', 'students']``
                q1="select * from %s" % j
                cursor.execute(q1)
                rows = cursor.fetchall()                            # Convert rows to a pandas DataFrame
                columns = [desc[0] for desc in cursor.description]  # Get column names from cursor description
                df = pd.DataFrame(rows, columns=columns)

        st.dataframe(df, use_container_width=True)

if choice=="Voice Input":
    audio = audiorecorder("Record", "Stop Recording")

    if len(audio) > 0:
        st.write("Input audio is: ")
        st.audio(audio.export().read())  
        audio.export("voiceinput.wav", format="wav")
        model=whisper.load_model("base")
        result=model.transcribe("voiceinput.wav")

        st.write("Transcribed text is: ")
        st.write(result["text"])

        x=vn.generate_sql(result["text"])
        st.write(x)
        query=x.replace('\n',' ')

        split_query=x.split()

        if (split_query[0].lower() == "select"):
            cursor.execute(query)
            df=pd.DataFrame (cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            st.dataframe(df, use_container_width=True)
        elif ("CREATE DATABASE" in query):
            cursor.execute(query)
            conn.commit()
            st.write("Database has been created.")
        elif ("USE" in query):
            cursor.execute(query)
            conn.commit()
            st.write("")
        elif ("DROP" in query):
            cursor.execute(query)
            conn.commit()
            st.write("Table has been deleted.")
        else:
            cursor.execute(query)
            conn.commit()

            l1=[]
            retrieve_tables="show tables"
            c1.execute(retrieve_tables) 
            for i in c1:
                l1.append(i[0])
            
            for j in l1:                         #cursor: UPDATE students SET name = 'Joseph' WHERE name = 'Bob';
                if j in query:                      #l1: ['classes', 'colleges', 'professors', 'students']``
                    q1="select * from %s" % j
                    cursor.execute(q1)
                    rows = cursor.fetchall()                            # Convert rows to a pandas DataFrame
                    columns = [desc[0] for desc in cursor.description]  # Get column names from cursor description
                    df = pd.DataFrame(rows, columns=columns)

            st.dataframe(df, use_container_width=True)