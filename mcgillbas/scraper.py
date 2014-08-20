#!/usr/bin/env python
#
# Copyright (c) 2014 Calem J Bendell <calemjbendell@gmail.com>
# Copyright (c) 2014 Marc-Etienne Brunet <marcetiennebrunet@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from bs4 import BeautifulSoup
import mechanize, json, influxdb, datetime, time

globals().update(json.load(open("config.json")))


def login(url, username, password):
	br = mechanize.Browser()
	br.open(url)
	br.select_form(name = "LoginForm")
	br["dbUser"] = username
	br["dbPass"] = password
	br.submit()
	return br


def scrape_data(url, username, password, search_name, attributes, sensor_pairlist, samples_limit = None, sleep_time = 3, secondary_sleep_time = 30):
	browser = login(url, username, password)
	if(verbose):
		print(browser)
	if(write_to_local):
		output = open(("dataset--" + '{0:%Y-%m-%d %Hh %Mm}'.format(datetime.datetime.now())) + ".csv", "w")
		output.write("time, sensor, deviceid, value\n")
	samples = 0
	while 1:
		for sensor_pair in sensor_pairlist:
			output.write(",".join([sensor_pair[0], sensor_pair[1], get_current_value(browser, url, url_addons[sensor_pair[2]], sensor_pair)]) + "\n")
			time.sleep(sleep_time)
		samples += 1
		if(samples_limit not None):
			if(samples > samples_limit):
				break
		time.sleep(secondary_sleep_time)


def get_current_value(browser, base_url, url_addon, sensor_pair):
	sensor_url = base_url + url_addon.format(sensor_pair[1])
	if(verbose):
		print("Visiting " + sensor_url)
	html_file = browser.open(sensor_url).read()
	sash_height = "NaN"
	sash_height = BeautifulSoup(html_file).find_all(name = search_name, attrs = {"name": "NewValue"})[0].get("value")

	if(verbose):
		print("Retreived " + sash_height)
	return sash_height



scrape_data(url, username, password, search_name, attributes, sensor_pairlist)
