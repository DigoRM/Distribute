#Library imports
import pandas as pd
import numpy as np
import streamlit as st
import base64
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Customer Integration Members
customer_integration =['Duda','Heberte','Matt','Rodrigo']

#Setting Title of App
st.title("Tasks Distribution - CI")
st.markdown("Upload the csv file with all orders CI has to integrate.")

#Uploading the dog image
demands = st.file_uploader("Upload csv file...", type="csv")
submit = st.button('Distribute')
#On predict button click
if submit:


    if demands is not None:

        df = pd.read_csv(demands)

        # Group df by parceiro column
        df_grouped = df.groupby('parceiro').agg({'order_id':'count'}).reset_index()
        

        # shuffle the columns randomly
        df_grouped = df_grouped.sample(frac=1, random_state=42)

        # shuffle the list randomly
        np.random.shuffle(customer_integration)

        # split the demands dataframe randomly into equal sized groups
        group_size = len(df_grouped) // len(customer_integration)
        groups = np.array_split(df_grouped, len(customer_integration))

        # assign each group of demands to a member
        for i, group in enumerate(groups):
            group["member"] = customer_integration[i]

        # concatenate the groups back into a single dataframe
        df_grouped_member_distributed = pd.concat(groups)

        # print the resulting dataframe
        st.markdown("Here is how the demands are distributed between members, for each partner.")
        df_grouped_member_distributed

        df_final = pd.merge(df,df_grouped_member_distributed,how='inner', on='parceiro')
        df_final = df_final.sort_values("member",ascending=True).drop('order_id_y', axis=1)
        st.markdown("Here is the file with all the orders distributed, respecting the distribution of members between partners")
        df_final

        st.write('Download the file with all orders distributed:')
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')


        csv = convert_df(df_final)

        st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )

        def send_email_distributed_tasks(member_email,df):
            # Set up email server and message
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('rodrigo.marcolino@appmax.com.br', '#Bento110615')
            msg = MIMEMultipart()
            msg['From'] = 'rodrigo.marcolino@appmax.com.br'
            msg['To'] = member_email
            msg['Subject'] = 'Your report is ready!'

            # Convert dataframe to CSV and attach to email message
            csv = MIMEApplication(df.to_csv(index=False), _subtype='csv')
            csv.add_header('Content-Disposition', 'attachment', filename='report.csv')
            msg.attach(csv)

            # Send email
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()


        df_duda = df_final.query("member == 'Duda'")
        send_email_distributed_tasks('eduarda.gomes@appmax.com.br',df_duda)

        df_heberte = df_final.query("member == 'Heberte'")
        send_email_distributed_tasks('heberte.anjos@appmax.com.br',df_heberte)

        df_matt = df_final.query("member == 'Matt'")
        send_email_distributed_tasks('matheus.victoria@appmax.com.br',df_matt)

        df_rodrigo = df_final.query("member == 'Rodrigo'")
        send_email_distributed_tasks('rodrigo.marcolino@appmax.com.br',df_rodrigo)

        send_email_distributed_tasks('joaoschutz@appmax.com.br',df_final)
    
