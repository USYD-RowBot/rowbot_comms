import operator
import re
import SocketServer
import threading
import sys

def calcchecksum(nmea_str):
	return reduce(operator.xor, map(ord, nmea_str), 0)
	
	#reads in a NMEA string, check integrity and returns dictionary of elements in message
	#returns a dictionary with keys: talker, sentence type, and a list of the data elements
def readNMEA(nmea_str):
	#create expression to parse NMEA sentence
	NMEApattern = re.compile('''
		^[^$]*\$?
		(?P<nmea_str>
			(?P<talker>\w{2})
			(?P<sentence_type>\w{3}),
			(?P<data>[^*]+)
		)(?:\\*(?P<checksum>[A-F0-9]{2}))
		[\\\r\\\n]*
		''', re.X | re.IGNORECASE)

	#split up NMEA sentence using RE pattern

	match = NMEApattern.match(nmea_str)
	if not match:
		raise ValueError('could not parse data: %r' % nmea_str)

	nmea_dict = {}	
		  
	nmea_str        = match.group('nmea_str')
	nmea_dict['talker']          = match.group('talker').upper()
	nmea_dict['sentence_type']   = match.group('sentence_type').upper()
	nmea_dict['data']            = match.group('data').split(',')
	checksum        = match.group('checksum')
	
	cs1 = int(checksum, 16)
	cs2 = calcchecksum(nmea_str)
	if cs1 != cs2:
		raise ValueError('checksum does not match: %02X != %02X' %
			(cs1, cs2))
				
	#parsed and CS good, return dictionary			
	return nmea_dict
	
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def parseHeartbeat(message):
  print "----------------------------------------------"
  print "Valid Heartbeat"
  print "Team ID: ", message['data'][6]
  print "Vehicle date", message['data'][0], "Vehicle time", message['data'][1], "Vehicle at ", message['data'] [2], message['data'] [3], message['data'] [4],message['data'] [5]
  if message['data'][7] == '1':
    print "Vehicle under RC mode"
  elif message['data'][7] == '2':
    print "Vehicle under Autonomous Mission Mode"
  elif message['data'][7] == '3':
		print "Vehicle is disabled"
  else:
    raise ValueError('Unknown mode reported')
  if message['data'][8] == '1':
    print "ROV is Stowed"
  elif message['data'][8] == '2':
    print "ROV deployed"
  else:
    ValueError('Unknown ROV mode reported')
  print "----------------------------------------------"

  # NOT USED 2018
def parseSearchTask(message):
	print "----------------------------------------------"
	print "Answer to Underwater Search Task given"
	print "Team ID: ", message['data'][5]
	print "Vehicle time", message['data'][0]
	print "Vehicle position ", message['data'] [1], message['data'] [2], message['data'] [3],message['data'] [4]
	print "Bouy number with active pinger: ", message['data'][6]
	
	if message['data'][7]:
		print "Reported pinger depth", message['data'][7]
	else:
		print "No pinger depth reported"
	print "----------------------------------------------"
	
def parseLightTask(message):
  print "----------------------------------------------"
  print "Answer to Light Tower Task given"
  print "Team ID: ", message['data'][2]
  print "Vehicle date", message['data'][0] 
  print "Vehicle time", message['data'][1] 
  print "Reported light sequency from first to last:  ",
  for a in message['data'] [3]:
    if a == 'R':
      print " Red ",
    elif a == 'G':
      print " Green ",
    elif a == 'B':
      print " Blue ",
  print ''
  print "----------------------------------------------"
	
	
class MyTCPHandler(SocketServer.StreamRequestHandler):

	def handle(self):
		
		#loop to keep connection alive
		while True:
	
			# self.rfile is a file-like object created by the handler;
			# we can now use e.g. readline() instead of raw recv() calls
			self.data = self.rfile.readline().strip()
			if self.data == '':
				break
			
			try:
				message = readNMEA(self.data)
				if message['talker'] != 'RX':
					raise ValueError('Invalid Talker, got %r' % message['talker'])
					
				#if you got here, message is good, time to act on it

				if message['sentence_type'] == 'HRB':
					parseHeartbeat(message)
				elif message['sentence_type'] == 'COD':
					parseLightTask(message)
				else: 
					raise ValueError('Invalid Sentence Type, got %r' % message['sentence_type'])
				
				#print "Got a message with talker: ", message['talker']
				#print "Sentence Type: ", message['sentence_type']
				#print "And the following data fields:"

			except ValueError as e:
				print "Error parsing message:" 
				print e
				

if __name__ == "__main__":
	
	#create server
	HOST, PORT = "localhost", 12345
	# Create the server, binding to localhost on port 12345
	#server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
	
	# Start a thread with the server -- that thread will then start one
    # more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	
	# Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()
	print "Server running"
	
	print "Connect to server on port:", PORT
	
	while True:
		command = raw_input("type 'quit' to exit program   ")
	
		if command == 'quit':
			sys.exit()
