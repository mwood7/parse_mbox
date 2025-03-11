If you need to parse an mbox file and write out all the attachments and message bodies to separate files, you may find parse_mbox.py to be useful. I needed such a program and couldn't find what I wanted with an internet search, so I gave ChatGPT prompts until I got something I could modify to satisfy my own needs.  

The code is very simple.  You enter your file name and desired output directory name at the bottom, and run.

The code steps through the email messages one-by-one, saving attachments with the following format ```{index}_{sender}_{attachment name}``` where any white space or special characters in the string are removed.  The message bodies are saved in files with the name format ```{index}_{sender}_msg.txt``` (even if there is an empty message body).  All files for a given email will have the same index.  

Created March 2025
