import streamlit as st
from backend import register_user, login_user

st.set_page_config(
    page_title="Login App",
    layout="centered"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():

    st.title("⚡ AI Employability")

    tab1,tab2 = st.tabs([
        "Login",
        "Register"
    ])

    # LOGIN
    with tab1:

        username = st.text_input(
            "Username",
            key="login_user"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            if login_user(
                username,
                password
            ):

                st.session_state.logged_in=True
                st.success("Login Success")
                st.rerun()

            else:
                st.error("Wrong username/password")

    # REGISTER
    with tab2:

        username = st.text_input(
            "Create Username",
            key="reg_user"
        )

        password = st.text_input(
            "Create Password",
            type="password",
            key="reg_pass"
        )

        if st.button("Register"):

            if register_user(
                username,
                password
            ):

                st.success(
                    "Registered successfully"
                )

            else:
                st.error(
                    "User already exists"
                )


def dashboard():

    st.title("Dashboard")

    st.success(
        "You are logged in"
    )

    if st.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()


if st.session_state.logged_in:
    dashboard()
else:
    login()
