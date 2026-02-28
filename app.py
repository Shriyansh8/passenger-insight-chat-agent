import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Passenger Insight Chat Agent", page_icon="🚢")

st.title("🚢 Passenger Insight Chat Agent")

df = sns.load_dataset("titanic")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask something about the Titanic dataset..."):

    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Bot response logic
    response_text = ""
    fig = None

    if "percentage" in prompt_lower and "male" in prompt_lower:
        total = len(df)
        males = len(df[df["sex"] == "male"])
        percent = (males / total) * 100
        response_text = f"📊 Percentage of male passengers: **{percent:.2f}%**"

    elif "average" in prompt_lower and "fare" in prompt_lower:
        avg_fare = df["fare"].mean()
        response_text = f"💰 Average ticket fare: **{avg_fare:.2f}**"

    elif "embarked" in prompt_lower:
        embarked_counts = df["embarked"].value_counts()
        response_text = "🚢 Passengers from each embarkation port:"
        fig, ax = plt.subplots()
        embarked_counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("Number of Passengers")

    elif "histogram" in prompt_lower and "age" in prompt_lower:
        response_text = "📈 Age Distribution Histogram:"
        fig, ax = plt.subplots()
        sns.histplot(df["age"].dropna(), bins=20, ax=ax)

    elif "survived" in prompt_lower:
        survived_counts = df["survived"].value_counts()
        response_text = "🛟 Survival Count:"
        fig, ax = plt.subplots()
        survived_counts.plot(kind="bar", ax=ax)
        ax.set_xticklabels(["Did Not Survive", "Survived"], rotation=0)

    else:
        response_text = "❓ Sorry, I don't understand that question yet."

    # Show bot message
    with st.chat_message("assistant"):
        st.markdown(response_text)
        if fig:
            st.pyplot(fig)

    # Store bot response
    st.session_state.messages.append({"role": "assistant", "content": response_text})