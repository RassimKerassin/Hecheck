#!/usr/bin/python3

import argparse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-list", required=True, help="Path to the list of domains and URLs")
args = parser.parse_args()

# Read the list of domains and URLs from the specified file
with open(args.list, "r") as f:
    domains_and_urls = f.readlines()

# Set up the headers to check for
headers_to_check = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Strict-Transport-Security"
]

# Set up the table to store the results
results_table = {}
for header in headers_to_check:
    results_table[header] = []

# Iterate over the domains and URLs, checking for the availability of the headers
for domain_or_url in domains_and_urls:
    domain_or_url = domain_or_url.strip()
    try:
        response = requests.get(domain_or_url, allow_redirects=True, verify=False)
    except Exception as e:
        print(f"Error while trying to request {domain_or_url}: {e}")
        continue
    for header in headers_to_check:
        if header not in response.headers:
            results_table[header].append(domain_or_url)

# Print the results table
for header, url_list in results_table.items():
    print(f"{header}: {len(url_list)}")
    print("\n".join(url_list))
    print()
