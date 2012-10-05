# -*- coding: utf-8 -*-
from django.views.decorators.csrf import requires_csrf_token
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib.auth.models import Group, User

from real_estate_app.forms.contact import ContactForm
from real_estate_app.conf.settings import MANAGERS, REAL_ESTATE_APP_SITE_NAME

@requires_csrf_token
def contact(request):

	try:
		for user in User.objects.filter(groups=Group.objects.get(name='Gerente')):
			MANAGERS.append((user.first_name+' '+user.last_name,user.email))
	except Group.DoesNotExist:
		pass

	send=''
	error=''
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			message = request.POST.get('message', '')
			subject ='CONTATO: %s' %  request.POST.get('name','')
			from_email = '%s <%s>' % (request.POST.get('name', ''),
                                      request.POST.get('from_email', ''))

			recipient_list = [mail_tuple[1] for mail_tuple in MANAGERS]

			send_mail(subject , message, from_email, recipient_list, fail_silently=False)
			send='A sua mensagem foi enviada com sucesso. Obrigado pelo contato,<br /> <strong>Equipe %s.</strong>' % REAL_ESTATE_APP_SITE_NAME

			form = ContactForm()
		else:
			error='Ops... houve algum error ao preencher o formulário de contato.'
	else:
		form = ContactForm()

	return render_to_response('real_estate_app/contact.html', {
									'send':send,
									'error':error,
									'form': form
							  },
							  context_instance=RequestContext(request))

