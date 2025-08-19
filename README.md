# 🚀 Flask Packet Capture Tool

A simple **web-based packet capture tool** built with **Flask** and **Scapy**.

This tool lets you:
- Capture network packets in real-time
- View packet details (source, destination, protocol, length, summary) in the browser
- Apply **BPF filters** (e.g., `tcp`, `udp`, `port 80`)
- Download captured packets as a **PCAP file** for Wireshark analysis

---

## 📂 Project Structure

```
flask-packet-capture/
├── app.py              # Main Flask backend
├── templates/
│   └── index.html      # Web interface (HTML + CSS + JS)
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## 🛠️ Prerequisites

Before running the project, install the following:

1. **Python 3.8+** → [Download here](https://www.python.org/downloads/)
2. **pip** (comes with Python)
3. **Npcap** (Windows only) → [Download here](https://nmap.org/npcap/)
   - On **Linux/Mac**, make sure **libpcap** is installed (`sudo apt install libpcap-dev`)
4. (Optional but recommended) **Virtual Environment**

---

## 📥 Installation & Setup

### 1️⃣ Download the project

### 2️⃣ Create a virtual environment (recommended)
```bash
python -m venv venv
```

Activate it:
- **Windows**:
```bash
venv\Scripts\activate
```
- **Linux/Mac**:
```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt` yet, create it with:
```
Flask
scapy
```

---

## ▶️ Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and go to:
```
http://127.0.0.1:5000
```

3. Use the web interface:
   - Select a **network interface**
   - Enter **packet count** (0 = infinite)
   - (Optional) Add a **BPF filter** (example: `tcp` or `port 80`)
   - Click **Start Capture**
   - Watch live packets appear in the log box
   - Click **Stop Capture** to end
   - Click **Download PCAP** to save packets

---

## ⚠️ Important Notes

- On **Linux/Mac**, you must run as **root** to capture packets:
```bash
sudo python app.py
```

- On **Windows**, run **Command Prompt/PowerShell as Administrator**.

- Make sure **Npcap** (Windows) or **libpcap** (Linux/Mac) is installed, otherwise packet capture will not work.

- Only use this tool for **educational or research purposes**. Do **not** capture traffic on networks without permission.

---

## 📦 Example Requirements.txt

Your `requirements.txt` file should contain:

```
Flask==3.0.0
scapy==2.5.0
```

*(Versions may vary, but this is a safe setup)*
