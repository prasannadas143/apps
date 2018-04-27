from Appsplatform.appsplatform.settings.base import BASE_DIR, TEMPLATES, USER_APPS,BUILTIN_APPS, INSTALLED_APPS
from os.path import   join


TEMPLATES[0]['DIRS'] += [  join(BASE_DIR,"shoppingcart" ),]
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
	'shoppingcart.options.SmsEmailSettings',
	'shoppingcart.options.SmsEmailTemplates',
	'shoppingcart.options.ShippingAndTax',

]

INSTALLED_APPS = BUILTIN_APPS + USER_APPS
