import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import json
# Setup port number and server name

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = "ralphbonner8@gmail.com"
email_list = ["ralphbonner8@gmail.com"]

# Define the password (better to reference externally)
pswd = "jphd njil nhre grqj" # As shown in the video this password is now dead, left in as example only


# name the email subject
subject = "New email from TIE with attachments!!"



# Define the email function (dont call it email!)
def send_emails(email_list):

    for person in email_list:

      # Make the body of the email
      body = f"""
      line 1
      line 2
      line 3
      etc
      """

      # make a MIME object to define parts of the email
      msg = MIMEMultipart()
      msg['From'] = email_from
      msg['To'] = person
      msg['Subject'] = subject

      # Attach the body of the message
      msg.attach(MIMEText(body, 'plain'))

      # Define the file to attach
      filename1 = ""
      
      for file in os.listdir("/tmp"):
        if file.startswith("trivy"):
          filename1 = file
      print(f"filename is {filename1}")
      filename1="/tmp/"+filename1
      # print(f"filename is {filename1}")

      def json_to_html(json_data):
        html_content = "<html><body><table border='1'><tr><th>Severity</th><th>PkgName</th><th>Title</th></tr>"
        for result in json_data.get("Results", []):
            for vulnerability in result.get("Vulnerabilities", []):
                html_content += f"<tr><td>{vulnerability['Severity']}</td><td>{vulnerability['PkgName']}</td><td>{vulnerability['Title']}</td></tr>"
        html_content += "</table></body></html>"
        return html_content

      def write_html_file(html_content, filename):
          with open(filename, "w") as html_file:
              html_file.write(html_content)
          print(f"HTML file '{filename}' has been created successfully.")
          
      # try:
      # with open(filename1, "r") as json_file:
      #       json_data = json.load(json_file)
      # except json.JSONDecodeError as e:
      #       print("Error decoding JSON:", e)
      #       json_data = None
    
      # print(json_data)

      # html_content = json_to_html(json_data)

      # # Write HTML to file
      # write_html_file(html_content, "output.html")

      # Open the file in python as a binary
      attachment= open(filename1, 'rb')  # r for read and b for binary

      # Encode as base 64
      attachment_package = MIMEBase('application', 'octet-stream')
      attachment_package.set_payload((attachment).read())
      encoders.encode_base64(attachment_package)
      # f2=""
      # for file in os.listdir():
      #   if file=="output.html":
      #     f2=file
      #     print(file)
      attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename1)
      msg.attach(attachment_package)

      # Cast as string
      text = msg.as_string()

      # Connect with the server
      print("Connecting to server...")
      TIE_server = smtplib.SMTP(smtp_server, smtp_port)
      TIE_server.starttls()
      TIE_server.login(email_from, pswd)
      print("Succesfully connected to server")
      print()


      # Send emails to "person" as list is iterated
      print(f"Sending email to: {person}...")
      TIE_server.sendmail(email_from, person, text)
      print(f"Email sent to: {person}")
      print()

      # Close the port
      TIE_server.quit()


# Run the function
send_emails(email_list)