from django.http import JsonResponse
from django.views import View
from django.shortcuts import  render,HttpResponse, get_object_or_404

from ..forms.PhotosForm import PhotoForm
from ..models import Photo
import pdb

class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def DeletePhoto(request, id):
    """ Delete service """
    photo_instance = get_object_or_404(Photo, pk=int(id))
    photo_instance.delete()
    return HttpResponse(status=204)
