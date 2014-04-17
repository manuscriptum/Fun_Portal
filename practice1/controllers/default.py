# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if 'login' in request.args:
        db.auth_user.username.label = T("Username or Email")
        auth.settings.login_userfield = 'username'
        if request.vars.username and not IS_EMAIL()(request.vars.username)[1]:
            auth.settings.login_userfield = 'email'
            request.vars.email = request.vars.username
            request.post_vars.email = request.vars.email
            request.vars.username = None
            request.post_vars.username = None
            return dict(form=auth())
        return dict(form=auth())
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def login():
    redirect(URL('user/login'))

def register():
    redirect(URL('user/register'))
    
@auth.requires_login()
def changepassword():
    redirect(URL('user/change_password'))

@auth.requires_login()
def profile():
    redirect(URL('user/profile'))

'''def all_records():
    grid = SQLFORM.grid(db.auth.settings.table_user_name,user_signature=False)
    return locals()'''

def retrieve():
    redirect(URL('user/retrieve_password'))



def quizTopic():
  session.ansDict = {}
  if request.vars.topic is not None:
    session.topic = request.vars.topic
    redirect(URL("quiz"))
  return dict()     

def quiz():
#   session.ansDict = {}
   session.flash = "Select an Option" 
   if session.topic == 'Football':
        var=db(db.Football.Serial == 1).select()
       # return dict(var=var)
   if session.topic == 'International':
        var = db(db.International.Serial == 1).select()
   var1 = request.vars.option
   session.counter = 1
   return dict(var = var) 

def nextQuestion():
   session.counter+=1
   if session.topic == 'Football':
       var2=db(db.Football.Serial == session.counter).select()
   if session.topic == 'International':
       var2 = db(db.International.Serial == session.counter).select()
   d={}
   for i in var2:
        d["serial"]=i.Serial
        d["question"]=i.question
        d["opt1"]=i.opt1
        d["opt2"]=i.opt2
   
   import json
   s = json.dumps(d)
   nextFlash()
   return s         

def nextFlash():
   try:
      numb = session.num
      numb = int(numb)
      numb = numb + 1
      numb = str(numb)
      session.flash = "You had selected " + session.ansDict[numb]
   except:
      session.flash = "Select an option"
def prevFlash():
   try:
       numb = session.num
       numb = int(numb)
       numb = numb - 1
       numb = str(numb)
       session.flash = "You had selected " + session.ansDict[numb]
   except:
       session.flash = "Select an option"

def prevQuestion():
   if session.counter == 1:
        return dict()
   session.counter-=1
   if session.topic == 'Football':
        var2=db(db.Football.Serial == session.counter).select()
   if session.topic == 'International':
        var2 = db(db.International.Serial == session.counter).select()
   d={}
   for i in var2:
        d["serial"]=i.Serial
        d["question"]=i.question
        d["opt1"]=i.opt1
        d["opt2"]=i.opt2
   import json
   s = json.dumps(d)
   prevFlash()
   return s
         

def selectedOption():
    numb = session.num
    if session.ansDict is None:
       session.ansDict = {}
    session.ansDict[numb] = request.vars.value
    response.flash = "You selected " + request.vars.value
    if session.topic == "Football":
        correctOption

def tempSave():
    session.num = request.vars.SerialNumber

def quizDone():
    return dict()
