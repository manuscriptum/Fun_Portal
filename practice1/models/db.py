# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

db.define_table(
    auth.settings.table_user_name,
    Field('first_name',length='128',default='',requires=[IS_NOT_EMPTY()]),
    Field('last_name',length='128',default='',requires=[IS_NOT_EMPTY()]),
    Field('username', requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC()]),
    Field('email', unique=True,requires=[IS_NOT_EMPTY(),IS_EMAIL()],default="xyz@abc.com"),
    Field('date_of_birth','date',requires=IS_DATE(error_message='must be YYYY-MM-DD!')),
    Field('password','password',readable=False,label='Password',requires=IS_NOT_EMPTY()),
    Field('image','upload',readable=False,requires=[IS_IMAGE(),IS_NOT_EMPTY()]),
    Field('gender',default='Male',requires=IS_IN_SET(['Male','Female'])),
    Field('registration_key', length=512, writable=False, readable=False, default=''),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default='')
    )

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=5, special=0, upper=0), CRYPT()]
custom_auth_table.email.requires = [
IS_EMAIL(error_message=auth.messages.invalid_email),
IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.settings.table_user = custom_auth_table
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.messages.verify_email = 'Click on the link http://' + \
request.env.http_host + \
URL(r=request,c='default',f='user',args=['verify_email']) + \
'/%(key)s to verify your email'
auth.messages.reset_password = 'Click on the link http://' + \
request.env.http_host + \
URL(r=request,c='default',f='user',args=['reset_password']) + \
'/%(key)s to reset your password'

auth.define_tables(username=True, signature=False)
auth_table = auth.settings.table_user
auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587' or 'logging' 
mail.settings.sender = 'registerkbc@gmail.com'
mail.settings.login = 'registerkbc:registerquiz'


## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

db.define_table('usage_statistics',
    Field('time_stamp','datetime', default=request.now),
    Field('client_ip','string', default=request.client),
    Field('user_id', 'reference auth_user', default=auth.user and auth.user.id),
    Field('request_controller','string', default=request.controller),
    Field('request_function','string', default=request.function),
    Field('request_extension','string', default=request.extension),
    Field('request_ajax','string', default=request.ajax),
    Field('request_args','string', default=request.args),
    Field('request_vars','string', default=request.vars),
    Field('request_view','string', default=request.view),
    Field('request_http_user_agent','string', default=request.env.http_user_agent),
    Field('request_language','string', default=request.env.http_accept_language),
    Field('description', 'text'),
    migrate=False
    )



#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
db.define_table('Football',
               Field('Serial','integer'),
               Field('question','string'),
               Field('opt1','string'),
               Field('opt2','string'),
               Field('correctAns','string')
               )

db.define_table('International',
                Field('Serial','integer'),
                Field('question','string'),
                Field('opt1','string'),
                Field('opt2','string'),
                Field('correctAns','string')
                )
if db(db.category.id>0).count() == 0:
    db.category.insert(name='General Knowledge')
    db.category.insert(name='Current Affairs')
    db.category.insert(name='Aptitude')

if db(db.subcategory.id>0).count() == 0:
    db.subcategory.insert(name='Computers & Technology', category_id=1)
    db.subcategory.insert(name='History', category_id=1)
    db.subcategory.insert(name='Geography', category_id=1)
    db.subcategory.insert(name='Literature', category_id=1)
    db.subcategory.insert(name='Sports', category_id=2)
    db.subcategory.insert(name='Politics', category_id=2)
    db.subcategory.insert(name='Science', category_id=3)
    db.subcategory.insert(name='Mathematics', category_id=3)
    db.subcategory.insert(name='Others', category_id=3)
    

#db.define_table('payer',
#       Field('name','string'),
#        Field('married','boolean'),
#        Field('spouse_name','string')
#        )
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)