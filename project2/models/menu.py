# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
  _class="brand",_href="http://www.web2py.com/")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Sharvil Katariya'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
(T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
    (T('General Knowledge Questions'), False,URL('default', 'take_ques1')),
    (T('Sports Questions'), False,URL('default', 'take_ques2')),
    (T('Aptitude Questions'), False,URL('default', 'take_ques3')),
    (SPAN('Quiz', _class='highlighted'), False, 'http://web2py.com'),
    (SPAN('Games', _class='highlighted'), False, 'http://web2py.com'),
    ]

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
