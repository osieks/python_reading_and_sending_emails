# CommVault Error Reporting Script

This Python script automates the process of checking for new CommVault error emails, extracting relevant information, and sending a summary report.

## Features

- Connects to an email server using IMAP
- Searches for unread emails in specified folders
- Extracts key information from CommVault error emails
- Generates an HTML table with the extracted data
- Sends a summary email with the compiled information

## Prerequisites

- Python 3.x
- Access to an IMAP-enabled email account
- CommVault system generating error emails

## Configuration

Before running the script, you need to set up the following variables in the script:

- `glob_EMAIL`: The email address to send from and check for errors
- `glob_EMAIL_FOLDERS`: A tuple of folder names to search for error emails
- `glob_SENDTO`: Comma-separated list of email addresses to send the report to
- `glob_PASSWORD`: The password for the email account (stored in a separate `secret.py` file)
- `glob_SERVER`: The IMAP server address

## Usage

1. Ensure all dependencies are installed.
2. Set up the `secret.py` file with your email password.
3. Configure the global variables as described above.
4. Run the script:

   ```
   python script_name.py
   ```

The script will automatically process new emails and send a summary report.

## Security Note

This script uses a separate `secret.py` file to store the email password. Ensure this file is kept secure and not shared or committed to version control.

## Customization

You can modify the `extract_lines_from_list` function to change which information is extracted from the emails.

## License

[Specify the license here]

## Contributing

[Specify how others can contribute to this project]

## Support

For support, please contact [Your Contact Information].
