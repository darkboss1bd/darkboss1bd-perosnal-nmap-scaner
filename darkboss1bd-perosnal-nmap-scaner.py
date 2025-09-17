#!/usr/bin/env python3
# auto-port-picker version: each run picks a new free port (random within range)
import os
import socket
from contextlib import closing
import random
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    scan_result = ""
    command_executed = ""

    if request.method == "POST":
        target = request.form.get("target", "")
        scan_type = request.form.get("scan_type", "")

        scan_options = {
            "Ping Scan (-sP)": "-sP",
            "TCP Connect Scan (-sT)": "-sT",
            "SYN Scan (-sS)": "-sS",
            "Aggressive Scan (-A)": "-A",
            "OS Detection Scan (-O)": "-O",
            "Scan without Ping (-Pn)": "-Pn",
            "UDP Scan (-sU)": "-sU",
            "Fragmented Packets Scan (-f)": "-f",
            "Traceroute (-tr)": "--traceroute",
            "Firewall Detection (-sA)": "-sA",
            "Version Detection (-sV)": "-sV",
            "Intense Scan (-T4 -A -v)": "-T4 -A -v",
            "Comprehensive Scan (-p 1-65535 -T4 -A -v)": "-p 1-65535 -T4 -A -v"
        }

        nmap_option = scan_options.get(scan_type, "-sP")
        requires_sudo = scan_type in [
            "OS Detection Scan (-O)", "Firewall Detection (-sA)",
            "SYN Scan (-sS)", "UDP Scan (-sU)", "Fragmented Packets Scan (-f)",
            "Traceroute (-tr)", "Intense Scan (-T4 -A -v)",
            "Comprehensive Scan (-p 1-65535 -T4 -A -v)", "Aggressive Scan (-A)"
        ]

        command = (["sudo", "nmap"] if requires_sudo else ["nmap"]) + nmap_option.split() + [target]
        command_executed = " ".join(command)

        try:
            scan_result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            scan_result = f"Error executing Nmap: {e.output}"

    # render_template expects an index.html in templates/ — keep your existing template
    return render_template("index.html", command_executed=command_executed, scan_result=scan_result)


def port_is_free(port, host="0.0.0.0"):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def pick_random_free_port(preferred_range=(20000, 30000), tries=200):
    """Pick a random free TCP port within preferred_range. Tries up to `tries` times.
       If can't find, fall back to OS-assigned ephemeral port (port 0)."""
    start, end = preferred_range
    # create a shuffled list of candidate ports (sample)
    candidates = random.sample(range(start, end + 1), min(tries, end - start + 1))
    for p in candidates:
        if port_is_free(p):
            return p

    # last resort: ask OS for ephemeral port
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    # 1) If user explicitly set PORT env var and it's free, honor it
    env_port = os.getenv("PORT")
    selected_port = None
    if env_port:
        try:
            p = int(env_port)
            if 1 <= p <= 65535 and port_is_free(p):
                selected_port = p
            else:
                print(f"PORT={p} from environment is not free/valid — selecting a random free port instead.")
        except ValueError:
            print("PORT environment variable is not an integer; ignoring it and selecting a random free port.")

    # 2) Otherwise pick a random free port each run (so "new" port most runs)
    if selected_port is None:
        # you can change the range below if you like (e.g., 5000-5999)
        selected_port = pick_random_free_port(preferred_range=(20000, 30000), tries=500)

    print(f"Starting Flask on 0.0.0.0:{selected_port}  — (each run picks a random free port).")
    # If you prefer binding to localhost only, change host="127.0.0.1"
    app.run(host="0.0.0.0", port=selected_port, debug=True)
