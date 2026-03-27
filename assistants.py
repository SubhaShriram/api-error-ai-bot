import streamlit as st
import pandas as pd
from openai import OpenAI

# Secure OpenAI connection
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load CSV knowledge base
data = pd.read_csv("Apierrors.csv")

# Convert CSV to text for GPT
knowledge = data.to_string()

# Load assistant instructions
with open("assistant_instruction.txt", "r") as f:
    instructions = f.read()

# Streamlit UI
st.title("API Error AI Assistant")

query = st.text_input("Describe the API error or ask your question")

if query:

    prompt = f"""
{instructions}

Knowledge Base:
{knowledge}

User Question:
{query}

FORMAT RESPONSE EXACTLY LIKE THIS:

Error Code: <value>
Error Title: <value>
Error Message: <value>

**Root Cause**
<root cause explanation>

**Solution**
<solution steps in new lines or bullet points>
"""

    # OpenAI request
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    st.markdown("### Assistant Response")

    # Display formatted response
    st.markdown(answer, unsafe_allow_html=True)
