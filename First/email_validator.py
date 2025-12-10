#!/usr/bin/env python3
"""
Email Domain Validator
Checks email addresses for valid MX records.
"""

import sys
import socket
import dns.resolver
from typing import List, Tuple


def extract_domain(email: str) -> str:
    """Extract domain from email address."""
    if '@' not in email:
        raise ValueError(f"Invalid email format: {email}")
    return email.split('@')[1].strip().lower()


def check_domain_exists(domain: str) -> bool:
    """Check if domain exists by attempting DNS lookup."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def check_mx_records(domain: str) -> Tuple[bool, str]:
    """
    Check if domain has valid MX records.
    Returns: (has_mx, status_message)
    """
    try:
        # Try to resolve MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        
        if len(mx_records) == 0:
            return False, "MX records are missing or invalid"
        
        # Check if any MX record is valid
        valid_mx = False
        for mx in mx_records:
            if mx.preference is not None and str(mx.exchange).strip():
                valid_mx = True
                break
        
        if valid_mx:
            return True, "domain is valid"
        else:
            return False, "MX records are missing or invalid"
            
    except dns.resolver.NXDOMAIN:
        return False, "domain does not exist"
    except dns.resolver.NoAnswer:
        # No MX records found, check if domain exists
        if check_domain_exists(domain):
            return False, "MX records are missing or invalid"
        else:
            return False, "domain does not exist"
    except dns.resolver.NoNameservers:
        return False, "domain does not exist"
    except Exception as e:
        # Fallback: try basic domain check
        if check_domain_exists(domain):
            return False, "MX records are missing or invalid"
        else:
            return False, "domain does not exist"


def validate_emails(email_list: List[str]) -> List[Tuple[str, str]]:
    """
    Validate a list of email addresses.
    Returns: List of (email, status) tuples
    """
    results = []
    
    for email in email_list:
        email = email.strip()
        if not email:
            continue
            
        try:
            domain = extract_domain(email)
            has_mx, status = check_mx_records(domain)
            results.append((email, status))
        except ValueError as e:
            results.append((email, f"Invalid email format: {e}"))
        except Exception as e:
            results.append((email, f"Error: {str(e)}"))
    
    return results


def main():
    """Main function to run the email validator."""
    if len(sys.argv) < 2:
        print("Usage: python email_validator.py <email1> [email2] [email3] ...")
        print("   or: python email_validator.py --file <filename.txt>")
        sys.exit(1)
    
    emails = []
    
    # Check if reading from file
    if sys.argv[1] == '--file' and len(sys.argv) > 2:
        try:
            with open(sys.argv[2], 'r', encoding='utf-8') as f:
                emails = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[2]}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        # Read emails from command line arguments
        emails = sys.argv[1:]
    
    if not emails:
        print("No email addresses provided.")
        sys.exit(1)
    
    # Validate emails
    results = validate_emails(emails)
    
    # Print results
    print("\nEmail Validation Results:")
    print("-" * 60)
    for email, status in results:
        print(f"{email:<40} — {status}")
    print("-" * 60)
    print(f"\nTotal checked: {len(results)}")


if __name__ == "__main__":
    main()

