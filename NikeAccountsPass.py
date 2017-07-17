#Script to change password in a list of nike+ accounts
#Works for Nike US and Nike EU
#The account file should contain email:password in each line for each account

ACCOUNTFILENAME="nikeaccounts.txt"

COUNTRY="US"
NEWPASSWORD="PASSWORD HERE"


#Do not change below this line

import json
import requests
from threading import Thread
import Queue
def changepass(email,password,newpassword):
	sess=requests.session()
	print "Logging in to {0}".format(email)
	if COUNTRY=="US":
		sess.cookies["CONSUMERCHOICE"]="us/en_us"
		sess.cookies["NIKE_COMMERCE_COUNTRY"]="US"
		sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_US"
		sess.cookies["nike_locale"]="us/en_US"
		e=sess.post("https://unite.nike.com/loginWithSetCookie?appVersion=239&experienceVersion=206&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=default&browser=Google%20Inc.&os=undefined&mobile=false&native=false",json={"username":email,"password":password,"client_id":"HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH","ux_id":"com.nike.commerce.nikedotcom.web","grant_type":"password"})
	else:
		sess.cookies["CONSUMERCHOICE"]="gb/en_gb"
		sess.cookies["NIKE_COMMERCE_COUNTRY"]="GB"
		sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_GB"
		sess.cookies["nike_locale"]="gb/en_GB"
		e=sess.post("https://unite.nike.com/loginWithSetCookie?appVersion=281&experienceVersion=244&uxid=com.nike.commerce.nikedotcom.web&locale=en_GB&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false",json={"username":email,"password":password,"client_id":"HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH","ux_id":"com.nike.commerce.nikedotcom.web","grant_type":"password"})
	e.raise_for_status()
	TOKEN=json.loads(e.text)['access_token']
	user=json.loads(e.text)["user_id"]
	e=sess.put("https://www.nike.com/profile/services/users/{0}/password".format(user),headers={"Content-Type":"application/json","X-Requested-With":"XMLHttpRequest"},json={"password":password,"newPassword":newpassword,"passwordConfirm":newpassword})
	e.raise_for_status()
alls=open(ACCOUNTFILENAME,'r').read().split('\n')
alls=[p.strip().split(":",1) for p in alls if p.strip()!=""]
alls1=Queue.Queue()
for p in alls:
	alls1.put(p)
def change1():
	while True:
		try:
			emp=alls1.get_nowait()
		except:
			return
		try:
			changepass(emp[0],emp[1],NEWPASSWORD)
			print "Successfully changed password for {0}".format(emp[0])
		except Exception as e:
			print "Failed to change password for {0}".format(emp[0])
			print e
for i in range(0,20):
	Thread(target=change1).start()
