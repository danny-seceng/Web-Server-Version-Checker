# Web Server Version Checker (Apache & PHP) For Windows

This project is a Python-based security and maintenance utility that detects **Apache** and **PHP** versions from a target web server and compares them against the **latest available and supported releases**.

The tool helps identify:
- Outdated Apache HTTP Server versions
- Outdated or unsupported PHP versions
- Missing or exposed HTTP headers (`Server`, `X-Powered-By`)

It is useful for **security assessments**, **hardening checks**, and **basic reconnaissance** during web application reviews.

---

## Features

- 🔍 Detects **Apache** version from HTTP `Server` header  
- 🐘 Detects **PHP** version from `X-Powered-By` header  
- 🌐 Retrieves the **latest Apache version** from `downloads.apache.org`  
- 🪟 Retrieves **latest supported PHP versions per branch** from `windows.php.net`
- ⚠️ Compares detected versions against:
  - Latest overall release
  - Latest release within the same major/minor branch
- 🧪 Gracefully handles missing headers

---

## How It Works

1. Sends an HTTP request to a target URL
2. Extracts:
   - Apache version from `Server` header
   - PHP version from `X-Powered-By` header
3. Fetches current release data from official sources
4. Compares detected versions with:
   - Latest available version
   - Latest supported version for the detected branch
5. Outputs status and upgrade recommendations

---

## Requirements

- Python **3.8+**
- Internet access

### Python Dependencies

```bash
pip install requests packaging
```

## Usage

### Run from Notebook

Open app.ipynb and execute all cells.

### Run as a Script

MacOS/Linux/Windows: type the following command in the terminal/command propmpt

```bash
python app.py https://example.com
```
or
```bash
python3 app.py https://example.com
```

## Limitations

- Relies on public HTTP headers
- Cannot detect versions if headers are removed or modified
- Does not perform vulnerability exploitation or active scanning

## Security Notes

- Version disclosure via headers can aid attackers during reconnaissance.
- Consider disabling or obfuscating:
    - Server header
    - X-Powered-By header
- Keeping Apache and PHP up-to-date reduces exposure to known CVEs.

## Todo List

- Add HTTPS/TLS inspection
- Export results to JSON or CSV
- CVE lookup for detected versions
- Batch scanning of multiple URLs
- Integration with vulnerability scanners or CI pipelines

## Disclaimer

This tool is intended for defensive security, system administration, and educational purposes only.
Only scan systems you own or have explicit permission to test.

## License

MIT License