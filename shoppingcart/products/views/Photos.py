from django.http import JsonResponse
from django.views import View
from django.shortcuts import  render,HttpResponse, get_object_or_404

from ..forms.PhotosForm import PhotoForm
from ..models import Photo, Products
import pdb

class BasicUploadView(View):
    def get(self, request, id):
        photos_list = Photo.objects.all()
        contextdata = _imageattributes(photos_list)
        contextdata['photos'] = photos_list
        contextdata['productid'] = id

        return render( self.request, 'photos.html', contextdata )

    def post(self, request,id):
        form = PhotoForm(self.request.POST, self.request.FILES)
        pd = get_object_or_404(Products , id= id)
        if form.is_valid():
            photo = form.save(commit= False)
            photo.photo_product = pd
            photo.save()
            contextdata = _imageattributes()

            contextdata['is_valid'] =  True
            contextdata['name'] = photo.file.name
            contextdata['url'] = photo.file.url
            contextdata['id'] = photo.id
        else:
            contextdata = {'is_valid': False}
        return JsonResponse(contextdata)

def _imageattributes(photos_list=None):
    filesizes = 0
    if photos_list is None:
        photos_list = Photo.objects.all()

    image_count = Photo.objects.count()
    for photo in photos_list:
        filesizes += photo.file.size
    img_attrs = {  "image_count" : image_count, "filesizes" : filesizes }
    return img_attrs

def DeletePhoto(request,productid , id):
    """ Delete service """
    photo_instance = get_object_or_404(Photo, pk=int(id))
    photo_instance.delete()
    contextdata = _imageattributes()

    return JsonResponse(contextdata)
