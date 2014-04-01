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

@auth.requires_login()
def hello():
    return dict(message='hello %(first_name)s %(last_name)s' % auth.user)

def take_ques1():
    form = SQLFORM(db.general_ques)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors or passed arguements are invalid'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict()

def take_ques2():
    form = SQLFORM(db.sports)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors or passed arguements are invalid'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict()

def take_ques3():
    form = SQLFORM(db.aptitude)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors or passed arguements are invalid'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict()

def select():
    """
    Display log event into usage_statistics table.
    """
    db.usage_statistics.id.readable = False
    table = SQLFORM.grid(db.usage_statistics, orderby=~db.usage_statistics.time_stamp, ui='jquery-ui', formstyle = 'divs')
    return dict(table=table)