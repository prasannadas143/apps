from appsplatform.settings.base import BASE_DIR, TEMPLATES, USER_APPS,BUILTIN_APPS, INSTALLED_APPS
from os.path import   join


USER_APPS += [
	'shoppingcart.products',
	'shoppingcart.clients',
	'shoppingcart.orders',
	'shoppingcart.dashboard',
	'shoppingcart.vouchers',
	'shoppingcart.report',
	'shoppingcart.options',
	'shoppingcart.options.countries',
	'shoppingcart.options.Backup',

]

INSTALLED_APPS = BUILTIN_APPS + USER_APPS
