import pd
import json
import datetime
from datetime import timedelta
import dateutil
from dateutil.parser import parse
import threading
import time
import schedule
from durations import Duration
from random import randint

with open('respondbot_config.json') as f:
	config = json.load(f)

current_incidents = {}

def acknowledge(incident):
	i = pd.request(api_key=incident['domain']['token'], endpoint=f"/incidents/{incident['id']}")
	user_id = i['incident']['assignments'][-1]['assignee']['id']
	u = pd.request(api_key=incident['domain']['token'], endpoint=f"/users/{user_id}")
	user_email = u['user']['email']
	user_name = u['user']['name']
	print(f"  Acknowledge by {user_name} - {user_email} ({user_id})")

	r = pd.request(api_key=incident['domain']['token'], 
		endpoint=f"/incidents/{incident['id']}",
		method="PUT",
		data={"incident": {"type": "incident_reference", "status": "acknowledged"}},
		addheaders={"From": user_email})

	current_incidents[incident['id']]['status'] = "acknowledged"
	del current_incidents[incident['id']]['should_ack']


def resolve(incident):
	i = pd.request(api_key=incident['domain']['token'], endpoint=f"/incidents/{incident['id']}")
	user_id = i['incident']['assignments'][-1]['assignee']['id']
	u = pd.request(api_key=incident['domain']['token'], endpoint=f"/users/{user_id}")
	user_email = u['user']['email']
	user_name = u['user']['name']
	print(f"  Resolve by {user_name} - {user_email} ({user_id})")

	r = pd.request(api_key=incident['domain']['token'], 
		endpoint=f"/incidents/{incident['id']}",
		method="PUT",
		data={"incident": {"type": "incident_reference", "status": "resolved"}},
		addheaders={"From": user_email})

	del current_incidents[incident['id']]


def find_incidents_job():
	for domain in config['domains']:
		incidents = [i for i in pd.fetch_incidents(api_key=domain['token']) if i['service']['id'] in domain['services']]
		for incident in incidents:
			created = parse(incident['created_at'])
			service = incident['service']['id']

			if not incident['id'] in current_incidents:
				current_incidents[incident['id']] = {
					"id": incident['id'],
					"status": incident['status'],
					"summary": incident['summary'],
					"domain": domain
				}

			if incident['status'] == "triggered":
				if 'should_resolve' in current_incidents[incident['id']]:
					del current_incidents[incident['id']]['should_resolve']
				if not 'should_ack' in current_incidents[incident['id']]:
					print(f"Found triggered incident {incident['summary']} ({incident['id']}), created at {created}")
					min_ack_duration = Duration(domain['services'][service]['ack']['min'])
					max_ack_duration = Duration(domain['services'][service]['ack']['max'])
					ack_seconds = randint(min_ack_duration.to_seconds(), max_ack_duration.to_seconds())
					current_incidents[incident['id']]['should_ack'] = created + timedelta(seconds=ack_seconds)
					print(f"  Will acknowledge incident {incident['id']} at {current_incidents[incident['id']]['should_ack']}")
			elif incident['status'] == "acknowledged":
				if 'should_ack' in current_incidents[incident['id']]:
					del current_incidents[incident['id']]['should_ack']
				if not 'should_resolve' in current_incidents[incident['id']]:
					print(f"Found acknowledged incident {incident['summary']} ({incident['id']}), created at {created}")
					min_res_duration = Duration(domain['services'][service]['resolve']['min'])
					max_res_duration = Duration(domain['services'][service]['resolve']['max'])
					res_seconds = randint(min_res_duration.to_seconds(), max_res_duration.to_seconds())
					current_incidents[incident['id']]['should_resolve'] = created + timedelta(seconds=res_seconds)
					print(f"  Will resolve incident {incident['id']} at {current_incidents[incident['id']]['should_resolve']}")

		for k, v in dict(current_incidents).items():
			if 'should_ack' in v and v['should_ack'] < datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc()):
				print(f"Should ack incident {v['summary']} ({k})")
				acknowledge(v)
			elif 'should_resolve' in v and v['should_resolve'] < datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc()):
				print(f"Should resolve incident {v['summary']} ({k})")
				resolve(v)

schedule.every(30).seconds.do(find_incidents_job)

while 1:
	schedule.run_pending()
	time.sleep(1)
