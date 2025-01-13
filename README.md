# VulnVoyager Vulnerability Scanner

**VulnVoyager** is a Python-based vulnerability scanner that evaluates the security posture of websites. It combines HTTP header checks, SSL/TLS validation, secure cookie analysis, and link crawling to provide a comprehensive report on potential vulnerabilities. This tool is designed for web developers, security professionals, and enthusiasts aiming to strengthen web application security.

---

![vulnVoyager_Launch](https://github.com/user-attachments/assets/600e7c07-c186-4c3d-b3b9-80ca8e361ed7)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/PrairieWaltz/VulnVoyager
   cd VulnVoyager
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python3 vulnVoyager.py -u https://example.com
   ```

Enjoy seamless and comprehensive web security scanning with VulnVoyager!

---

## Features

### 1. **HTTP Header Analysis**

- Identifies missing or improperly configured security headers, such as:
  - `Content-Security-Policy`
  - `X-Frame-Options`
  - `X-Content-Type-Options`
- Identifies missing headers and highlights potential vulnerabilities.

### 2. **SSL/TLS Configuration Validation**

- Verifies the validity of SSL/TLS certificates.
- Ensures secure HTTPS configurations are in place.
- Detects expired or misconfigured certificates.

### 3. **Cookie Security Analysis**

- Evaluates cookies for:
  - `Secure` flag to prevent unencrypted transmission.
  - `HttpOnly` flag to protect against JavaScript-based attacks.
- Flags insecure cookies for review.

### 4. **Multithreaded Link Crawling**

- Uses multithreading to efficiently crawl links on a webpage.
- Recursively discovers links up to a user-specified depth.
- Provides a list of all discovered links for further analysis.

### 5. **Customizable Output**

- Saves results in JSON or plain text format.
- Allows users to specify output file paths and formats.

---

## How It Works

1. **Setup and Execution**

   - Users can provide a target URL via the `--url` or `-u` flag.
   - The app validates the URL and begins scanning the website.
   - EXAMPLE: Scan a chosen URL and save the file as results.txt to the Desktop using a search depth of 2
   - `python3 vulnVoyager.py -u https://URLHERE.com -o ~/Desktop/results.txt(results.json) -d 2`

2. **Scanning Process**

   - **HTTP Header Check**: The app fetches the target's HTTP headers and evaluates their security.
   - **SSL/TLS Validation**: A secure connection is established, and the SSL/TLS certificate is analyzed.
   - **Cookie Analysis**: The app parses the `Set-Cookie` header for security flags.
   - **Link Crawling**: Discovered links are fetched and recursively crawled up to the specified depth.

3. **Saving Results**
   - Results are saved to a user-defined file or default location.
   - Supports JSON for structured data and plain text for human-readable output.

---

## Flags and Default Settings

### Default Behavior

- Without additional flags, the app scans the provided URL, performs a basic security check, and saves the results to `scan_results.json` in the current directory.

### Command-Line Flags

1. **`--url` or `-u`** (Required):

   - Specify the target URL to scan.
   - Example: `python3 vulnVoyager.py -u https://URLHERE.com`

2. **`--output` or `-o`**:

   - Define the output file's name and location.
   - Supports `.json` or `.txt` formats.
   - Example: `python3 vulnVoyager.py -u https://URLHERE.com -o ~/Desktop/results.txt`

JSON Formatting:

![vulnVoyager_Data](https://github.com/user-attachments/assets/a5f5c261-62c2-4027-a800-9d017bd78e8c)

Plain Text Formatting:

![vulnVoyager_TXTData](https://github.com/user-attachments/assets/61b254db-650b-4754-abfc-ffc95d8f9df3)

4. **`--depth` or `-d`**:
   - Specify the crawling depth for discovering links.
   - Default: `1`.
   - Example: `python3 vulnVoyager.py -u https://URLHERE.com -d 3`

### Example Usage

```bash
python3 vulnVoyager.py -u https://URLHERE.com -o ~/Desktop/results.json -d 2
```

---

## Why Use VulnVoyager?

- **Efficiency**: Combines multiple security checks into one tool.
- **Customizable**: Allows tailored scans based on user needs.
- **Ease of Use**: Simple CLI with interactive prompts for ease of operation.
- **Comprehensive**: Provides detailed reports for informed decision-making.

**VulnVoyager** is a must-have for anyone looking to assess and improve their website’s security, making it invaluable for both beginners and professionals.

---
