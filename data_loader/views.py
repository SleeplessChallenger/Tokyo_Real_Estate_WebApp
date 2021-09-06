from django.shortcuts import render
from general.models import PropertyClass
from django.contrib import messages


def inject_data(request):
	if request.method == 'POST':
		if not request.user.is_staff or not request.user.is_superuser:
			messages.warning(request, "You don't have rights to make this action")
			return redirect('all_info')
		else:
			# initiate class and do all the stuff
			messages.success(request, 'Data has been injected')
			return redirect('all_info')

	else:
		return render(request, 'data_loader/make_load.html')
