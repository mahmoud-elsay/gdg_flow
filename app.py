import streamlit as st
import requests

# API Endpoints
CHAT_API_URL = "https://cridguard-430965227338.us-central1.run.app/chat"
PREDICT_API_URL = "https://gdg-430965227338.us-central1.run.app//predict"

# --- Sidebar for Feature Selection ---
st.sidebar.title("Features")
feature = st.sidebar.selectbox("Choose a feature", ["Chatbot", "Loan Prediction"])

# --- Chatbot Feature ---
if feature == "Chatbot":
    st.title("Coin Guard Chatbot 🤖")
    st.markdown(
        """
        <style>
        .chat-container {
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 5px;
        }
        .user {
            background-color: #f0f0f0;
        }
        .bot {
            background-color: #e6f7ff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Your message:", key="user_input")

    if st.button("Send") and user_input:
        # Send the user input to the chatbot API
        response = requests.post(CHAT_API_URL, json={"user_input": user_input})
        if response.status_code == 200:
            data = response.json()
            chat_history = data.get("chat_history", [])
            st.session_state.chat_history = chat_history

            # Display chat history with a small SVG icon for the bot responses
            for chat in st.session_state.chat_history:
                if chat["role"] == "user":
                    st.markdown(
                        f'<div class="chat-container user">🧑‍💻 {chat["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    with st.container():
                        col1, col2 = st.columns([1, 8])
                        with col1:
                            st.image("coin_chatbot.svg", width=30)  # small SVG icon
                        with col2:
                            st.markdown(
                                f'<div class="chat-container bot">{chat["content"]}</div>',
                                unsafe_allow_html=True,
                            )
        else:
            st.error("Error fetching response from the Chatbot API")

# --- Loan Prediction Feature ---
elif feature == "Loan Prediction":
    st.title("Loan Recommendation Prediction")
    st.write("Enter the following details to get a loan recommendation:")

    # Use a form for better layout and UX
    with st.form("loan_form"):
        col1, col2 = st.columns(2)
        with col1:
            id_val = st.number_input("ID", value=1, step=1)
            duration = st.number_input("Duration in months", value=36, step=1)
            credit_history = st.selectbox("Credit history", options=[0, 1], index=1)
            purpose_credit = st.number_input("Purpose of the credit", value=2, step=1)
            credit_amount = st.number_input("Credit amount", value=5000, step=100)
            savings_status = st.number_input(
                "Status of savings account/bonds", value=2, step=1
            )
            present_employment = st.number_input(
                "Present employment (years)", value=3, step=1
            )
            installment_rate = st.number_input(
                "Installment rate (% of disposable income)", value=4, step=1
            )
            personal_status = st.number_input("Personal status", value=0, step=1)
            other_debtors = st.selectbox(
                "Other debtors/guarantors", options=[0, 1], index=1
            )
        with col2:
            present_residence = st.number_input(
                "Present residence (years)", value=2, step=1
            )
            property_val = st.number_input("Property", value=1, step=1)
            age = st.number_input("Age in years", value=35, step=1)
            other_installment = st.number_input(
                "Other installment plans (banks/stores)", value=0, step=1
            )
            housing = st.selectbox("Housing", options=[0, 1], index=1)
            num_existing_credits = st.number_input(
                "Number of existing credits at this bank", value=2, step=1
            )
            job = st.number_input("Job", value=1, step=1)
            num_people_liable = st.number_input(
                "Number of people being liable to provide maintenance for",
                value=1,
                step=1,
            )
            telephone = st.selectbox("Telephone", options=[0, 1], index=0)
            foreign_worker = st.selectbox("Foreign worker", options=[0, 1], index=1)

        submitted = st.form_submit_button("Submit")

    if submitted:
        payload = {
            "id": id_val,
            "Duration in months": duration,
            "Credit history": credit_history,
            "Purpose of the credit": purpose_credit,
            "Credit amount": credit_amount,
            "Status of savings account/bonds": savings_status,
            "Present employment(years)": present_employment,
            "Installment rate in percentage of disposable income": installment_rate,
            "personal_status": personal_status,
            "Other debtors / guarantors": other_debtors,
            "Present residence since X years": present_residence,
            "Property": property_val,
            "Age in years": age,
            "Other installment plans (banks/stores)": other_installment,
            "Housing": housing,
            "Number of existing credits at this bank": num_existing_credits,
            "Job": job,
            "Number of people being liable to provide maintenance for": num_people_liable,
            "Telephone": telephone,
            "Foreign worker": foreign_worker,
        }
        with st.spinner("Fetching loan recommendation..."):
            response = requests.post(PREDICT_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success("Prediction received!")
            st.markdown("---")
            st.subheader("Loan Recommendation")
            st.write(data.get("Loan_Recommendation", "N/A"))
            st.write("Raw Prediction:", data.get("Raw_Prediction", "N/A"))
            st.write("Risk Category:", data.get("Risk_Category", "N/A"))
        else:
            st.error("Error fetching prediction from the API")
