from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import imaplib
import smtplib
import urllib
import os
import cv2
import pytesseract
from PIL import Image

mail = imaplib.IMAP4_SSL('imap.gmail.com')
(retcode, capabilities) = mail.login('new.check8@gmail.com','@@check@@')
mail.list()
mail.select('inbox')

n=0
(retcode, messages) = mail.search(None, '(UNSEEN)')
# if retcode == 'OK':
print(messages)
domain_name=[]
links_in_email  = []
percentage = 0
def compare(domain, links,percentage):
    # percentage = 0
    print(domain)
    domain_at_split = domain[1].split('@')[1]
    if(len(domain_at_split.split('.'))>2):
        percentage+=80
    does_not_match = False
    i=0
    for link in links:
        if(domain_at_split==link):
            domain_split_by_dot = domain_at_split.split('.')
            link_split_by_dot = link.split('.')
            z=0
            while z<len(domain_split_by_dot) or z<len(link_split_by_dot):
                i=0
                j=0
                try:
                    while(i<len(domain_split_by_dot[z]) or j<len(link_split_by_dot[z])):
                        if(domain_split_by_dot[z][i]==link_split_by_dot[z][j]):
                            j += 1
                            i += 1
                            continue
                        else:
                            does_not_match = True
                            break
                except Exception as  e:
                    print(e)
                    # percentage+=5
                    does_not_match = True
                    break
                z+=1
                if(does_not_match==True):
                    break
            # print(match)
        else:
            # percentage+=15
            continue
        if (does_not_match == True):
            percentage+=15
            break
    return percentage
email_from = ''
for num in messages[0].split() :
      print ('Processing ')
      # n=n+1
      typ, data = mail.fetch(num,'(RFC822)')
      for response_part in data:
         if isinstance(response_part, tuple):
             content_of_image = ''
             message = email.message_from_string(response_part[1])

             if message.is_multipart():
                 mail_content = ''
                 mail_contents = ''
                 # on multipart we have the text message and
                 # another things like annex, and html version
                 # of the message, in that case we loop through
                 # the email payload
                 for part in message.get_payload():
                     # if the content type is text/plain
                     # we extract it
                     if part.get_content_type() == 'text/html':
                         mail_content += part.get_payload()
                         mail_contents = mail_content.split("\r\n")

             else:
                 mail_content = message.get_payload()
                 mail_contents = mail_content.split("\r\n")
             i = 1
             sources_of_imgs = []
             while i < len(mail_content.split('src=3D"')):
                 if (mail_content.split('src=3D"')[i].split('"')[0].split('.')[
                     len(mail_content.split('src=3D"')[i].split('"')[0].split('.')) - 1] == 'png' or
                         mail_content.split('src=3D"')[i].split('"')[0].split('.')[
                             len(mail_content.split('src=3D"')[i].split('"')[0].split('.')) - 1] == 'jpg'):
                     sources_of_imgs.append(mail_content.split('src=3D"')[i].split('"')[0])
                 i += 1
             print(sources_of_imgs)
             i = 0
             while i < len(sources_of_imgs):
                 try:
                     # print(sources_of_imgs[i].split('.')[len(sources_of_imgs[i].split('.'))-2].split('/')[len(sources_of_imgs[i].split('.')[0].split('/'))])
                     urllib.urlretrieve(sources_of_imgs[i], str(i) + '.png')
                     if bool(str(i) + '.png'):
                         filePath = os.path.join('C:\\Users\\', str(i) + '.png')
                         if not os.path.isfile(filePath):
                             fp = open(filePath, 'wb')
                             fp.write(part.get_payload(decode=True))
                             fp.close()
                         # subject = str(message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                         # latest_email_uid = "new world"
                         # print(fileName)

                         img = cv2.imread('C:\\Users\\' + str(i) + '.png')

                         # filename = "{}.png".format(os.getpid())
                         # print(filename)

                         # cv2.imwrite(filename, img)

                         # Load the image using PIL (Python Imaging Library), Apply OCR, and then delete the temporary file
                         content_of_image = pytesseract.image_to_string(Image.open(str(i) + '.png'))
                         print(content_of_image.split('.'))
                         if (content_of_image.split('.')[0] == 'www' and content_to_client[1].split('.')[0] == 'www'):
                             if (content_of_image.split('.')[1] == content_to_client[1].split('.')[1]):
                                 percentage = percentage
                             else:
                                 percentage += 5
                         elif (content_of_image.split('.')[0] != 'www' and content_to_client[1].split('.')[0] != 'www'):
                             if (content_of_image.split('.')[0] == content_to_client[1].split('.')[0]):
                                 percentage = percentage
                             else:
                                 percentage += 5
                         elif (content_of_image.split('.')[0] == 'www' and content_to_client[1].split('.')[0] != 'www'):
                             if (content_of_image.split('.')[1] == content_to_client[1].split('.')[0]):
                                 percentage = percentage
                             else:
                                 percentage += 5
                         elif (content_of_image.split('.')[0] != 'www' and content_to_client[1].split('.')[0] == 'www'):
                             if (content_of_image.split('.')[0] == content_to_client[1].split('.')[1]):
                                 percentage = percentage
                             else:
                                 percentage += 5
                         os.remove(str(i) + '.png')
                         break

                 except Exception as e:
                     print(e)
                     break
                 i += 1

             original = email.message_from_string(response_part[1])

            # print (original['From'])
            # print (original['Subject'])
             raw_email = data[0][1]
             raw_email_string = raw_email.decode('utf-8')
             email_message = email.message_from_string(raw_email_string)
             for part in email_message.walk():
                        if (part.get_content_type() == "text/plain"): # ignore attachments/html
                              body = part.get_payload(decode=True)
                              # save_string = str(r"C:\Users\DAR\Desktop\Dumpemail_" + str('richboy') + ".txt" )
                              # myfile = open(save_string, 'a')
                              email_from = original['From']
                              print(original['From']+'\n')
                              # print(original['Subject']+'\n')
                              print (body.split('\r\n'))
                              print ('**********\n')
                              domain_name = []
                              links_in_email = []
                              domain_name.append('Domain Name: ')
                              domain_name.append(body.split('<')[1].split('>')[0])
                              links_in_email.append('Links: ')
                              for part in body.split('\r\n'):
                                # print part
                                try:
                                  if(part[1]=='h' and part[2]=='t' and part[3]=='t' and part[4]=='p' and part[5]=='s'):
                                      https_split = part.split('https://')[1]
                                      https_split_f_slash_split = https_split.split('/')
                                      # print https_split_f_slash_split[0]
                                      links_in_email.append(https_split_f_slash_split[0])
                                      for link in links_in_email:
                                          if(link == https_split_f_slash_split[0]):
                                              break
                                          else:
                                              links_in_email.append(https_split_f_slash_split[0])

                                  if (part[1] == 'h' and part[2] == 't' and part[3] == 't' and part[4] == 'p'and part[5]!='s'):
                                      http_split = part.split('http://')[1]
                                      http_split_f_slash_split = http_split.split('/')
                                      # print http_split_f_slash_split[0]
                                      for link in links_in_email:
                                          if(link == http_split_f_slash_split[0]):
                                              break
                                          else:
                                              links_in_email.append(http_split_f_slash_split[0])

                                  # input('Press enter: ')
                                except:
                                    continue
                              # myfile.close()
                              percentage = compare(domain_name, links_in_email,percentage)
                              print(domain_name)
                              print(links_in_email)
                              print(percentage)
                              mail_content = 'Domain of the Email: ' + domain_name[1] + ' ' + ' and phishing percentage is ' + str(percentage) + '%'

                              message = MIMEMultipart()
                              message['From'] = 'new.check8@gmail.com'
                              message['To'] = email_from
                              message['Subject'] = 'Phishing Percentage'  # The subject line
                              # The body and the attachments for the mail
                              message.attach(MIMEText(mail_content, 'plain'))
                              # Create SMTP session for sending the mail
                              session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
                              session.starttls()  # enable security
                              session.login('new.check8@gmail.com', '@@check@@')  # login with mail_id and password
                              text = message.as_string()
                              session.sendmail('new.check8@gmail.com', email_from, text)
                              session.quit()
                              print('Mail Sent')
                        else:
                              # domain_name.append('Null')

                              continue
             for part in email_message.walk():
                 # this part comes from the snipped I don't understand yet...
                 if part.get_content_maintype() == 'multipart':
                     continue
                 if part.get('Content-Transfer-Encoding') is None:
                     # print(part.get_filename)
                     # print("part.get_filename")
                     continue
                 fileName = part.get_filename()
                 if bool(fileName):
                     filePath = os.path.join('C:\\Users\\DAR\\Le\\', fileName)
                     if not os.path.isfile(filePath):
                         fp = open(filePath, 'wb')
                         fp.write(part.get_payload(decode=True))
                         fp.close()
                     subject = str(message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                     latest_email_uid = "new world"
                     print(fileName)

                     img = cv2.imread('C:\\Users\\DAR\\Le\\' + fileName)

                     filename = "{}.png".format(os.getpid())
                     print(filename)

                     cv2.imwrite(filename, img)

                     # Load the image using PIL (Python Imaging Library), Apply OCR, and then delete the temporary file
                     content_of_image = pytesseract.image_to_string(filename)
                     print(content_of_image.split('.'))
                     if (content_of_image.split('.')[0] == 'www' and content_to_client[1].split('.')[0] == 'www'):
                         if (content_of_image.split('.')[1] == content_to_client[1].split('.')[1]):
                             percentage = percentage
                         else:
                             percentage += 5
                     elif (content_of_image.split('.')[0] != 'www' and content_to_client[1].split('.')[0] != 'www'):
                         if (content_of_image.split('.')[0] == content_to_client[1].split('.')[0]):
                             percentage = percentage
                         else:
                             percentage += 5
                     elif (content_of_image.split('.')[0] == 'www' and content_to_client[1].split('.')[0] != 'www'):
                         if (content_of_image.split('.')[1] == content_to_client[1].split('.')[0]):
                             percentage = percentage
                         else:
                             percentage += 5
                     elif (content_of_image.split('.')[0] != 'www' and content_to_client[1].split('.')[0] == 'www'):
                         if (content_of_image.split('.')[0] == content_to_client[1].split('.')[1]):
                             percentage = percentage
                         else:
                             percentage += 5
                     os.remove(str(i) + '.png')
                     break
