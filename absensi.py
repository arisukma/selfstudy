from datetime import datetime, timedelta
import time
import requests
import urllib as ulib
from bs4 import BeautifulSoup
import random
import json

randtime = random.randint(1,2)
time.sleep(randtime)

mode = "clockin"
idpeg = "xxxxxxxx"
homeurl = "https://apps.pertamina.com"
WIB = "-420"
longi = "101.443633"
lati = "0.574720"
nomorhp = "0xxxxxx"
if datetime.now().weekday()>=5:
    worksystem = "7"  # 1:WFH 2:WFO 7:harilibur 8:cuti 9:Dinas
else:
    worksystem = "1"  # 1:WFH 2:WFO 7:harilibur 8:cuti 9:Dinas
clocknow =  datetime.now().strftime("%d.%m.%Y %H:%M:%S")
healthdata = {"EmployeeID":"19266721","IsTKJP":"0",
                          "Email":"ari.negara@pertamina.com","EmployeeName":"Ari Sukma Negara",
                          "CompanyCode":"2202","Directorate":"PHR",
                          "WorkFunction":"Information Technology",
                          "WorkLocation":"145","WorkSystem":worksystem,
                          "WorkObstacles":"tidak ada","MobileNumber":nomorhp,
                          "IsolationEmployee":"0","IsolationReason_Contact":0,
                          "IsolationReason_PCR":0,"IsolationReason_Symptoms":0,
                          "IsolationReason_WaitPCR":0,
                          "ComorbidCancer":0,"ComorbidDiabetes":0,
                          "ComorbidAsthma":0,"ComorbidAutoImun":0,
                          "ComorbidHepatitis":0,"ComorbidHeart":0,
                          "ComorbidHipertensi":0,"ComorbidKidney":0,
                          "DiagnosedCovid":"0",
                          "HealthMonitoringTimeClient":clocknow,
                          "BrowserType":"Chrome 96.0.4664.93","Latitude":float(lati),"Longitude":float(longi),
                          "IsolationConsultation":"",
                          "IsolationDays ":"",
                          "IsolationWhere":"",
                          "IsolationTemperature":"",
                          "IsolationSaturartion":"",
                          "IsolationSaturartionDesc":"",
                          "IsolationComplaints":"",
                          "IsolationDrugs":"",
                          "IsolationObstacle":"",
                          "IsolationFamilyDesc":"",
                          "ConditionDesc":"",
                          "Sick":"",
                          "Incare":"",
                          "ContactName":"",
                          "ContactNumber":"",
                          "ContactVisit":"",
                          "ConditionFamilyDesc":"",
                          "DrugsConsumeDesc":"",
                          "Height":"",
                          "Weight":"",
                          "WorkLocationDesc":""
             }

###RETREIVE ENCRYPTED SESSION ID#####
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
read1 = s.get(homeurl+'/myattendance/Account/LoginByIdentity')
session_id = BeautifulSoup(read1.text,'lxml').find_all('input', {'name' : "AntiforgeryFieldname"})[0]['value']

###LOGGING IN TO SYTEM##############
header = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https://apps.pertamina.com/myattendance/Account/LoginByIdentity'}
read2 = s.post(homeurl+'/myattendance/Account/SignInByEmployeeNumber',
             data = {'txtEmployeeNumber' : idpeg, 'AntiforgeryFieldname' : session_id}, headers = header)

###SUBMIT HEALTH MONITORING ##############
headerx = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'apps.pertamina.com',
            'Origin' : 'https://apps.pertamina.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-length' :'2234',
            'Referer': 'https://apps.pertamina.com/myattendance/HealthMonitoring/Index'}
readx = s.post(homeurl+'/myattendance/HealthMonitoring/Submit',
            data = {"jsonInput" : json.dumps(healthdata)},
            headers = headerx)

###SUBMIT CLOCK IN ##############
randtime = random.randint(1,5)
time.sleep(randtime) ###give delay to submission time to avoid susipicious activity
clocknow =  datetime.now().strftime("%d.%m.%Y %H:%M:%S")
#header3 = {'Content-Type': 'application/json;charset=utf-8', 'Referer': 'https://apps.pertamina.com/myattendance/Attendance/Index'}
header3  = {'Content-type': 'application/x-www-form-urlencoded'}
#clockinencode = ulib.parse.quote('{"EmployeeID":"'+idpeg+'", "WorkSystem":"'+worksystem+'", "ClockInTimeClient":"'+clocknow+'", "ClockInTimeZone":'+WIB+', "Longitude":'+longi+', "Latitude":'+lati+'}')
clockindata = {
    "EmployeeID":idpeg,
    "WorkSystem":worksystem,
    "ClockInTimeClient":clocknow,
    "ClockInTimeZone":int(WIB),
    "Longitude":float(longi),
    "Latitude":float(lati)
}
#read3 = s.get(homeurl+'/myattendance/Attendance/InsertClockIn?json='+clockinencode, headers = header3)
read3 = s.post(homeurl+'/myattendance/Attendance/InsertClockIn',
            data = {"jsonInput" : json.dumps(clockindata)},
            headers = header3)

print("health submission status {}".format(readx.json()))
print("clockin status {}".format(read3))

messagesent = "health submission status {} clockin status : {}".format(readx.json() , read3)
from email.message import EmailMessage
import smtplib,ssl
def send_mail(to_email, subject, message, server='smtp.example.cn',from_email='xx@example.com'):
    # import smtplib
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg.set_content(message)
    print(msg)
    server = smtplib.SMTP(server, 25)
    context = ssl.create_default_context()
    server.send_message(msg)
    server.quit()
    print('successfully sent the mail.')

send_mail(["ari.negara@pertamina.com"], "status absensi pagi", messagesent,
          server = 'smtp.rokan.local',from_email="absensi@pertamina.com")