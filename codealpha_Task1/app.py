from flask import Flask, request, send_file, Response, render_template, redirect, url_for
from scapy.all import sniff, wrpcap, get_if_list
import threading
import time
import json

app = Flask(__name__)

captured_packets = []
packet_details = []
capture_thread = None
sniffing = False


def process_packet(packet):
    """Extract detailed info for each packet."""
    try:
        details = {
            "time": str(packet.time),
            "summary": packet.summary(),
            "length": len(packet),
            "src": packet[0][1].src if hasattr(packet[0][1], "src") else "N/A",
            "dst": packet[0][1].dst if hasattr(packet[0][1], "dst") else "N/A",
            "proto": packet[0][1].name if hasattr(packet[0][1], "name") else "N/A",
            "full": repr(packet)
        }
        packet_details.append(details)
        captured_packets.append(packet)
    except Exception as e:
        print(f"Error processing packet: {e}")


def start_capture(count=0, iface=None, bpf=None):
    global sniffing
    sniffing = True

    def should_stop(packet):
        return not sniffing  

    sniff(
        prn=process_packet,
        count=count if count > 0 else 0,
        iface=iface,
        filter=bpf,
        stop_filter=should_stop
    )
    sniffing = False


@app.route("/")
def index():
    return render_template("index.html", interfaces=get_if_list(), sniffing=sniffing)


@app.route("/start", methods=["POST"])
def start():
    global capture_thread, captured_packets, packet_details

    if sniffing:
        return "Capture already running", 400

    captured_packets = []
    packet_details = []

    count = int(request.form.get("count", 0))  # 0 = infinite
    iface = request.form.get("iface") or None
    bpf = request.form.get("bpf") or None

    capture_thread = threading.Thread(target=start_capture, args=(count, iface, bpf))
    capture_thread.daemon = True
    capture_thread.start()

    return redirect(url_for("index"))


@app.route("/stop", methods=["POST"])
def stop():
    global sniffing
    if sniffing:
        sniffing = False
        return redirect(url_for("index"))
    return "No capture running", 400


@app.route("/download")
def download():
    if not captured_packets:
        return "No packets captured yet", 400
    wrpcap("captured_packets.pcap", captured_packets)
    return send_file("captured_packets.pcap", as_attachment=True)


@app.route("/stream")
def stream():
    """Stream live packet details using SSE"""
    def event_stream():
        last_index = 0
        while True:
            time.sleep(1)
            global packet_details
            if last_index < len(packet_details):
                for pkt in packet_details[last_index:]:
                    yield f"data: {json.dumps(pkt)}\n\n"
                last_index = len(packet_details)
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
