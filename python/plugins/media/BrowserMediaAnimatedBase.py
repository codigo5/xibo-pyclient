#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Xibo - Digitial Signage - http://www.xibo.org.uk
# Copyright (C) 2009 Alex Harrington
#
# This file is part of Xibo.
#
# Xibo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version. 
#
# Xibo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Xibo.  If not, see <http://www.gnu.org/licenses/>.
#

from BrowserMediaBase import BrowserMediaBase
from threading import Thread
import urllib
import sys, os, time

class BrowserMediaAnimatedBase(BrowserMediaBase):
        
    def injectContent(self):
        """ Returns a string of content to inject in to the page """
        content = ""
        
        items = self.getContent()
        
        for tmpItem in items:
            if self.options['direction'] == 'left' or self.options['direction'] == 'right':
                tmpItem = tmpItem.replace('<p>','')
                tmpItem = tmpItem.replace('</p>','')
                
                tmpItem = "<span class='article' style='padding-left:4px;'>%s</span>" % tmpItem
                tmpItem += "<span style='padding-left:4px;'> - </span>"
            else:
                tmpItem = "<div class='XiboRssItem' style='display:block;padding:4px;width:%d'>%s</div>" % (self.width - 10,tmpItem)
            
            content += tmpItem
        
        textWrap = ""
        
        if self.options['direction'] == 'none':
            pass
        else:
            if self.options['direction'] == 'left' or self.options['direction'] == 'right':
                textWrap = "white-space: nowrap";
                content = "<nobr>%s</nobr>" % content
            else:
                textWrap = "width: %dpx;" % (self.width - 50);
            
            if self.options['direction'] == 'single':
                content = "<div id='text'>%s</div>" % content
            else:
                content = "<div id='text' style='position:relative;overflow:hidden;width:%dpx; height:%dpx;'><div id='innerText' style='position:absolute; left: 0px; top: 0px; %s'>%s</div></div>" % (self.width - 10,self.height, textWrap, content)
                
        return content
    
    def injectScript(self):
        """ Returns a string of script to inject in to the page """
        js = ""
        if self.options['direction'] == "single":
            js = "<script type='text/javascript'>\n\n"
            js += "function init() {\n"
            js += "  var totalDuration = %d * 1000;\n" % int(self.duration)
            js += "  var itemCount = $('.XiboRssItem').size();\n"
            js += "  var itemTime = totalDuration / itemCount;\n"
            js += "  if (itemTime < 2000) itemTime = 2000;\n"
            js += "  // Try to get the itemTime from an element we expect to be in the HTML\n"
            js += "  $('#text').cycle({fx: 'fade', timeout:itemTime});\n"
            js += "  }\n"
            js += "</script>\n\n"
            js += "<style type='text/css'>html {overflow:hidden;}</style>\n\n"
        else:
            js = "<script type='text/javascript'>\n\n"
            js += "function init() {\n"
            js += "  tr = new TextRender('text', 'innerText', '" + self.options['direction'] + "');\n"
            js += "  var timer = 0;\n"
            js += "  timer = setInterval('tr.TimerTick()', " + str(self.options['scrollSpeed']) + ");\n"
            js += "}"
            js += "</script>\n\n"
            js += "<style type='text/css'>html {overflow:hidden;}</style>\n\n"
        return js
    
    def browserOptions(self):
        """ Return a tuple of options for the Browser component. True/False/None. None makes no change to the
        current state. True sets to on, False sets to off. Options order is:
            Transparency,Scrollbars
        """
        return (True,False)
    
    def getContent(self):
        return []
