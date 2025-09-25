import subprocess
import sys
from collections import OrderedDict
import time

# Colors for the terminal (ANSI escape codes)
class Colors:
    HEADER = '\033[95m'  # Magenta
    OKBLUE = '\033[94m'  # Blue
    OKCYAN = '\033[96m'  # Cyan
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m'    # Red
    ENDC = '\033[0m'     # Reset color
    BOLD = '\033[1m'     # Bold
    UNDERLINE = '\033[4m' # Underline

def run_dig(domain, record_type, dns_server="1.1.1.1"):
    """Executes the dig command and returns the cleaned output."""
    try:
        command = ['dig', f'@{dns_server}', domain, record_type, '+short']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""
    except FileNotFoundError:
        print(f"{Colors.FAIL}{Colors.BOLD}Error: 'dig' command not found. Make sure 'dnsutils' is installed.{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

def run_dig_ptr(ip_address, dns_server="1.1.1.1"):
    """Executes the dig command for a PTR record."""
    try:
        command = ['dig', f'@{dns_server}', '-x', ip_address, '+short']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        print(f"{Colors.FAIL}{Colors.BOLD}Error: 'dig' command not found. Make sure 'dnsutils' is installed.{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}DIG ANY{Colors.ENDC}")
    print(f"{Colors.WARNING}Made by thesw0rd{Colors.ENDC}")
    print("\n" + "="*60 + "\n")

    if len(sys.argv) != 2:
        print(f"{Colors.WARNING}Usage: {sys.argv[0]} <domain>{Colors.ENDC}")
        print(f"{Colors.WARNING}Example: {sys.argv[0]} google.com{Colors.ENDC}")
        sys.exit(1)

    domain = sys.argv[1]
    dns_server = "1.1.1.1" # Can be made an argument once in the future

    print(f"{Colors.HEADER}{Colors.BOLD}Analyzing domain: {domain}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}Using DNS server: {dns_server}{Colors.ENDC}")
    print("\n" + "="*60 + "\n")

    record_types = OrderedDict([
        ("A", "IPv4 Address"),
        ("AAAA", "IPv6 Address"),
        ("MX", "Mail Exchange Records (Email Servers)"),
        ("NS", "Name Server Records"),
        ("TXT", "Text Records"),
        ("CNAME", "Canonical Name (Alias)"),
        ("SOA", "Start of Authority Record"),
        ("CAA", "Certification Authority Authorization"),
        ("SRV", "Service Records")
    ])

    results = {}

    for record_type, description in record_types.items():
        print(f"{Colors.OKCYAN}{Colors.BOLD}--- {description} ({record_type}) ---{Colors.ENDC}")
        output = run_dig(domain, record_type, dns_server)
        if output:
            lines = output.splitlines()
            for line in lines:
                print(f"{Colors.OKGREEN}  {line}{Colors.ENDC}") # indentation for aesthetics
            results[record_type] = lines
        else:
            print(f"{Colors.WARNING}  No records found for type {record_type} or error retrieving.{Colors.ENDC}")
        print("")

    # PTR (Reverse DNS Lookup)
    print(f"{Colors.OKCYAN}{Colors.BOLD}--- PTR (Reverse DNS Lookup) ---{Colors.ENDC}")

    ip_address = None
    if "A" in results and results["A"]:
        ip_address = results["A"][0] # Take the first IP from A records
        print(f"{Colors.OKBLUE}  Found IP for {domain}: {ip_address}{Colors.ENDC}")
        ptr_record = run_dig_ptr(ip_address, dns_server)
        if ptr_record:
            print(f"{Colors.OKGREEN}  {ptr_record}{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}  No PTR record for {ip_address} (status: NXDOMAIN or NOERROR with empty response).{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}  Could not retrieve IPv4 address for {domain}, PTR query not possible.{Colors.ENDC}")

    print("\n" + "="*60 + "\n")
    print(f"{Colors.HEADER}{Colors.BOLD}--- Analysis complete. All available information above. ---{Colors.ENDC}")

if __name__ == "__main__":
    main()
