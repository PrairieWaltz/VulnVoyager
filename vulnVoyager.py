import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from time import sleep
import pyfiglet
import argparse
import json
import ssl
import socket
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# Define required headers
REQUIRED_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def install_dependencies():
    try:
        # Suppress all output except errors
        print("Checking and installing dependencies (this may take a moment)...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("all done...")
    except subprocess.CalledProcessError:
        print(Fore.CYAN + Style.BRIGHT)
        print("Warning: Some dependencies could not be installed.")
        print(f"Some features might not work as expected.")
        print(Fore.WHITE)


def display_banner():
    banner = pyfiglet.figlet_format("VulnVoyager", font="ogre")
    print(banner)


def check_headers(url):
    """Check for missing HTTP security headers."""
    print(f"\nScanning headers for: {url}")
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        results = {"url": url, "headers": {}}

        for header in REQUIRED_HEADERS:
            if header not in headers:
                print(f"\u26A0 Missing: {header}")
                results["headers"][header] = "Missing"
            else:
                print(f"\u2705 Found: {header}")
                results["headers"][header] = "Found"

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch URL - {e}")
        return {"url": url, "error": str(e)}


def check_ssl_tls(url):
    """Check SSL/TLS configuration."""
    print(f"\nChecking SSL/TLS configuration for: {url}")
    results = {"url": url, "ssl_tls": {}}

    try:
        hostname = url.replace(
            "https://", "").replace("http://", "").split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                results["ssl_tls"]["certificate_valid"] = True

        print(f"\u2705 SSL/TLS configuration is valid for {hostname}")

    except Exception as e:
        print(f"\u26A0 SSL/TLS issue: {e}")
        results["ssl_tls"]["certificate_valid"] = False

    return results


def check_cookies(url):
    """Check for secure cookies."""
    print(f"\nChecking cookies for: {url}")
    results = {"url": url, "cookies": []}

    try:
        response = requests.get(url, timeout=10)
        if "Set-Cookie" in response.headers:
            cookies = response.headers["Set-Cookie"].split(",")
            for cookie in cookies:
                secure = "Secure" in cookie
                http_only = "HttpOnly" in cookie
                cookie_result = {
                    "cookie": cookie.strip(),
                    "secure": secure,
                    "http_only": http_only,
                }
                results["cookies"].append(cookie_result)
                if not (secure and http_only):
                    print(f"\u26A0 Insecure cookie: {cookie.strip()}")
                else:
                    print(f"\u2705 Secure cookie: {cookie.strip()}")

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch cookies - {e}")
        return {"url": url, "error": str(e)}


def crawl_links(url, max_depth=1):
    """Crawl links on a given website up to a specified depth."""
    print(f"\nCrawling links for: {url}")
    visited = set()
    to_visit = {url}

    def fetch_links(current_url):
        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set(a["href"] for a in soup.find_all("a", href=True))
            return links
        except requests.exceptions.RequestException:
            return set()

    for _ in range(max_depth):
        next_to_visit = set()
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(
                fetch_links, link): link for link in to_visit}
            for future in future_to_url:
                next_to_visit.update(future.result())

        visited.update(to_visit)
        to_visit = next_to_visit - visited

    return visited


def save_results_to_file(results, output_file):
    """Save results to a file."""
    # Expand `~` to the user's home directory
    output_file = os.path.expanduser(output_file)

    directory = os.path.dirname(output_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if output_file.endswith(".json"):
        with open(output_file, "w") as file:
            json.dump(results, file, indent=4)
        print(f"\nResults saved to {output_file}")
    elif output_file.endswith(".txt"):
        with open(output_file, "w") as file:
            file.write(format_results_as_text(results))
        print(f"\nResults saved to {output_file}")


def format_results_as_text(results):
    """Format results as plain text for saving."""
    output = []

    output.append(f"URL: {results.get('url', 'N/A')}")

    if "headers" in results:
        output.append("\nHTTP Headers:")
        for header, status in results["headers"].items():
            output.append(f"  {header}: {status}")

    if "ssl_tls" in results:
        output.append("\nSSL/TLS Configuration:")
        cert_status = "Valid" if results["ssl_tls"].get(
            "certificate_valid", False) else "Invalid"
        output.append(f"  Certificate Status: {cert_status}")

    if "cookies" in results:
        output.append("\nCookies:")
        for cookie in results["cookies"]:
            secure = "Yes" if cookie.get("secure") else "No"
            http_only = "Yes" if cookie.get("http_only") else "No"
            output.append(f"  Cookie: {cookie.get('cookie', 'N/A')}")
            output.append(f"    Secure: {secure}, HttpOnly: {http_only}")

    return "\n".join(output)


def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Enhanced Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="URL to scan")
    parser.add_argument(
        "-o", "--output", help="File to save the results", default="scan_results.json")
    parser.add_argument("-d", "--depth", type=int, default=1,
                        help="Crawling depth for link discovery")
    args = parser.parse_args()

    # Ask user for save path if not provided explicitly
    if args.output == "scan_results.json":
        save_path = input(
            "\nEnter directory and filename to save the results (e.g., /path/to/results.txt): ").strip()
        if save_path:
            args.output = save_path

    # Expand `~` to full path in case it's used
    args.output = os.path.expanduser(args.output)

    # Perform scans
    results = {}
    results.update(check_headers(args.url))
    results.update(check_ssl_tls(args.url))
    results.update(check_cookies(args.url))

    # Crawl links if depth > 0
    if args.depth > 0:
        links = crawl_links(args.url, args.depth)
        results["crawled_links"] = list(links)

    # Save results
    save_results_to_file(results, args.output)


if __name__ == "__main__":
    install_dependencies()
    sleep(1)
    print("\nStarting scans......")
    print(Fore.RED + Style.BRIGHT)
    display_banner()
    print(Fore.WHITE)
    sleep(1)
    main()
