import streamlit as st
import socket
import platform
import getpass
import subprocess
import speedtest

# ================= PAGE =================
st.set_page_config(page_title="Network Toolkit v5", layout="wide")


# ================= LOGIN SYSTEM =================
def login():
    st.title("🔐 Login to Network Toolkit")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["auth"] = True
        else:
            st.error("Invalid credentials")


if "auth" not in st.session_state:
    login()
    st.stop()


# ================= MAIN DASHBOARD =================
st.title("🌐 Network Toolkit v5 - Secure Dashboard")


# ================= SYSTEM INFO =================
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


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


# ================= SPEED TEST =================
if st.button("⚡ Run Speed Test"):
    st.info("Running speed test...")

    stest = speedtest.Speedtest()
    download = stest.download() / 1_000_000
    upload = stest.upload() / 1_000_000
    ping = stest.results.ping

    st.success("Completed")
    st.metric("Download Mbps", round(download, 2))
    st.metric("Upload Mbps", round(upload, 2))
    st.metric("Ping ms", round(ping, 2))


# ================= NETWORK TOOLS =================
st.subheader("🛠 Network Tools")

if st.button("IP Config"):
    output = subprocess.getoutput("ipconfig")
    st.text(output)

if st.button("Flush DNS"):
    output = subprocess.getoutput("ipconfig /flushdns")
    st.text(output)

if st.button("Ping Google"):
    output = subprocess.getoutput("ping google.com -n 4")
    st.text(output)


# ================= LOGOUT =================
if st.button("🚪 Logout"):
    st.session_state["auth"] = False
    st.rerun()