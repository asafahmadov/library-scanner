🛡️ Gradle Security Checker
Automated security scanning for Gradle dependencies using OSV API & CoreUI

![image](https://github.com/user-attachments/assets/69333720-a7ac-4159-a94b-b0e907fe7556)



📌 Overview
Gradle Security Checker is a Python-based tool that scans your Gradle project dependencies for known vulnerabilities using the OSV API. It generates a detailed security report with a CoreUI-based dashboard, displaying dependency vulnerabilities in an easy-to-read format.

🚀 Features
✔️ Automated Gradle Dependency Scanning
✔️ OSV (Open Source Vulnerabilities) API Integration
✔️ Multi-threaded Vulnerability Checking (Fast & Efficient)
✔️ CoreUI-based Responsive Dashboard
✔️ Detailed Dependency & CVE Report (HTML Output)
✔️ Supports Windows (gradlew.bat) & Linux/macOS (./gradlew)


📦 Installation
Make sure you have Python 3.6+ installed. Then follow these steps:

1️⃣ Clone the Repository

git clone https://github.com/<your-username>/gradle-security-checker.git
cd gradle-security-checker
2️⃣ Install Dependencies

pip install -r requirements.txt
⚡ Usage
Navigate to your Gradle project root (where gradlew.bat is located) and run:


python gradle_vuln_check.py
or
py gradle_vuln_check.py

After running, it will:

Extract Gradle dependencies
Check for vulnerabilities via OSV API
Generate an HTML security report
Open the report automatically in your browser

📄 Example Output
The script generates a file called dependencies_security_report.html.

To view it manually:

open dependencies_security_report.html  # macOS
xdg-open dependencies_security_report.html  # Linux
start dependencies_security_report.html  # Windows
🌍 Run with a Local Server
For best results, serve the report via an HTTP server:


python -m http.server 8000
Then open: 👉 http://127.0.0.1:8000/dependencies_security_report.html

🔧 Configuration
The tool automatically detects your Gradle dependencies.
If the script cannot find gradlew.bat, ensure you are inside your project directory.
The HTML template, CSS, and JavaScript are customizable in the static/ and template/ folders.
👨‍💻 Technologies Used
Python 3.6+
Gradle
OSV API
CoreUI
Chart.js
HTML, CSS, JavaScript
🛠️ Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request.

Fork the repo
Create a feature branch
Make changes & commit
Submit a pull request


📞 Contact
For any issues, feel free to open an issue or reach out:

📧 Email: asefehmed1@gmail.com
🐦 Linkedin: (https://www.linkedin.com/in/asaf-ahmadov/)

⭐ Support
If you find this project useful, please star ⭐ the repo to show support! 🚀

📢 Disclaimer
This tool is for educational and security research purposes only. The author is not responsible for any misuse.
