import csv
import json
import os
import sys
from typing import List, Any, Union
from io import StringIO

# Force UTF-8 encoding for Windows terminal
if sys.platform == 'win32':
    # Set console to UTF-8 mode
    os.system('chcp 65001 > nul')
    
# For Python 3.7+, reconfigure stdout to use UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
elif hasattr(sys.stdout, 'buffer'):
    # For older Python versions, wrap stdout with UTF-8 encoding
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def json_to_csv(json_array: List[dict], fields: List[str], output_file: str = None) -> str:
    """
    Extract specified fields from a JSON array and convert to CSV format.
    
    Args:
        json_array: List of dictionaries (JSON objects)
        fields: List of field names to extract from each JSON object
        output_file: Optional path to write CSV file. If None, returns CSV as string
        
    Returns:
        CSV content as string
    """
    # Create CSV in memory
    output = StringIO(newline='')
    writer = csv.DictWriter(
        output, 
        fieldnames=fields, 
        extrasaction='ignore',
        quoting=csv.QUOTE_ALL,
        doublequote=True,
        lineterminator='\n'
    )
    
    # Write header
    writer.writeheader()
    
    # Process each item in the JSON array
    for item in json_array:
        row = {}
        # Create a case-insensitive lookup dictionary for the current item
        item_lower = {k.lower(): (k, v) for k, v in item.items()}
        
        for field in fields:
            # Try case-insensitive lookup
            field_lower = field.lower()
            if field_lower in item_lower:
                actual_key, value = item_lower[field_lower]
            else:
                value = None
            
            # Handle different data types
            if value is None:
                row[field] = ''
            elif isinstance(value, list):
                # Convert lists to pipe-separated strings
                row[field] = ' | '.join(str(v).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ') for v in value)
            elif isinstance(value, dict):
                # Convert dicts to JSON string
                row[field] = json.dumps(value).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
            else:
                row[field] = str(value).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        
        writer.writerow(row)
    
    # Get CSV content
    csv_content = output.getvalue()
    output.close()
        
    return csv_content


# Example usage
if __name__ == "__main__":
    
    # read input file from argument
    import sys
    if len(sys.argv) < 2:
        print("Usage: python json_to_csv.py <input_json_file> <optional: users/groups/computers>")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) == 3:
        input_type = sys.argv[2]
        if input_type not in ["users", "groups", "computers"]:
            print("Invalid input type. Use 'users' or 'groups' or 'computers'")
            # sys.exit(1)
    
        if input_type == "users":
            ad_attributes = [
                # Core Identity Information
                "samaccountname",           # Their login username (critical for authentication)
                "displayname",              # The user's full name as shown throughout systems
                "userprincipalname",        # Their email-style login (user@domain)
                "employeeid",               # Unique identifier linking to HR systems
                "distinguishedname",        # Their exact location in AD hierarchy
                "description"               # Account description/notes

                # Contact Information
                "mail",                     # Primary email for communication (EmailAddress)
                "mobile",                   # Phone contact details
                "telephonenumber",          # Phone contact details
                "officephone",              # Desk phone extension
                
                # Location & Organization
                "office",                   # Physical office location
                "department",               # Which team/department they belong to
                "title",                    # Job role
                "company",                  # Organization name
                "manager",                  # Their supervisor (helps build org charts)
                "streetaddress",            # Physical address
                "l",                     # City for location context
                "st",                    # State/Province for location context
                "postalcode",               # Postal code for location context
                "co"                        # country
                "ou",                       # Organizational Unit
                
                # Security & Access
                "memberof",                 # Security and distribution groups (determines permissions)
                "accountexpirationdate",    # When access ends (for contractors/temps)
                "enabled",                  # Whether the account is active
                "pwdlastset",               # Password security status (PasswordLastSet)
                "passwordexpired",          # Password security status
                "lockedout",                # If account is locked due to failed logins
                "useraccountcontrol",       # Account control flags
                "admincount",               # Indicates privileged account
                "serviceprincipalname",     # Service account identification
                "iscriticalsystemobject",   # System-critical account flag
                
                # Backend/System Attributes
                "objectguid",               # Unique system identifier
                "sid",                      # Security identifier for Windows
                "objectclass",              # Defines it as a user object
                "whencreated",              # Audit timestamps
                "whenchanged",              # Audit timestamps
                "lastlogondate",            # System tracking (useful for access reviews)
                "lastlogon",                # Last logon timestamp
                
                # Additional
            ]

        elif input_type == "groups":
            ad_attributes = ["adminCount","CanonicalName","CN","Created","Deleted","Description","DisplayName","DistinguishedName","GroupCategory","HomePage","ManagedBy","member","MemberOf","Members","Modified","modifyTimeStamp","Name","SamAccountName","SID","whenChanged","whenCreated"]
        elif input_type == "computers":
            ad_attributes = ["AccountNotDelegated","AllowReversiblePasswordEncryption","BadLogonCount","badPasswordTime","badPwdCount","CannotChangePassword","CanonicalName","CN","createTimeStamp","Description","DisplayName","DistinguishedName","DNSHostName","DoesNotRequirePreAuth","Enabled","IPv4Address","IPv6Address","KerberosEncryptionType","LastBadPasswordAttempt","lastLogoff","LastLogonDate","Location","LockedOut","ManagedBy","MemberOf","modifyTimeStamp","Name","OperatingSystem","OperatingSystemHotfix","OperatingSystemServicePack","OperatingSystemVersion","PasswordExpired","PasswordLastSet","PasswordNeverExpires","PasswordNotRequired","PrincipalsAllowedToDelegateToAccount","pwdLastSet","sAMAccountType","ServiceAccount","servicePrincipalName","SID","TrustedForDelegation","TrustedToAuthForDelegation"]
    else:
        ad_attributes = None
    # testing - give input file
    script_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_path, 'users.json')

    # Sample data
    
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())
    
    if json_data['results']: 
        json_data = json_data['results']

    
    if ad_attributes is None: 
        # Extract all unique keys from all JSON objects
        ad_attributes = set()
        for item in json_data:
            ad_attributes.update(item.keys())
    
    # Convert to sorted list for consistent column ordering
    fields_to_extract = sorted(list(ad_attributes))
    
    # Convert to CSV
    csv_output = json_to_csv(json_data, fields_to_extract)
    
    # Print with proper encoding handling
    # Simply print the output - sys.stdout is already configured for UTF-8
    print(csv_output, end='')
    