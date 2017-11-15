from django.shortcuts import  render_to_response
from appointmentscheduler.models import  * 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def updateGeneral(request):
	options=AppschedulerOptions.objects.all();
	template_name="updateGeneral"
	return render_to_response(template_name, {'General': options})
