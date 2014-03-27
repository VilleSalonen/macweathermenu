import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

import weather
import datetime


start_time = NSDate.date()

class Timer(NSObject):
  statusbar = None
  state = 'idle'
  weather = weather.WeatherStatus()


  def applicationDidFinishLaunching_(self, notification):
    statusbar = NSStatusBar.systemStatusBar()
    # Create the statusbar item
    self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    self.statusitem.setTitle_('Starting...')
    # Let it highlight upon clicking
    self.statusitem.setHighlightMode_(1)

    # Build a very simple menu
    self.menu = NSMenu.alloc().init()
    # Default event
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Update', 'tick:', '')
    self.menu.addItem_(menuitem)
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(menuitem)
    # Bind it to the status item
    self.statusitem.setMenu_(self.menu)

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 300.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)


  def tick_(self, notification):
    self.weather.update()
    text = unicode(self.weather) #+ ' ' + str(datetime.datetime.now())
    self.statusitem.setTitle_(text)


if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
