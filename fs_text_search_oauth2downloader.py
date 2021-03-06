#------------------------------------------------------------
'''
A python script to do basic text search on freesound.org with tags and download the original
sound files to the specified directory using oauth2.

This script uses freesound-python client library to interact with the freesound.org api
https://github.com/MTG/freesound-python


Albin Andrew Correya
'''

#------------------------------------------------------------

import ast,sys,os,time
import freesound
import subprocess
import webbrowser


client_id = "YOUR CLIENT_ID HERE"
token = "YOUR CLIENT_SECRET HERE"

url = 'https://www.freesound.org/apiv2/oauth2/authorize/?client_id=' + client_id + \
			'&response_type=code&state=xyz'

webbrowser.open(url, new = 2) #opens the url in a new tab in your default web browser automatically.

code = raw_input('\nPlease go to: '+ url +'\nEnter the given code from the response: ')


print '\n Authenticating:\n'

req = 'curl -X POST -d "client_id=' + client_id + '&client_secret=' + token + \
			'&grant_type=authorization_code&code=' + code + '" ' + \
			'"https://www.freesound.org/apiv2/oauth2/access_token/"'

output = subprocess.check_output(req, shell=True)
output = ast.literal_eval(output)
access_oauth = output['access_token']
refresh_oauth = output['refresh_token']


client = freesound.FreesoundClient()
client.set_token(access_oauth,auth_type='oauth')
print "\nSuccessfully Authorized..."


#create a folder in your working directory
download_folder = os.getcwd()+'/downloads/'

text_query = raw_input('\nEnter your text query to search :')
tag = raw_input('\n Enter the tag to filter :')

results_pager = client.text_search(query=text_query,filter="tag:"+tag+" duration:[2.0 TO 100.0]",\
				fields="id,name,url,type",page_size=50)

print "\nNum results:", results_pager.count

pages = results_pager.count/50

print "\n\t----- PAGE 1 -----"
for sound in results_pager:
	name = sound.name
	sname = name.replace('/','')
	sound.retrieve(sound.url,download_folder+str(sound.id)+'__'+sname+ '.' +sound.type)
	print '\n Downloading finsihed for sound >>', sound.id

print "\n Finished downloading page one..."

time.sleep(5) # used to delay the request process time since freesound api only allows 60 requests per minute.

j = 1
if pages>1:
	for i in range(pages):
		if i<6:
			print '\n\t----- PAGE '+str(j+1)+' -----'
			results_pager = results_pager.next_page()
			for sound in results_pager:
				name = sound.name
				sname = name.replace('/','')
				sound.retrieve(sound.url,download_folder+str(sound.id)+'__'+sname+ '.' +sound.type)
				print '\n Downloading finsihed for sound >>', sound.id
			print '\n Finished downloading page ',str(j+1)
			j=j+1
			time.sleep(5)  # used to delay the request process time since freesound api only allows 60 requests per minute.
 
