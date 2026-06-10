import customtkinter as ctk
import subprocess
import threading
import socket
import platform
import getpass
import speedtest
import sqlite3
import time
from datetime import datetime

# Optional graph support
try:
    import matplotlib.pyplot as plt
    GRAPH_OK = True
except:
    GRAPH_OK = False


# ================= THEME =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

output_box = None


# ================= DATABASE =================
conn = sqlite3.connect("network_logs.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    type TEXT,
    data TEXT
)
""")
conn.commit()


def log_event(log_type, data):
    cursor.execute(
        "INSERT INTO logs (time, type, data) VALUES (?, ?, ?)",
        (str(datetime.now()), log_type, data)
    )
    conn.commit()


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


# ================= OUTPUT =================
def write(text):
    output_box.insert("end", text + "\n")
    output_box.see("end")


def clear():
    output_box.delete("1.0", "end")


# ================= RUN COMMAND =================
def run_command(cmd):
    clear()

    def task():
        try:
            result = subprocess.check_output(cmd, shell=True, text=True)
            write(result)
            log_event("CMD", cmd)
        except Exception as e:
            write(str(e))

    threading.Thread(target=task).start()


# ================= SPEED TEST =================
def speed_test():
    clear()

    def task():
        try:
            write("Running speed test...\n")

            st = speedtest.Speedtest()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            ping = st.results.ping

            result = f"{download:.2f},{upload:.2f},{ping:.2f}"
            log_event("SPEED", result)

            write(f"Download: {download:.2f} Mbps")
            write(f"Upload: {upload:.2f} Mbps")
            write(f"Ping: {ping:.2f} ms")

        except Exception as e:
            write(str(e))

    threading.Thread(target=task).start()


# ================= PING TEST =================
def ping_test():
    clear()

    def task():
        try:
            result = subprocess.check_output("ping google.com -n 4", shell=True, text=True)
            write(result)
            log_event("PING", "google.com")
        except Exception as e:
            write(str(e))

    threading.Thread(target=task).start()


# ================= PORT SCANNER =================
def port_scan():
    clear()

    def task():
        target = "127.0.0.1"
        write(f"Scanning ports on {target}...\n")

        open_ports = []

        for port in range(20, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05)

            if sock.connect_ex((target, port)) == 0:
                write(f"Port {port} OPEN")
                open_ports.append(port)

            sock.close()

        log_event("PORT_SCAN", str(open_ports))
        write("\nScan complete.")

    threading.Thread(target=task).start()


# ================= DIAGNOSTIC =================
def diagnose():
    clear()
    write("Running full diagnosis...\n")

    write(f"PC: {platform.node()}")
    write(f"User: {getpass.getuser()}")
    write(f"Local IP: {get_local_ip()}")
    write(f"External IP: {get_external_ip()}")

    run_command("ipconfig")


# ================= EXPORT =================
def export_report():
    data = output_box.get("1.0", "end")

    with open("NetworkReport.txt", "a", encoding="utf-8") as f:
        f.write("\n\n====================\n")
        f.write(str(datetime.now()) + "\n")
        f.write(data)

    write("Report exported.")


# ================= GRAPH =================
def show_graph():
    if not GRAPH_OK:
        write("Matplotlib not installed.")
        return

    cursor.execute("SELECT data FROM logs WHERE type='SPEED'")
    rows = cursor.fetchall()

    if not rows:
        write("No speed data found.")
        return

    downloads = []
    uploads = []

    for r in rows:
        try:
            d, u, p = r[0].split(",")
            downloads.append(float(d))
            uploads.append(float(u))
        except:
            pass

    plt.plot(downloads, label="Download")
    plt.plot(uploads, label="Upload")
    plt.legend()
    plt.title("Speed History")
    plt.show()


# ================= MAIN APP =================
app = ctk.CTk()
app.title("Network Toolkit v3")
app.geometry("950x850")


ctk.CTkLabel(
    app,
    text="Network Toolkit v3 (Pro)",
    font=("Arial", 24, "bold")
).pack(pady=10)


frame = ctk.CTkFrame(app)
frame.pack(pady=10)


buttons = [
    ("Run Diagnosis", diagnose),
    ("Speed Test", speed_test),
    ("Ping Test", ping_test),
    ("Port Scan", port_scan),
    ("IP Config", lambda: run_command("ipconfig /all")),
    ("Flush DNS", lambda: run_command("ipconfig /flushdns")),
    ("Renew IP", lambda: run_command("ipconfig /renew")),
    ("Show Graph", show_graph),
    ("Export Report", export_report),
]


for text, cmd in buttons:
    ctk.CTkButton(frame, text=text, width=260, command=cmd).pack(pady=5)


output_box = ctk.CTkTextbox(app, width=900, height=400)
output_box.pack(pady=20)


ctk.CTkButton(app, text="Exit", command=app.destroy).pack(pady=10)

app.mainloop()