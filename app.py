# Main Streamlit App Entry Point
import streamlit as st
from estimations import run_estimations

def main():
    st.title("AI-Powered Effort Estimation Tool")
    st.write("Upload requirements or paste text to begin.")
    run_estimations()

if __name__ == "__main__":
    main()
