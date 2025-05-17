import streamlit as st
from pages import candidate_mode, manager_mode

def main():
    st.sidebar.title("Select Mode")
    mode = st.sidebar.selectbox("Choose mode", ["Candidate Mode", "Manager Mode"])

    if mode == "Candidate Mode":
        candidate_mode.candidate_mode()
    else:
        manager_mode.manager_mode()

if __name__ == "__main__":
    main()
