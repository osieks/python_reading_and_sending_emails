import email
import imaplib
import re
import csv
import time
from datetime import datetime

unique_first_items = []

def extract_lines_from_list(xlist):
    return [line.strip() for line in xlist
        if 'Detected Time:' in line
        or 'Job ID:' in line
        or 'Client:' in line
        or 'Storage Policy Name:' in line
        or 'Copy Name:' in line
        or 'Agent Type:' in line
        or 'Backup Set:' in line
        or 'Subclient:' in line
        or 'Failure Reason:' in line
        ]


#CLEANR = re.compile('<.*?>') 
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
TAG_RE = re.compile(r'<[^>]+>')

def cleanhtml(raw_html):
    return re.sub(TAG_RE, '', raw_html)

def list_without_empty_lines(text):
    lines = text.split('\n')
    list_of_lines = []
    for line in lines:
        if line.strip():
            #print(line)
            list_of_lines.append(line)
    return list_of_lines

def mail_content_to_csv(csv_writer,mail_content):
    content_of_email = list_without_empty_lines(cleanhtml(mail_content))
    print(content_of_email)

    extracted_data = extract_lines_from_list(content_of_email)
    extracted_data = [item.split(':', 1)[-1].strip() for item in extracted_data]

    print("data po ekstakrcji")
    print(extracted_data)

    try:
        Job_ID = extracted_data[1] if extracted_data else None
        if Job_ID not in unique_first_items:
            unique_first_items.append(Job_ID)
            csv_writer.writerow(extracted_data)
    except:
        Job_ID = 000
        csv_writer.writerow(extracted_data)
    

def read_and_print_errors(EMAIL,PASSWORD,SERVER,email_folder,csv_file):

    csv_writer = csv.writer(csv_file)
   
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select(email_folder)
    #print(mail.list())
    #status, data = mail.search(None, 'ALL')
    #exit()
    status, data = mail.search(None, 'UNSEEN')
    mail_ids = []

    #print(data)

    if(data == [None]):
        return 0

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            mail_content = part.get_payload(decode=True)
                            if mail_content is not None:
                                mail_content = mail_content.decode(errors='replace')
                            break
                else:
                    mail_content = message.get_payload(decode=True)
                    if mail_content is not None:
                        mail_content = mail_content.decode(errors='replace')


                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                #print(f'Content: {cleanhtml(mail_content)}')
                mail_content_to_csv(csv_writer,mail_content)
                

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    EMAIL = 'mateusz.dziezok@coig.pl'
    PASSWORD = '~ZFzR6rsGBUZGS_z'
    SERVER = 'mx.coig.pl'
    email_folders = ('CommVault/Errors','CommVault/Failed')
    output_csv = "file"+datetime.today().strftime('%Y-%m-%d---')+".csv"
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        for folder in email_folders:
            read_and_print_errors(EMAIL,PASSWORD,SERVER,folder,csv_file)