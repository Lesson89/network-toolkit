import streamlit as st
import socket
import platform
import getpass
import subprocess

st.set_page_config(page_title="Network Toolkit", layout="wide")

# ================= LOGIN =================
def login():
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state["auth"] = True
        else:
            st.error("Wrong credentials")

if "auth" not in st.session_state:
    login()
    st.stop()

# ================= DASHBOARD =================
st.title("🌐 Network Toolkit (Cloud Version)")

st.write("App is running successfully ✔")

st.subheader("System Info")
st.write("PC:", platform.node())
st.write("User:", getpass.getuser())
st.write("Local IP:", socket.gethostbyname(socket.gethostname()))

# ================= SAFE COMMANDS =================
if st.button("Ping Google"):
    result = subprocess.getoutput("ping google.com -n 4")
    st.text(result)

if st.button("IP Config"):
    result = subprocess.getoutput("ipconfig")
    st.text(result)

st.success("Dashboard loaded successfully")