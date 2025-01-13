# VulnVoyager Vulnerability Scanner

The VulnVoyager Vulnerability Scanner is a versatile tool designed to analyze websites for common security issues. By combining HTTP header checks, SSL/TLS validation, and secure cookie analysis with multithreaded link crawling, this app provides a comprehensive overview of a website's security posture. Users can customize their scans with various command-line flags or rely on sensible default settings for quick checks.

---

## Features

### 1. **HTTP Header Analysis**

- Checks for critical security headers:
  - `Content-Security-Policy`
  - `X-Frame-Options`
  - `X-Content-Type-Options`
- Identifies missing headers and highlights potential vulnerabilities.

### 2. **SSL/TLS Configuration Validation**

- Verifies the validity of SSL/TLS certificates.
- Ensures secure HTTPS configurations are in place.
- Detects expired or misconfigured certificates.

### 3. **Secure Cookie Check**

- Analyzes `Set-Cookie` headers for:
  - `Secure` flag to prevent transmission over unencrypted connections.
  - `HttpOnly` flag to protect cookies from JavaScript-based attacks.
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
     EXAMPLE: Scan a chosen URL and save the file as scan.txt to Desktop using a depth of 2
     `python3 vulnVoyager.py -u https://URLHERE.com -o ~/Desktop/scan.txt(scan.json) -d 2`

2. **Scanning Process**

   - **HTTP Header Check**: The app fetches the target's HTTP headers and evaluates their security.
   - **SSL/TLS Validation**: A secure connection is established, and the SSL/TLS certificate is analyzed.
   - **Cookie Analysis**: The app parses the `Set-Cookie` header for security flags.
   - **Link Crawling**: Discovered links are fetched and recursively crawled up to the specified depth.

3. **Saving Results**
   - Results are saved to a user-defined file or default location.
   - Supports JSON for structured data and plain text for human-readable output.

---

## Spotlight: Using Flags and Default Settings

### Default Behavior

- Without additional flags, the app scans the provided URL, performs a basic security check, and saves the results to `scan_results.json` in the current directory.

### Command-Line Flags

1. **`--url` or `-u`** (Required):

   - Specify the target URL to scan.
   - Example: `python3 vuln_scanner.py -u https://example.com`

2. **`--output` or `-o`**:

   - Define the output file's name and location.
   - Supports `.json` or `.txt` formats.
   - Example: `python3 vuln_scanner.py -u https://example.com -o ~/Desktop/results.txt`

3. **`--depth` or `-d`**:
   - Specify the crawling depth for discovering links.
   - Default: `1`.
   - Example: `python3 vuln_scanner.py -u https://example.com -d 3`

---

## Why Use This App?

- **Ease of Use**: Command-line flags and interactive prompts make it accessible for beginners and advanced users alike.
- **Customizable**: Allows fine-tuned scans tailored to specific needs.
- **Comprehensive**: Combines multiple security checks into a single tool, saving time and effort.

This scanner is an essential tool for web developers, security professionals, and enthusiasts looking to bolster their web application security.
