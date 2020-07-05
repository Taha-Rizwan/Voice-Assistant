import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import time
import threading

API_KEY = 'tQhUoxabuwp6'
PROJECT_TOKEN = "tdBj4sh2q7vT"
RUN_TOKEN = "tXKkDrVfat-c"
response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={'api_key':API_KEY})
data = json.loads(response.text)

class Data:
	def __init__(self, api_key, project_token):
		self.api_key = api_key
		self.project_token = project_token
		self.params = {
			"api_key": self.api_key
		}
		self.data = self.get_data()

	def get_data(self):
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
		data = json.loads(response.text)
		return data

	def get_total_cases(self):
		data = self.data['total']

		for content in data:
			if content['name'] == "Coronavirus Cases:":
				return content['value']

	def get_total_deaths(self):
		data = self.data['total']

		for content in data:
			if content['name'] == "Deaths:":
				return content['value']

		return "0"

	def get_total_recovered(self):
		data = self.data['total']

		for content in data:
			if content['name'] == "Recovered:":
				return content['value']

		return "0"

	def get_country_data(self, country):
		data = self.data["country"]

		for content in data:
			if content['name'].lower() == country.lower():
				return content

		return "0"

	def get_list_of_countries(self):
		countries = []
		for country in self.data['country']:
			countries.append(country['name'].lower())

		return countries

	def update_data(self):
		response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

		def poll():
			time.sleep(0.1)
			old_data = self.data
			while True:
				new_data = self.get_data()
				if new_data != old_data:
					self.data = new_data
					print("Data updated")
					break
				time.sleep(5)


		t = threading.Thread(target=poll)
		t.start()


def speak(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()


def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio, language='en-GB')
		except Exception as e:
			print("Exception:", str(e))

	return said.lower()


def main():
	print("Started Program")
	data = Data(API_KEY, PROJECT_TOKEN)
	END_PHRASE = "stop" or "end"
	master = 'Taha the great'
	country_list = data.get_list_of_countries()
	Duh = 'Duh'
	Hi = 'Hi'
	nice = 'nice'
	maybe = 'maybe'
	beatbox = 'beatbox'
	Thanks = 'Thanks'
	ans='ans'
	hadi='hadi'
                

                
	TOTAL_PATTERNS = {
	re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
	re.compile("[\w\s]+ total cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
	 re.compile("[\w\s]+ total [\w\s]+ recovered"): data.get_total_recovered,
                    re.compile("[\w\s]+ total recovered"): data.get_total_recovered
	
					}

	COUNTRY_PATTERNS = {
	    re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]+")or('[\w\s+death [\w\s]+'): lambda country: data.get_country_data(country)['total_deaths'],
	     re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: data.get_country_data(country)['total_recovered'],
					}
	WEIRD_PATTERNS={
		re.compile('who is your master'):master
		}
	
	GREETING_PATTERNS = {
		re.compile('hello'):Hi,
		re.compile('hi'):Hi,
		re.compile('hey'):Hi}
	FEEL_PATTERNS={
		re.compile('i am fine'):nice,
		re.compile('i am [\w\s]'):nice}
	ROBO_PATTERNS={
		re.compile('are you a robot'):maybe,
		re.compile('are you a human'):maybe,
		re.compile('what is your name'):maybe,
		re.compile('who are you'):maybe
		
		}
	BEATBOX_PATTERNS={
                re.compile('beatbox'):beatbox}
	THANKS_PATTERNS={
                re.compile('thanks'):Thanks,
                re.compile('thank you'):Thanks,
                re.compile('thank you so much'):Thanks}
	ANS_PATTERNS = {
                re.compile('who is ansh'):ans}
	HADI_PATTERNS = {
                re.compile('who is hubby'):hadi,
                re.compile('who is hardy'):hadi}
	
	UPDATE_COMMAND = "update"

	while True:
		print("Listening...")
		text = get_audio()
		print(text)
		result = None

		for pattern, func in COUNTRY_PATTERNS.items():
			if pattern.match(text):
				words = set(text.split(" "))
				for country in country_list:
					if country in words:
						result = func(country)
						break

		for pattern, func in TOTAL_PATTERNS.items():
			if pattern.match(text):
				result = func()
				break
		for pattern,func in WEIRD_PATTERNS.items():
			if pattern.match(text):
				speak('Sir Taha the great')
				
				
				break
		
		for pattern,func in GREETING_PATTERNS.items():
			if pattern.match(text):
				speak('Hello my dude, how are you')
				
				
				break
		for pattern,func in FEEL_PATTERNS.items():
			if pattern.match(text):
				speak('Nice')
				
				
				break
		for pattern,func in ROBO_PATTERNS.items():
			if pattern.match(text):
				speak('I am usually called Robo Nigga arounf these parts.')
				
				
				break
		for pattern,func in BEATBOX_PATTERNS.items():
			if pattern.match(text):
				speak('boom chick, boom ba boom chick. pao boom chick ba boom ba boom chik')
				
				
				break
		for pattern,func in THANKS_PATTERNS.items():
			if pattern.match(text):
				speak('Please dont thank me. Thank my master and creator, Taha the great!')
				
				
				break
		for pattern,func in ANS_PATTERNS.items():
			if pattern.match(text):
				speak(' Anas is sir Taha the greats big brother. Anas is a very big fat nigga!')
				
				
				break
		for pattern,func in HADI_PATTERNS.items():
			if pattern.match(text):
				speak(' Hadi is sir Taha the greats little brother. Hadi is naalapooni and a malooni.')
				
				
				break			
		

		if text == UPDATE_COMMAND:
			result = "Data is being updated. This may take a moment!"
			data.update_data()

		if result:
			speak(result)

		if text.find(END_PHRASE) != -1:  
			speak('Ok Boomer')
			break

main()
