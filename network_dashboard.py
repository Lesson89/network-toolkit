import streamlit as st
import socket
import platform
import getpass
import subprocess

# ================= PAGE =================
st.set_page_config(page_title="Network Toolkit", layout="wide")


# ================= LOGIN =================
def login():
    st.title("🔐 Network Toolkit Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["auth"] = True
        else:
            st.error("Invalid login")


if "auth" not in st.session_state:
    login()
    st.stop()


# ================= MAIN APP =================
st.title("🌐 Network Toolkit Dashboard (Stable Version)")


# ================= SYSTEM INFO =================
def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"


def get_external_ip():
    try:
        import urllib.request
        return urllib.request.urlopen("https://api.ipify.org").read().decode()
    except:
        return "Unavailable"


col1, col2, col3 = st.columns(3)

col1.metric("PC Name", platform.node())
col2.metric("User", getpass.getuser())
col3.metric("Local IP", get_local_ip())

st.write("External IP:", get_external_ip())


# ================= NETWORK TOOLS =================
st.subheader("🛠 Network Tools")

if st.button("IP Config"):
    result = subprocess.getoutput("ipconfig")
    st.text(result)

if st.button("Ping Google"):
    result = subprocess.getoutput("ping google.com -n 4")
    st.text(result)

if st.button("Flush DNS"):
    result = subprocess.getoutput("ipconfig /flushdns")
    st.text(result)


# ================= DIAGNOSTIC =================
st.subheader("🧠 Quick Diagnosis")

if st.button("Run Diagnosis"):
    st.write("Checking system...")
    st.write("Checking network...")
    st.write("Checking IP...")

    result = subprocess.getoutput("ipconfig")
    st.text(result)


# ================= FOOTER =================
st.markdown("---")
st.write("Network Toolkit - Stable Cloud Version ✔")