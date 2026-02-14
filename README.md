# 🔎PortLens – Visual Network Security Scanner

PortLens is a modern, GUI-based network port scanner built with Python and CustomTkinter. It helps cybersecurity students, professionals, and network administrators identify open ports, detect running services, and evaluate overall system security risk through a clean and intuitive visual dashboard.

It combines fast multithreaded scanning, service detection, and risk analysis into one professional desktop application.

---

## 🚀 Features
✔ Modern GUI built with CustomTkinter  
✔ Fast multithreaded port scanning engine  
✔ Scan custom ports or use predefined presets  
✔ Service detection for open ports  
✔ Built-in Risk Level Analysis (Low / Medium / High)  
✔ Export results to JSON, CSV, TXT, and PDF  
✔ Real-time scan progress tracking  
✔ Professional dashboard interface  
✔ Clean modular architecture  

---

## 🧠 Risk Level Detection
PortLens automatically evaluates system exposure based on open ports:

| Risk Level | Description |
|----------|-------------|
| 🔴 High Risk | Critical ports like SSH, MySQL, MongoDB open |
| 🟡 Medium Risk | Web ports like HTTP / HTTPS open |
| 🟢 Low Risk | No sensitive ports exposed |

This allows instant security assessment without manual analysis.

---

## 🛠 Built With
• Python 3  
• CustomTkinter  
• Socket Programming  
• Multithreading  
• JSON / CSV / PDF Export  
• Modular Architecture  

---

## ⚙️ Installation
### Clone repository
```bash
git clone https://github.com/PanthilShah/PortLens.git
cd PortLens
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run application
```bash
python main.py
```

---

## 🎯 Usage
1. Enter target IP or hostname  
2. Enter ports or use presets  
3. Click **Start Scan**  
4. View open ports, services, and risk level  
5. Export results if needed  

---

## 📁 Project Structure
```
PortLens/
│
├── core/           # Scanning engine
├── gui/            # GUI components
├── utils/          # Validators, exporters, logger
├── data/           # Port and vulnerability data
├── exports/        # Exported reports
├── main.py         # Entry point
├── config.py       # App configuration
└── README.md
```

---

## 🔐 Educational Purpose
This project is intended for:

• Cybersecurity learning  
• Ethical hacking practice  
• Network security analysis  
• Academic projects  

Do NOT use on unauthorized systems.

---

## 👨‍💻 Author
Panthil Shah  
Cybersecurity Enthusiast | Python Developer  

GitHub:  
https://github.com/PanthilShah

---

## ⭐ Support
If you like this project, consider giving it a star ⭐ on GitHub.
