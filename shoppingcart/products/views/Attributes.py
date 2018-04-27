from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404 , HttpResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import Http404
import pdb, json, operator,re
from ..forms.ProductsForm import ProductsForm
from ..models import Products, Categories, Attributes
from .Catagories import _catagories_datastructure
from ..forms.AttributesForm import AttributesForm

@requires_csrf_token
def attributes(request, id):
    if request.POST:
        pdb.set_trace()
        formparams = request.POST.dict()
        fieldsname = list(request.POST.keys())
        request.POST._mutable = True
        request.POST.clear()
        pattern = "attr_name_"
        attr_names = _getfieldsname(fieldsname, pattern)
        pd = get_object_or_404(Products, id = id)
        for attr_name in attr_names:
            fldname = attr_name + "_value_"
            print(attr_name)
            request.POST['attr_name'] = formparams[attr_name]
            for fieldname in  _getfieldsname(fieldsname, fldname):
                request.POST['attr_value'] = formparams[fieldname]
                attributesform = AttributesForm(request.POST or None)
                if attributesform.is_valid():
                    attributesobj = attributesform.save(commit=False)
                    attributesobj.attributes_product = pd
                    attributesobj.save()
    attributes = Attributes.objects.filter( attributes_product__id = id ).order_by('id', 'attr_name')
    attrs = []
    for attribute in attributes :
        attr = dict()
        attr['attr_name'] = attribute.attr_name
        attr['attr_value'] = attribute.attr_value
        attr['attr_id'] = attribute.id
        attrs.append( attr )
    attrsdetails = _attrsdetails( attrs )
    attributes_cnt = len(attrsdetails)
    if not attributes_cnt :
        attributes_cnt = 0
    templatename = "Attributes.html"
    return render(request, templatename , {"productid" : id, "attrsdetails" : attrsdetails, "attributes_cnt" : attributes_cnt } )


def _getfieldsname(fieldsname, pattern):
    attr_names = []
    flag = 0
    fieldindex = 0
    while fieldindex < len(fieldsname):

        fieldname = fieldsname[fieldindex]

        if fieldname == 'csrfmiddlewaretoken':
            fieldsname.remove(fieldname)
            continue

        my_regex = re.escape(pattern) + r"\d+$"

        m = re.search(my_regex, fieldname)

        # if the string ends in digits m will be a Match object, or None otherwise.
        if m is not None:
            fieldname = m.group()
            attr_names.append(fieldname)
            fieldsname.remove(fieldname)
        else:
            fieldindex += 1
    return attr_names

def _attrsdetails( attrs ):
    cnt = 0

    attr_datas = list()
    attr_data = dict()
    attr_values = list()
    attr_name_cnt = 1

    attr_new_name = None
    flag = 0

    while cnt < len(attrs):

        attr_id = attrs[cnt]['attr_id']
        attr_name = attrs[cnt]['attr_name']
        attr_value = attrs[cnt]['attr_value']

        if (cnt + 1) < len(attrs):
            attr_new_name = attrs[cnt + 1]['attr_name']

        if attr_name != attr_new_name:  # value and next value not same  f 1
            flag = 1

        attr_values.append(attr_value)

        if flag or (cnt == len(attrs) - 1):
            attr_data = dict()
            attr_data['attr_name_cnt'] = attr_name_cnt
            attr_data['attr_id'] = attr_id
            attr_data['attr_value_cnt'] = len(attr_values)
            attr_data['attr_name_value'] = attr_name
            attr_data['attr_values'] = attr_values
            attr_datas.append(attr_data)
            attr_values = []
            attr_name_cnt += 1
            flag = 0

        cnt += 1

    return attr_datas
