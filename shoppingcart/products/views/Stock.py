from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import Http404
import pdb, json, operator, re
from ..forms.StockForm import StockForm
from ..models import Stocks,Products,Photo, Attributes


def deletestock(request, id ):
    stockid  = int( request.POST['stock_id'] )
    stockobj = get_object_or_404(Stocks, id=stockid)
    stockobj.stock_attribute.clear()
    stockobj.delete()
    return HttpResponse(status = 204)

@requires_csrf_token
def InStock(request, id):
    productobj = get_object_or_404(Products, id=id)
    addcombination = 1
    showattributes = 0
    attributes = Attributes.objects.filter(attribute_product=productobj).order_by('attr_name').values()
    listattributes = getattributes(attributes)
    if productobj.is_digital:
        if attributes.exists():
            showattributes = 1
    columnnames = [ attribute['attr_name'] for attribute in listattributes ]
    print(columnnames)
    if request.POST:

        formparams = request.POST.dict()
        fieldsname = list(request.POST.keys())
        request.POST._mutable = True
        request.POST.clear()
        fieldlen = len(fieldsname)
        while fieldlen > 0:
            row_fields = _getfieldsname( fieldsname)
            print( row_fields )
            if row_fields is None :
                continue
            stock_attributes = []
            if isinstance(row_fields, list) and len(row_fields):
                stockid = ""
                for row_field in row_fields:
                    if re.match("qty", row_field):
                        request.POST["qty"] = formparams[row_field]
                    elif re.match("price", row_field):
                        request.POST["price"] = formparams[row_field]
                    elif re.match("img_hd", row_field):
                        imageid = formparams[row_field]
                        photoobj = get_object_or_404(Photo , id = imageid )

                    elif re.match("stock", row_field):
                        stockid = formparams[row_field]
                        stockobj = get_object_or_404(Stocks , id = int(stockid) )
                    else :
                        attribute_related = int( formparams[row_field] )
                        attribute_obj = get_object_or_404(Attributes , id = attribute_related )
                        stock_attributes.append( attribute_obj )
                if stockid:
                    stockform = StockForm(request.POST or None , instance= stockobj )
                else :
                    stockform = StockForm(request.POST or None )
                if stockform.is_valid():
                    so = stockform.save( commit= False)
                    stockid = so.id
                    so.image = photoobj
                    so.stock_product = productobj
                    so.save()
                    stock_attributes_cnt = so.stock_attribute.count()
                    if stock_attributes_cnt:
                        stockobj.stock_attribute.clear()
                    for stock_attribute in stock_attributes:
                        so.stock_attribute.add(stock_attribute)
                fieldlen = len(fieldsname)

    stockobjs = Stocks.objects.filter( stock_product = productobj )

    stockdetails = []

    for stockobj in stockobjs:
        stockdetail = dict()
        stockdetail['id'] =stockobj.id
        stockdetail['qty'] = stockobj.qty
        stockdetail['price'] = str( stockobj.price )
        imageid = stockobj.image.id
        photoobj = get_object_or_404( Photo, id=imageid )
        stockdetail['imagepath'] = photoobj.file.url
        stockdetail['imageid'] = imageid
        stock_attributes = stockobj.stock_attribute.all()
        stock_attribute_details = list()
        for stock_attribute in stock_attributes :
            stock_attribute_detail = dict()
            stock_attribute_id = stock_attribute.id
            stock_attribute_obj = get_object_or_404( Attributes , id=stock_attribute_id )
            stock_attribute_detail['attributeid'] = stock_attribute_id
            stock_attribute_detail['stock_attr_value'] = stock_attribute_obj.attr_value
            stock_attribute_detail['stock_attr_name'] = stock_attribute_obj.attr_name

            stock_attribute_details.append( stock_attribute_detail )
        stockdetail['stock_attribute_details'] = stock_attribute_details
        stockdetails.append( stockdetail )
    templatename = "AddStock.html"
    return render(request, templatename, {"id": id,  "stockdetails" : stockdetails , "showattributes" : showattributes, "attributes" : listattributes})

def getattributes( attributes ):

    attr_old_name = None
    attr_values = []
    attributes_struct = []
    attribute_name = dict()

    for attribute in attributes:
        attr_name = attribute['attr_name']
        if attr_old_name != attr_name:
            if attr_old_name is not None:
                attributes_struct.append(attribute_name)
            attribute_name = dict()
            attribute_name['attr_name'] = attr_name
        attribute_name.setdefault("attrvalues", []).append(
            {'attrid': attribute['id'], 'attr_value': attribute['attr_value']})
        attr_old_name = attr_name

    attributes_struct.append(attribute_name)
    return attributes_struct

def listimages(request , id):
    pd = get_object_or_404( Products , id= id )
    photos_objs = Photo.objects.filter(photo_product = pd)
    photo_list = []
    for photos_obj in photos_objs:
        photo = dict()
        photo['imageid'] = photos_obj.id
        photo['imageurl'] = photos_obj.file.url
        photo_list.append( photo )
    return HttpResponse( json.dumps(photo_list), content_type='application/json' )# verify url request to adstock

# check_stockproperties: -     attribute is available for the product.


# verify the "stock" has any row o r not assiosiated with product.


def _getfieldsname(fieldsname):
    row_fields = []
    flag = 0
    fieldindex = 0
    fieldname = fieldsname[0]
    # Remove it if it is "csrfmiddlewaretoken"
    if fieldname == 'csrfmiddlewaretoken':
        fieldsname.remove(fieldname)
        return None
    my_regex = r"\w+(?P<fieldid>\d+)$"
    m = re.search(my_regex, fieldname)
    if m is not None:
        fieldid = m.group('fieldid')

    fieldindex = 0
    while fieldindex < len(fieldsname):

        fieldname = fieldsname[fieldindex]
        my_regex = r'\w+' + re.escape(fieldid) + r"$"

        m = re.search(my_regex, fieldname)

        if m is not None:
            fieldname = m.group()
            row_fields.append(fieldname)
            fieldsname.remove(fieldname)
        else:
            fieldindex += 1

    fileindex = 0

    return row_fields
