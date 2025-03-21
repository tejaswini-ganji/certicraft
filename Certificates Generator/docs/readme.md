# Introduction
This project is a certificate generator that creates personalized certificates based on a given template and candidate details provided in an Excel sheet.

## Version 1.0
Initially, the application was built to generate certificates for each candidate mentioned in the Excel sheet.
The generated certificates were saved as PNG and PDF files in the output directory.
## Version 2.0
In this version, an email feature was added.
The generated certificates were automatically sent to the respective email addresses mentioned in the Excel sheet using SMTP.
## Roadblocks & Challenges Faced
1. **SMTP Credentials & Security Issues**

    Initially, when setting up SMTP, Gmail rejected my credentials due to security concerns. Here’s how I resolved it:
    
    - App Password Requirement
    SMTP requires an App Password, which is a 16-character password used for authentication instead of your actual Gmail password.
    The app password contains spaces, which caused issues when storing it in .env.
    - Storing Credentials Securely
    To store sensitive credentials securely, I explored two methods:
    
    ▶ Method 1: Using Environment Variables (.env)
   
   • can store the SMTP credentials as system environment variables, which will keep them secure and accessible within the script.
         This method works without any issues, as it avoids parsing errors caused by spaces in the app password.
   
    ▶ Method 2: Using a config.json File (Implemented)
   
    • Instead of .env, I used a config.json file to store SMTP details securely.
          Example config.json:
 
          {
          
            "email": "your_email@gmail.com",
            
            "app_password": "your-16-character-app-password",
            
          }
    
    This method worked without issues and provided a clean way to store credentials.
    
2. **Email Delivery Issues (Spam Folder Problem)**

   Initially, the emails were received in the Spam folder instead of the inbox. To fix this, I took the following steps:
  
  - Steps to Reduce Spam Detection
     - Avoided Spam Trigger Words
     
       Words like "Congratulations!", "Click Here!", "Lottery Won!", etc., are often flagged as spam.
    
       I ensured that the email content was simple and professional.
       
       Added Reply-To Header
      
      - Adding msg["Reply-To"] = "your_email@gmail.com" increased email trustworthiness.
      
      - Added a Delay Between Emails.Since SMTP servers detect bulk emails as spam if too many are sent at once.
      I introduced a time delay ( time.sleep(10)) between sending each email to avoid triggering spam filters.
      
3. **SMTP Connection Issues & Security Fixes**
   
     At first, Gmail rejected the SMTP connection because it considered the app as "less secure."
  
    - Switching to TLS for Higher Security
       Initially, my emails were being blocked because Gmail detected an insecure connection.
       I resolved this by switching to TLS encryption (Transport Layer Security):
       This increases security and prevents unauthorized access.

