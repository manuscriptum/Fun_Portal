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

def memorygame():
  return dict();

def dodgeball():
  return dict();
  
def subcategory():
   var = db(db.subcategory.category_id == session.cat).select()
   d = {}
   count = 1
   for i in var:
     d[count] = i.name
  #   d["serial"] = i.Serial
     count += 100
   d["len"] = count - 1
   print d
   import json
   s = json.dumps(d)
   return s

def game():
  return dict() 

def quizTopic():
 #  redirect(URL("quiz"))
   var = db().select(db.category.ALL)
   session.counter = 1
   session.ansDict = {}
#   redirect(URL("quiz2"))
   return dict(var=var)
   
#   if session.topic is not None:
#    session.topic = request.vars.topic
#    redirect(URL("quiz"))
#  return dict()     

def Tempquiz():
#   try:
    session.topic = request.vars.topic
#    print request.vars.topic
#    if session.topic is not None:
#         print 'hello'
#    quiz2()
#         session.topic = request.vars.topic
 #        redirect(URL("quiz"))       


def quiz():
#   session.ansDict = {}
#   session.topic = request.vars.topic
#   session.flash = "Select an Option" 
#   if session.topic == 'Football':
#        var=db(db.Football.Serial == 1).select()
       # return dict(var=var)
#   if session.topic == 'International':
#        var = db(db.International.Serial == 1).select()
#   var1 = request.vars.option
#   session.counter = 1
#   return dict(var = var)
#   print session.cat
#   print type(session.cat)
   session.cat = int(session.cat)
   session.subCatNumber = (session.cat)*100 + 1
   session.quesNo = (session.subCatNumber)*100+1
   session.first = session.quesNo
#   print subCatNumber
   session.counter = session.quesNo
   var = db(db.questions.RollNo == session.quesNo).select()
   #for i in var:
    #    print i.opt1 

   return dict(var = var)


def nextQuestion():
   session.counter+=1
#   if session.topic == 'Football':
   var = db(db.questions.RollNo == session.counter).select()
#   if session.topic == 'International':
#       var2 = db(db.International.Serial == session.counter).select()
   d={}
   for i in var:
        d["serial"]=i.RollNo
        d["question"]=i.question
        d["opt1"]=i.opt1
        d["opt2"]=i.opt2
        d["opt3"]=i.opt3
        d["opt4"]=i.opt4

   import json
   s = json.dumps(d)
   print d
   nextFlash()
   return s         

def nextFlash():
   try:
      numb = session.quesNo
      numb = int(numb)
      numb = numb + 1
      numb = str(numb)
      print session.ansDict
  #    print 'nextCalled'
      session.flash = "You had selected " + session.ansDict[numb]
   except:
      session.flash = "Select an option"
def prevFlash():
   try:
       numb = session.quesNo
       numb = int(numb)
       numb = numb - 1
       numb = str(numb)
   #    print numb
       print session.ansDict
   #    print 'prevCalled'
       session.flash = "You had selected " + session.ansDict[numb]
   except:
       session.flash = "Select an option"


def prevQuestion():
   if session.counter == session.first:
        return dict()
   session.counter-=1
#   if session.topic == 'Football':
   var = db(db.questions.RollNo == session.counter).select()
#   if session.topic == 'International':
#        var2 = db(db.International.Serial == session.counter).select()
   d={}
   for i in var:
        d["serial"]=i.RollNo
        d["question"]=i.question
        d["opt1"]=i.opt1
        d["opt2"]=i.opt2
        d["opt3"]=i.opt3
        d["opt4"]=i.opt4
   import json
   s = json.dumps(d)
   prevFlash()
   return s
         

def selectedOption():
    numb = session.quesNo
    if session.ansDict is None:
       session.ansDict = {}
    session.ansDict[numb] = request.vars.value
    print session.ansDict
    response.flash = "You selected " + request.vars.value
    
def tempSave():
    session.quesNo = request.vars.SerialNumber

def quizDone():
    return dict()

def cats():
   session.cat = request.vars.val
#   print session.cat

