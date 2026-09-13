import streamlit as st


def show_prediction(
    effort,
    cost,
    risk
):

    st.subheader(
        "Maintenance Prediction"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Effort",
        f"{effort:.2f}"
    )

    col2.metric(
        "Estimated Cost",
        f"₹{cost:,.2f}"
    )

    col3.metric(
        "Risk",
        risk
    )