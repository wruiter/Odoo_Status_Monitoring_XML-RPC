# Odoo Status Monitoring through the xml-rpc interface.
# Will request te current status based in the version, license, expiration, number of users, users and installed apps.
# Can be installed on any system, does not have to be the server itself.
# Fill in the following credentials:

url = ''
db = ''
username = ''
password = ''

import xmlrpc.client
    
common = xmlrpc.client.ServerProxy(url+'/xmlrpc/2/common'.format(url))  
print (common.version())    
print (common.version()['server_version'])

uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

parameters = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
[[['key' , 'in', ['database.uuid', 'database.create_date', 'database.enterprise_code', 'database.expiration_date', 'database.expiration_reason']]]],{'fields':['key', 'value'], 'limit': 50})
for parameter in parameters:
  print (parameter['key'] + ' ' + parameter['value'])

num_of_users = models.execute_kw(db, uid, password,
    'res.users', 'search_count',
    [[['share', '=', False]]])
print(num_of_users)

users = models.execute_kw(db, uid, password, 'res.users', 'search_read',
[[['share', '=', False]]],{'fields':['name'], 'limit': 50})
for user in users:
  print (user['name'])

installed_modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read',
[[['state' , 'in', ['installed', 'to upgrade', 'to remove']], ['application', '=', True]]],{'fields':['name', 'application', 'state'], 'limit': 50})
for module in installed_modules:
  print (module['name'])
