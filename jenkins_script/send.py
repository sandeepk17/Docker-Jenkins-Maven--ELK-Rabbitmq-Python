import pika
import os
import json
import sys
import urllib
import urllib2
import base64

user = ''
password = ''
jenkinsUrl = "http://192.168.99.100:8080/job/Maven/lastBuild/api/json"


def urlopen(url, data=None):
	'''Open a URL using the urllib2 opener.'''
	request = urllib2.Request(url, data)
	base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n','')
	# request.add_header("Authorization", "Basic %s" % base64string)
	return urllib2.urlopen(request)

def generateQ():
	status = "SUCCESS"
	try:
		jenkinsStream = urlopen(jenkinsUrl)
	except urllib2.HTTPError, e:
		print "URL Error: " + str(e.code)
		print "job name Maven probably wrong"
		status = "Failed"
		return

	try:
		buildStatusJson = json.load( jenkinsStream )
	except:
		print "Failed to parse json"
		status = "Failed"
		return
	if buildStatusJson.has_key( "result" ):
		print "Maven build status: " + buildStatusJson["result"]
		status = buildStatusJson["result"]
	else:
		status = "Failed"
		return

	print (status)

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.99.100'))
	channel = connection.channel()
	channel.queue_declare(queue='Maven')
	message = {
			'BUILD_ID' : buildStatusJson["displayName"],
			'JOB_NAME' : "Maven",
			'STATUS' : status
	}

	channel.basic_publish(exchange='', routing_key='Maven', body=json.dumps(message))

	connection.close()

generateQ()