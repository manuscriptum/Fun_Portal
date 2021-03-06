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
    return dict()

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

def all_records():
    grid = SQLFORM.grid(db.questions)
    return locals()

def retrieve():
    redirect(URL('user/retrieve_password'))

def subcategory():
   var = db(db.subcategory.category_id == session.cat).select()
   d = {}
   count = 1
   for i in var:
     d[count] = i.name
     count += 1
   d["len"] = count - 1
   import json
   s = json.dumps(d)
   return s

@auth.requires_login()
def quizTopic():
   session.correctNo = 0
   session.wrongNo = 0
   session.score = 0
   session.notAttempted = 0
   session.flag = 0
   var = db().select(db.category.ALL)
   session.counter = 1
   session.ansDict = {}
   return dict(var=var)
   
def Tempquiz():
  session.topic = request.vars.topic

@auth.requires_membership('creators')
def manage():
  grid=SQLFORM.smartgrid(db.questions)
  return dict(grid=grid)

mp3_file=URL(r=request,c='static',f='test.mp3')
wav_file=URL(r=request,c='static',f='test.wav')

def test_embed():
  embed_mp3=XML('<embed src="%s" autoplay="false" loop="false" />' % mp3_file)
  embed_wav=XML('<embed src="%s" autoplay="true" loop="true" />' % wav_file)
  return dict(wav=embed_wav,mp3=embed_mp3)

@auth.requires_login()
def quiz():
   session.cat = int(session.cat)
   session.topic=int(session.topic)
   session.subCatNumber = (session.cat)*100 + session.topic
   session.quesNo = (session.subCatNumber)*100+1
   session.first = session.quesNo
   session.last = session.first + 3
   session.counter = session.quesNo
   var = db(db.questions.RollNo == session.quesNo).select()
   return dict(var = var)


def nextQuestion():
   if session.counter == session.last:
        return dict()
   session.counter+=1
   var = db(db.questions.RollNo == session.counter).select()
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
   nextFlash()
   return s         

def nextFlash():
   try:
      numb = session.quesNo
      numb = int(numb)
      numb = numb + 1
      print session.ansDict
      session.flash = "You had selected " + session.ansDict[numb]
   except:
      session.flash = "Select an option"

def prevFlash():
   try:
       numb = session.quesNo
       numb = int(numb)
       numb = numb - 1
       print session.ansDict
       session.flash = "You had selected " + session.ansDict[numb]
   except:
       session.flash = "Select an option"

def prevQuestion():
   if session.counter == session.first:
        return dict()
   session.counter-=1
   var = db(db.questions.RollNo == session.counter).select()
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
    numb = int(session.quesNo)
    if session.ansDict is None:
       session.ansDict = {}
    session.ansDict[numb] = request.vars.value
    print session.ansDict
    response.flash = "You selected " + request.vars.value
    
def tempSave():
    session.quesNo = request.vars.SerialNumber

@auth.requires_login()
def quizDone():
   if session.flag == 0:
     var = db(db.questions.subcategory == session.subCatNumber).select()
     for i in var:
       var1 = int(i.RollNo)
       if session.ansDict.has_key(var1):
         print session.ansDict
         print var1
         if i.answer == session.ansDict[var1]:
           session.correctNo += 1
           session.score += 3
         elif i.answer != session.ansDict[var1]:
           session.wrongNo += 1
           session.score -=1
         else:
           pass
       else:
         pass 
     session.notAttempted = 4 - len(session.ansDict)
     db.userScore.bulk_insert([{'Correctans':session.correctNo,'Wrongans':session.wrongNo,'Notattempted':session.notAttempted,'Score':session.score}])
     session.flag = 1
   else:
     pass  

   return dict(correct=session.correctNo,wrong=session.wrongNo,unattempted=session.notAttempted,score=session.score)

def memorygame():
  return dict()

def dodgeball():
  return dict()
  
def game():
  return dict()

@auth.requires_login()
def stats():
  form,results = dynamic_search(db.userScore)
  table=db(db.userScore.userid==auth.user.id).select(db.userScore.Correctans,db.userScore.Wrongans,db.userScore.Notattempted,db.userScore.Score)
  rows=db(db.userScore.userid==auth.user.id).select()
  correct=0;
  wrong=0
  avg_score=0
  unattempted=0
  length=len(rows)
  scores=[]
  
  for row in rows:
    correct+=row.Correctans
    wrong+=row.Wrongans
    avg_score+=row.Score
    unattempted+=row.Notattempted
    scores.append(int(row.Score))
  
  if length!=0:
    correct=float(correct)/length
    wrong=float(wrong)/length
    avg_score=float(avg_score)/length
    unattempted=float(unattempted)/length

  correct=round(correct,2)
  wrong=round(wrong,2)
  avg_score=round(avg_score,2)
  unattempted=round(unattempted,2)

  labels=[]
  tool=[]
  for i in range(length):
    labels.append("quiz_"+str(i+1))
    tool.append(str(labels[i])+ ":" + str(scores[i]))
  return dict(form=form,results=results,table=table,tool=tool,scores=scores,labels=labels,correct=correct,wrong=wrong,avg_score=avg_score,unattempted=unattempted)

def cats():
   session.cat = request.vars.val

@auth.requires_login()
def build_query(field, op, value):
    if op == 'equals':
        return field == value
    elif op == 'not equal':
        return field != value
    elif op == 'greater than':
        return field > value
    elif op == 'less than':
        return field < value
    elif op == 'starts with':
        return field.like(value+'%')
    elif op == 'ends with':
        return field.like('%'+value)
    elif op == 'contains':
        return field.like('%'+value+'%')

@auth.requires_login()
def dynamic_search(table):
    tbl = TABLE()
    selected = []
    ops = ['equals','not equal','greater than','less than',
           'starts with','ends with','contains']
    query = table.id > 0    
    for field in table.fields:
        if (field=='id' or field=='userid'):
          pass
        else:
          chkval = request.vars.get('chk'+field,None)
          txtval = request.vars.get('txt'+field,None)
          opval = request.vars.get('op'+field,None)
          row = TR(TD(INPUT(_type="checkbox",_name="chk"+field,
                          value=chkval=='on')),
            TD(field),TD(SELECT(ops,_name="op"+field,
                                     value=opval)),
            TD(INPUT(_type="text",_name="txt"+field,
                          _value=txtval)))
          tbl.append(row)
          if chkval:
            if txtval:
              query &= build_query(table[field], 
                                opval,txtval)
          selected.append(table[field])           
    form = FORM(tbl,INPUT(_type="submit"))
    if auth.user:
      results = db(query&(db.userScore.userid==auth.user.id)).select(*selected)
    return form, results

@auth.requires_login()
def search():
    form,results = dynamic_search(db.userScore)
    return dict(form=form,results=results)
