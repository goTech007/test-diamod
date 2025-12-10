# Email Domain Validator - Instructions

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Command Line Arguments
Pass email addresses directly as arguments:

```bash
python email_validator.py user@example.com test@gmail.com admin@invalid-domain-xyz.com
```

### Option 2: From File
Create a text file with one email per line, then run:

```bash
python email_validator.py --file emails.txt
```

Example `emails.txt`:
```
user@example.com
test@gmail.com
admin@invalid-domain-xyz.com
contact@company.com
```

## Output

The script will display results for each email address with one of the following statuses:
- **"domain is valid"** - Domain exists and has valid MX records
- **"domain does not exist"** - Domain cannot be resolved
- **"MX records are missing or invalid"** - Domain exists but has no valid MX records

## Example Output

```
Email Validation Results:
------------------------------------------------------------
user@example.com                          — domain is valid
test@gmail.com                            — domain is valid
admin@invalid-domain-xyz.com             — domain does not exist
contact@company.com                       — domain is valid
------------------------------------------------------------

Total checked: 4
```

## Notes

- The script uses DNS queries to check MX records
- Requires internet connection
- Some domains may take a few seconds to resolve

