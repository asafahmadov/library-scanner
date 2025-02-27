import subprocess
import re
import os
import webbrowser
import requests
from concurrent.futures import ThreadPoolExecutor

OSV_API_URL = "https://api.osv.dev/v1/query"

def run_gradle_dependencies():
    """Run Gradle Wrapper to get dependencies."""
    if not os.path.exists("gradlew.bat"):
        print("❌ Error: 'gradlew.bat' not found. Run the script inside the project folder!")
        return None

    try:
        result = subprocess.run(
            ["gradlew.bat", "dependencies", "--configuration", "runtimeClasspath"], 
            capture_output=True, text=True, shell=True
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None

def extract_dependencies(gradle_output):
    """Extract dependencies with versions from Gradle output."""
    dependencies = set()
    pattern = re.compile(r'[-+|\\]+---\s([\w\-.]+):([\w\-.]+):([\w\-.]+)')
    
    for line in gradle_output.split("\n"):
        match = pattern.search(line.strip())
        if match:
            # (Group, Name, Version)
            dependencies.add((match.group(1), match.group(2), match.group(3)))

    return sorted(dependencies)

def get_highest_severity(vuln):
    """Extract the highest severity level from a vulnerability report."""
    severity_levels = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    highest = "UNKNOWN"
    
    # Check "severity" field directly
    if "severity" in vuln:
        for severity in vuln["severity"]:
            severity_label = severity.get("type", "").upper()
            if severity_label in severity_levels and severity_levels[severity_label] > severity_levels.get(highest, 0):
                highest = severity_label

    # Check "affected" field for severity info
    if "affected" in vuln:
        for affected in vuln["affected"]:
            if "database_specific" in affected and "severity" in affected["database_specific"]:
                severity_label = affected["database_specific"]["severity"].upper()
                if severity_label in severity_levels and severity_levels[severity_label] > severity_levels.get(highest, 0):
                    highest = severity_label

    return highest

def check_vulnerability(group, name, version):
    """Check if a library has known vulnerabilities using OSV API."""
    payload = {"package": {"name": f"{group}:{name}"}, "version": version}
    
    try:
        response = requests.post(OSV_API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "vulns" in data and data["vulns"]:
                return "❌ Vulnerable", [
                    (
                        vuln.get("id", "N/A"), 
                        vuln.get("summary", "No description available"),
                        next((ref["url"] for ref in vuln.get("references", []) if "cve" in ref["url"]), "#"),
                        get_highest_severity(vuln)
                    )
                    for vuln in data["vulns"]
                ]
        return "✅ Safe", []
    except Exception:
        return "⚠️ Error", []

def generate_table_rows(vulnerability_results):
    """Helper function to generate <tr> rows for the dependencies table."""
    rows = []
    for (group, name, version), (vuln_status, cve_list) in vulnerability_results.items():
        if vuln_status == "✅ Safe":
            status_class = "text-success"
        elif vuln_status == "❌ Vulnerable":
            status_class = "text-danger"
        else:
            status_class = "text-warning"

        if cve_list:
            # cve_list[0][3] -> severity
            severity_label = cve_list[0][3].lower()
            severity_class = severity_label if severity_label in ["critical","high","medium","low"] else "unknown"

            cve_details = "<br>".join(
                f'<a href="{cve_link}" target="_blank">{cve_id}</a>: {summary}'
                for (cve_id, summary, cve_link, _) in cve_list
            )
            severity_display = cve_list[0][3]
        else:
            cve_details = "N/A"
            severity_class = "unknown"
            severity_display = "UNKNOWN"

        row_html = f"""
        <tr>
          <td>{group}</td>
          <td>{name}</td>
          <td>{version}</td>
          <td class="{status_class}">{vuln_status}</td>
          <td>{cve_details}</td>
          <td class="{severity_class}">{severity_display}</td>
        </tr>
        """
        rows.append(row_html)
    return "\n".join(rows)

def generate_html_report(dependencies):
    """Generate an HTML report by reading an external HTML template."""
    print("\n🔎 Checking for vulnerabilities...")
    vulnerability_results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda dep: (dep, check_vulnerability(*dep)), dependencies)
        vulnerability_results = dict(results)

    safe_count = sum(1 for vuln, _ in vulnerability_results.values() if vuln == "✅ Safe")
    vulnerable_count = sum(1 for vuln, _ in vulnerability_results.values() if vuln == "❌ Vulnerable")
    total_count = len(dependencies)
    vulnerability_rate = round((vulnerable_count / total_count * 100), 1) if total_count else 0

    # Dış HTML şablonunu oku
    template_path = os.path.join("template", "report_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Değişkenleri yerleştir
    html_template = html_template.replace("{{ total_count }}", str(total_count))
    html_template = html_template.replace("{{ safe_count }}", str(safe_count))
    html_template = html_template.replace("{{ vulnerable_count }}", str(vulnerable_count))
    html_template = html_template.replace("{{ vulnerability_rate }}", str(vulnerability_rate))
    html_template = html_template.replace("{{ table_rows }}", generate_table_rows(vulnerability_results))

    # Son HTML dosyasını yaz
    output_file = "dependencies_security_report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"\n✅ HTML security report generated: {output_file}")
    webbrowser.open(output_file)

if __name__ == "__main__":
    print("🚀 Extracting Gradle dependencies...\n")
    
    gradle_output = run_gradle_dependencies()
    if gradle_output:
        dependencies = extract_dependencies(gradle_output)
        if dependencies:
            print("\n📦 Generating HTML Security Report...")
            generate_html_report(dependencies)
        else:
            print("\n❌ No dependencies found.")
