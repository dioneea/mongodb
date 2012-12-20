import pymongo
import urllib2
import urllib
import cookielib
import random
import re
import string
import sys
import getopt
import json


connection = None
db = None
webhost = "localhost:8082"
mongostr = "mongodb://localhost:27017"
db_name = "final7"

# command line arg parsing to make folks happy who want to run at mongolabs or mongohq
# this functions uses global vars to communicate. forgive me.
def arg_parsing(argv):

    global webhost
    global mongostr
    global db_name

    try:
        opts, args = getopt.getopt(argv, "-p:-m:-d:")
    except getopt.GetoptError:
        print "usage validate.py -p webhost -m mongoConnectString -d databaseName"
        print "\twebhost defaults to {0}".format(webhost)
        print "\tmongoConnectionString default to {0}".format(mongostr)
        print "\tdatabaseName defaults to {0}".format(db_name)
        sys.exit(2)
    for opt, arg in opts:
        if (opt == '-h'):
            print "usage validate.py -p webhost -m mongoConnectString -d databaseName"
            sys.exit(2)
        elif opt in ("-p"):
            webhost = arg
            print "Overriding HTTP host to be ", webhost
        elif opt in ("-m"):
            mongostr = arg
            print "Overriding MongoDB connection string to be ", mongostr
        elif opt in ("-d"):
            db_name = arg
            print "Overriding MongoDB database to be ", db_name
            
# main section of the code
def main(argv):
	arg_parsing(argv)
	global connection
	global db
	global found
	print "Question 7"
	connection = pymongo.Connection(mongostr, safe=True)
	db = connection[db_name]
	images = db.images
	img = images.find()

	inAlbum = db.albums.aggregate([{'$unwind':'$images'},{'$group':{'_id':'$images'}}])
	for i in img:

		id =  i['_id']		
		found = None
		for j in range(len(inAlbum['result'])) :
			if (inAlbum['result'][j]['_id'] == id):
				#print "same"
				found = 1
		
		if (found==None):
			print id
			images.remove({'_id':id})
					
	print "question 7 end !"
	
if __name__ == "__main__":
    main(sys.argv[1:])