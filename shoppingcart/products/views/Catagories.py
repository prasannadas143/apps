from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from ..models import Categories
from ..forms.CatagorieForm import CategoriesForm
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
import pdb, json, operator


@requires_csrf_token
def AddCatagorie(request):
    root_obj = _create_root()
    if request.method == 'POST':
        # update the  request.POST
        catagorie_name = request.POST['catagorie_name']
        parentid = request.POST['parent_id']
        request.POST._mutable = True
        request.POST.clear()
        request.POST['catagorie_name'] = catagorie_name
        request.POST['parent_id'] = parentid
        # Get the node structure  and get the position of child node
        graphs = _catagories_graphs()
        pn = graphs[int(parentid)]
        request.POST['child_position'] = len(pn.child) + 1
        categoriesform = CategoriesForm(request.POST or None)
        if categoriesform.is_valid():
            categoriesformobj = categoriesform.save(commit=False)
            categoriesformobj.save()
            return HttpResponseRedirect('/shoppingcart/products/Catagories/')
    catagories = _catagories_datastructure()
    listcatagories = Categories.objects.all()
    # use the structure to display it on dropdown in addcatagorie
    templatename = "AddCatagorie.html"
    return render(request, templatename, {"data": catagories})


@requires_csrf_token
def catagories(request):
    catagories = _catagories_datastructure()
    data = {"data": catagories}
    templatename = "Catagories.html"
    return render(request, templatename, data)


@requires_csrf_token
def MoveCatagories(request, id):
    if 'uparrow' in request.POST:
        nodeid = int(request.POST['uparrow'])
        uparrow = 1
    else:
        nodeid = int(request.POST['downarrow'])
        uparrow = 0

    categorie = get_object_or_404(Categories, id=nodeid)
    categorie_parent_id = categorie.parent_id
    categorie_position = categorie.child_position
    if uparrow:
        new_arrow_position = categorie_position - 1
    else:
        new_arrow_position = categorie_position + 1
    categorie_sibling = get_object_or_404(Categories, parent_id=categorie_parent_id, child_position=new_arrow_position)
    categorie.child_position = new_arrow_position
    categorie_sibling.child_position = categorie_position
    categorie.save()
    categorie_sibling.save()
    return HttpResponseRedirect('/shoppingcart/products/Catagories/')


def _catagories_datastructure():
    root = get_a_root(_catagories_graphs())
    catagories = root.toJSON()
    catagories = json.loads(catagories)
    catagories = catagories["child"][0]
    _sort_catagories_positions(catagories)
    return catagories


def _sort_catagories_positions(catagories):
    childs = catagories['child']
    childs.sort(key=operator.itemgetter('location'))
    for child in childs:
        _sort_catagories_positions(child)


def get_a_root(items):
    """Find a root node from items.

    Grab some node and follow the parent pointers to a root.
    """
    cur_key = list(items.keys())[0]
    while items[cur_key].parent is not None:
        cur_key = items[cur_key].parent.value
    parent = items[cur_key]
    return parent


def _catagories_graphs():
    listcatagories = Categories.objects.values('id', 'parent_id', 'catagorie_name', 'child_position')
    """Map all input graphs into Node(object)'s.           

     Return: A hash table by value: Node(value, child, parent)              
     """
    items = {}
    for catagorie in listcatagories:
        child = catagorie['id']
        parent = catagorie['parent_id']
        catagorie_name = catagorie['catagorie_name']
        child_position = catagorie['child_position']

        c_n = Node(child, catagorie_name, child_position)
        items[child] = c_n

        if not parent in items:
            p_n = Node(parent)
            items[parent] = p_n
        else:
            p_n = items[parent]
        # if c_n has value for "position" field, suppose  "child 1 child 4 child 7"
        # then keep it as 7th element of parent node.
        p_n.set_child(c_n)
        c_n.set_parent(p_n)

    return items


def _create_root():
    try:
        root_obj = Categories.objects.get(id=1)
    except ObjectDoesNotExist:
        # create the root object
        root_obj = Categories.objects.create(id=1, parentid=0, catagorie_name="noparent", child_position=0)
    return root_obj


def _removekey(d, key):
    r = dict(d)
    del r[key]
    return r


class Node(object):
    def __init__(self, value, name=None, location=None):
        self.value = value
        # List of references to Node()'s.
        self.child = []
        # Reference to parent Node()
        self.parent = None
        self.name = name
        self.location = location

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        self.child.append(child)

    def set_position(self):
        pos = None
        if getattr(self, 'parent') is not None:
            self.location = self.parent.child.index(self) + 1
        else:
            self.location = 1
        print(self.location)

    def toJSON(self):
        return json.dumps(self, default=lambda o: _removekey(o.__dict__, 'parent'))
