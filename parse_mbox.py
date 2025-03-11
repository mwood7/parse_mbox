#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_mbox: parse a standard mbox file.  Writes all attachments and message
bodies to output files with a leading running index.

Change file and directory names at bottom of code for your purposes.

Author: M. Wood (using ChatGPT)
March 2025
"""

import mailbox
import os
import email
from email.policy import default
import re

def sanitize_filename(name):
    """Sanitize filenames by removing special characters."""
    return re.sub(r'[\/:*?"<>|]', '_', name)

def remove_leading_underscores(filename):
    """Removes leading underscores from a filename."""
    while filename.startswith("_"):
        filename = filename[1:]
    return filename

def extract_mbox_attachments(mbox_file, output_dir):
    """Extract attachments and save email bodies for messages without attachments."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mbox = mailbox.mbox(mbox_file, factory=lambda f: email.message_from_binary_file(f, policy=default))
    counter = 1

    for message in mbox:
        sender = message.get("From", "unknown_sender")
        sender = sanitize_filename(sender)

        has_attachment = False

        if message.is_multipart():
            for part in message.iter_attachments():
                filename = part.get_filename()
                if filename:
                    filename = sanitize_filename(filename)
                    fname = f"{counter:04}_{sender}_{filename}".replace(" ","")
                    fname = remove_leading_underscores(fname)
                    file_path = os.path.join(output_dir, fname)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Saved attachment: {file_path}")


        body = None
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = message.get_payload(decode=True).decode(errors="ignore")

        if body:
            file_path = os.path.join(output_dir, f"{counter:04}_{sender}_msg.txt".replace(" ",""))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(body)
            print(f"Saved email body: {file_path}")
                
        counter += 1

# Example usage
mbox_file = "v1674her.mbox"   # Replace with your mbox file name
output_dir = "output_folder"  # Replace with your desired output folder
extract_mbox_attachments(mbox_file, output_dir)
