# DIG ANY - DNS Reconnaissance Script

## Overview

This Python script queries various DNS record types for a given domain individually, as the standard `dig <domain> ANY` often fails. It provides a structured, color-coded output in the terminal, making DNS information easy to read.

---

## Features

* Queries common DNS records: A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV.
* Performs PTR (reverse DNS) lookup for the main IPv4 address.
* Presents output with colors for better readability.
* Provides clean and formatted results.

---

## Setup

### Prerequisites

* **Python 3**
* **`dig` utility**: Install `dnsutils` (Debian/Ubuntu) or `bind-utils` (CentOS/RHEL).

    * **Debian/Ubuntu:** `sudo apt install dnsutils`
    * **CentOS/RHEL:** `sudo yum install bind-utils` or `sudo dnf install bind-utils`

### Installation

1.  Save the script: Copy the Python code into a file, e.g., `dig_any.py`.
2.  Make it executable: `chmod +x dig_any.py`

---

## Usage

Run the script with the domain as an argument:

```bash
./digany.py example.com
```
---
Made by thesw0rd
