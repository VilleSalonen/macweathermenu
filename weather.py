#!/usr/bin/env python
# encoding: utf-8

import urllib2
import re


class ParseException(Exception):
  def __init__(self, value):
     self.parameter = value

  def __str__(self):
     return repr(self.parameter)


class WeatherStatus(object):
  WEATHER_URL = "http://weather.jyu.fi/"

  temperature = 0.0
  wind_chill = 0.0

  page = None


  def __init__(self):
    self.update()


  def update(self):
    self.temperature = self._get_value_with_regexp("<td style=\"font-size:20px; strong;\">([-]?[0-9]+\.[0-9]+) \&\#176;C")
    self.wind_chill = self._get_value_with_regexp("<td >([-]?[0-9]+\.[0-9]+) \&\#176;C")


  def _get_value_with_regexp(self, r_str):
    self._cache_page()
    r = re.compile(r_str)
    match = r.search(self.page)

    if not match:
        raise ParseException("Cannot parse value from %s" % self.WEATHER_URL)

    return float(match.group(1))


  def _cache_page(self):
    url_o = urllib2.urlopen(self.WEATHER_URL, data=None, timeout=10)
    self.page = url_o.read()


  def __unicode__(self):
    return u'Temp: %.1f°C / Chill: %.1f°C ' % (self.temperature, self.wind_chill)


if __name__ == '__main__':
  weather_status = WeatherStatus()
  print weather_status
