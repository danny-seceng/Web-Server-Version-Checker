# %%
import requests
import re
from packaging import version

TIMEOUT = 10

# %%
# ----------------------------
# Latest Versions
# ----------------------------

def get_latest_apache_version():
    url = "https://downloads.apache.org/httpd/"
    r = requests.get(url, timeout=TIMEOUT)
    matches = re.findall(r"httpd-(\d+\.\d+\.\d+)\.tar\.gz", r.text)
    return sorted(matches, key=version.parse)[-1] if matches else None

# %%
def get_latest_supported_php_version():
    url = "https://www.php.net/releases/index.php?json"
    r = requests.get(url, timeout=10)
    data = r.json()

    versions = []
    supported = set()

    for info in data.values():
        if "version" in info:
            versions.append(info["version"])
        if "supported_versions" in info:
            supported.update(info["supported_versions"])

    # Keep only versions from supported branches
    filtered = [
        v for v in versions
        if v.rsplit(".", 1)[0] in supported
    ]

    return sorted(filtered, key=version.parse)[-1] if filtered else None

# %%
# ----------------------------
# Remote Detection
# ----------------------------

def detect_from_headers(url):
    r = requests.get(url, timeout=TIMEOUT, allow_redirects=True)

    server_header = r.headers.get("Server", "")
    x_powered = r.headers.get("X-Powered-By", "")

    apache_version = None
    php_version = None

    apache_match = re.search(r"Apache/([\d.]+)", server_header)
    if apache_match:
        apache_version = apache_match.group(1)

    php_match = re.search(r"PHP/([\d.]+)", x_powered)
    if php_match:
        php_version = php_match.group(1)

    return apache_version, php_version, server_header, x_powered

# %%
def check_latest_php_version_for_current_branch(php_version = None):
    if php_version is None:
        return None

    r = requests.get('https://windows.php.net/downloads/releases/releases.json', timeout=TIMEOUT, allow_redirects=True)
    data = r.json()

    latest_php_supported = None
    major = php_version.split('.')[0]
    minor = php_version.split('.')[1]
    current_version = f"{major}.{minor}"

    if current_version is None:
        return None

    latest_build_version = data.get(current_version)
    latest_php_supported = latest_build_version.get('version')

    return latest_php_supported

# %%
def check_software(name, detected, latest, latest_current_branch = None):
    if not detected:
        print(f"[i] {name}: Version not disclosed")
        return

    print(f"[+] {name} Detected Version: {detected}")
    if latest_current_branch is not None:
        print(f"[+] {name} Latest Branch Version: {latest_current_branch}")

    print(f"[+] {name} Latest Version:   {latest}")

    if version.parse(detected) < version.parse(latest):
        print(f"[!] {name} UPDATE AVAILABLE\n")
    else:
        print(f"[✓] {name} is up to date\n")

# %%
# ----------------------------
# Main
# ----------------------------

def main():
    target_url = input("Enter target URL (https://example.com): ").strip()

    print("\n=== Remote Apache & PHP Version Check ===\n")
    print(f"=== Target URL: {target_url} ===\n")

    apache_latest = get_latest_apache_version()
    php_latest = get_latest_supported_php_version()

    apache_detected, php_detected, server_hdr, x_powered_hdr = detect_from_headers(target_url)

    print(f"Server Header:     {server_hdr or 'Not Present'}")
    print(f"X-Powered-By:      {x_powered_hdr or 'Not Present'}\n")

    php_latest_current_branch = check_latest_php_version_for_current_branch(php_detected)

    check_software("Apache", apache_detected, apache_latest)
    check_software("PHP", php_detected, php_latest,php_latest_current_branch)

# %%
if __name__ == "__main__":
    main()


