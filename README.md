A modern, lightweight graphical control panel for Kali Linux built in Python using ttkbootstrap.

This project transforms the standard Kali application menu into a cyber-style dashboard interface, featuring searchable tools, categorized views, and one-click launch buttons.

⚡ Features
🖥️ GUI Dashboard Interface
Clean, dark-themed control center UI
Card-based layout for installed Kali tools
🚀 One-Click Tool Launching
Automatically detects installed .desktop applications
Launch tools directly from GUI buttons
🔍 Search System
Instantly filter tools by name
📂 Category Filtering
Recon
Exploitation
Web Security
Wireless
Password Attacks
🧠 Smart Info System

Provides human-readable explanations of tools, including:

What the tool does
Category
Execution command
🧅 Tor Toggle Switch
Start/stop Tor service directly from the GUI
Visual ON/OFF status indicator
📜 Scrollable Dashboard
Handles large numbers of installed tools
Smooth mouse-wheel scrolling support
🛠️ Built With
Python 3
ttkbootstrap (modern Tkinter UI framework)
subprocess (system command execution)
configparser (reads Linux .desktop entries)
📦 Installation
sudo apt install tor python3-pip
pip install ttkbootstrap
▶️ Run
python3 kali_control_center.py
🔐 Requirements
Kali Linux (or Debian-based system)
Root privileges for Tor service control (systemctl)
Installed .desktop application entries
⚠️ Disclaimer

This tool is intended for educational and authorized security testing only.

Do not use Kali Linux tools on systems you do not own or have explicit permission to test.

🚀 Future Plans
Live network mapping dashboard
Metasploit module integration
Nmap scan results viewer
VPN + Tor routing manager
Attack workflow presets (recon → exploit → report)
Cyber animated background UI
📌 Summary

This project transforms Kali Linux from a traditional menu-based system into a modern cyber operations dashboard, making penetration testing tools easier to access, organize, and understand.
