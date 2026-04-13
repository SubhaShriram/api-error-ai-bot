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

query = st.text_input("Describe the API error or ask your question and press the Enter Key")

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


# -------------------------------
# Add New Error to Knowledge Base
# -------------------------------

st.markdown("### Add New Error to Knowledge Base")

with st.form("add_error_form"):
    error_code = st.text_input("Error Code")
    error_title = st.text_input("Error Title")
    error_message = st.text_input("Error Message")
    root_cause = st.text_area("Root Cause")
    solution = st.text_area("Solution")

    submit = st.form_submit_button("Save to Knowledge Base")

if submit:
    if error_code and error_title:
        # Create new row
        new_row = {
            "Error Code": error_code,
            "Error Title": error_title,
            "Error Message": error_message,
            "Root Cause": root_cause,
            "Solution": solution
        }

        # Append to existing dataframe
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

        # Save back to CSV
        data.to_csv("Apierrors.csv", index=False)

        st.success("New error added successfully!")

        # Reload updated knowledge (optional but useful)
        data = pd.read_csv("Apierrors.csv")
        knowledge = data.to_string()

    else:
        st.error("Please fill at least Error Code and Error Title.")
