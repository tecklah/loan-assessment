import streamlit as st
import uuid
import agent

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("Hello, how can I assist you with your loan application assessment today?")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def onclick_button_session():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []

button_session = st.sidebar.button('New Session', on_click=onclick_button_session)
st.sidebar.write(f"Session ID: {st.session_state.session_id}")

if prompt := st.chat_input("Enter your loan application assessment query here..."):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = agent.run_agent(prompt, st.session_state.session_id)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})