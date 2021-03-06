#! /usr/bin/env python

import sys
import os
import roslib
import rospy

import strands_webserver.page_utils
import strands_webserver.client_utils
import std_srvs.srv 


def trigger_pleading(req):
      print 'please, please help'
      return std_srvs.srv.EmptyResponse()

def party_time(req):
      print 'woo, off I go baby'
      return std_srvs.srv.EmptyResponse()


if __name__ == '__main__':
	rospy.init_node("strands_webserver_demo")
	# The display to publish on, defaulting to all displays
	display_no = rospy.get_param("~display", 0)	
	prefix = rospy.get_param("~prefix", '/strands_webserver')	

	# display a start-up page
	strands_webserver.client_utils.display_url(display_no, 'http://strands-project.eu', prefix)

	# sleep for 5 seconds
	rospy.sleep(5.)

	# tell the webserver where it should look for web files to serve
	http_root = os.path.join(roslib.packages.get_pkg_dir("strands_webserver"), "data")
	strands_webserver.client_utils.set_http_root(http_root, prefix)

	# start with a basic page pretending things are going normally
	strands_webserver.client_utils.display_relative_page(display_no, 'example-page.html', prefix)

	# sleep for 5 seconds
	rospy.sleep(5.)

	# now ask for help
	notice = 'Help me, I am <em>stuck</em>'
	buttons = [('No', 'trigger_pleading'), ('Sure', 'party_time')]
	service_prefix = '/caller_services'
	content = strands_webserver.page_utils.generate_alert_button_page(notice, buttons, service_prefix)	
	strands_webserver.client_utils.display_content(display_no, content, prefix) 
	rospy.Service('/caller_services/trigger_pleading', std_srvs.srv.Empty, trigger_pleading) 
	rospy.Service('/caller_services/party_time', std_srvs.srv.Empty, party_time) 
	rospy.spin()