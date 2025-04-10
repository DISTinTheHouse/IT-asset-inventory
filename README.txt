# 🖥️ IT Asset Inventory for Windows Devices

This project contains two Python scripts designed to scan and consolidate hardware and system information from Windows-based computers. It provides a lightweight and efficient way to maintain an updated inventory of all laptops or workstations across an organization.

---

## 📁 Scripts Overview

### 1. `inventario_windows.py`

This script gathers system information from a local machine and saves it as a JSON file. It's intended to be executed individually on each computer you want to inventory.

**Collected information includes:**
- Date and user
- Hostname and domain
- Operating system and version
- CPU, architecture, RAM
- BIOS manufacturer, model, and serial number
- Uptime and battery status
- Local IP and MAC address
- Network interfaces
- Disk partitions and usage

**Output:** A JSON file named `INVENTARIO_<HOSTNAME>.json`

#### ✅ Example output structure:
```json
{
  "fecha": "2025-04-10 12:34:56",
  "usuario": "admin",
  "nombre_equipo": "LAPTOP-1234",
  "ip_local": "192.168.1.10",
  "mac_address": "00:1a:2b:3c:4d:5e",
  ...
}

2. consolidad_inventario.py
Once multiple inventory JSON files have been collected, this script consolidates them into a single Excel spreadsheet for easy analysis and reporting.

Key features:

Flattens all relevant JSON fields into rows

Adds battery status (if available)

Sums disk capacity across devices

Isolates data for the main disk (typically C:\)

Lists all IPs associated with the device

Output: INVENTARIO_LAPTOPS.xlsx — ready for Excel or further processing

🔧 How to Generate .exe (Optional)
To distribute inventario_windows.py without requiring Python installation on target machines, you can package it using PyInstaller:

pip install pyinstaller
pyinstaller --onefile inventario_windows.py

This will create an executable in the dist/ directory. Do not upload the .exe to GitHub. It should be shared internally via your preferred method.

📁 Recommended Project Structure
/inventario
│
├── inventario_windows.py          # Runs on each device to collect info
├── consolidad_inventario.py       # Merges all JSONs into Excel
├── /inventario_laptops/JSONs      # Folder with all individual JSON outputs
├── .gitignore                     # Ignore build files and JSON data
├── LICENSE                        # Proprietary license info
└── README.md                      # Project documentation

🛡️ License
© 2025 [Jesús Ibarra M.]. All rights reserved.

This software is proprietary and confidential. Unauthorized use, copying, or distribution is strictly prohibited. For permission requests, contact: [ufkwear@gmail.com]

📬 Contact
For support or business inquiries, feel free to reach out at [ufkwear@gmail.com].