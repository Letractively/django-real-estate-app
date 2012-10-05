# -*- coding: utf-8 -*-
from datetime import datetime
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render_to_response
from django.views.decorators.csrf import requires_csrf_token
from django.http import Http404
from django.conf import settings

from real_estate_app.forms.sendcontent import ContentMailForm
from real_estate_app.conf.settings import REAL_ESTATE_APP_SITE_NAME

@requires_csrf_token 
def send_content(request):
	default_msg = {
		'sent':u'<strong>Enviado com sucesso.</strong>',
		'msg': u'O Sr(a) %s\n \
				 encaminho para você o seguinte conteúdo, para acessar clique no link abaixo:\n\
				 \n \
				 %s\n \
				 \n \
				 Att,\n \
				 Equipe Bontempo Imóveis.',
		'error': u'Ops... houve algum error ao preencher o formulário de contato',
	
	}

	msg_send=''
	error=''
	form = ContentMailForm()
	if request.GET:
		url=request.GET.get('url',False)
		form=ContentMailForm(initial={'url':url})
		if not url:
			raise Http404


	elif request.POST:
		form = ContentMailForm(request.POST)
		
		if form.is_valid():
			name = request.POST.get('name')
			url=request.POST.get('url',False)
			subject = u'%s enviou um conteúdo do sítio %s' %(name,REAL_ESTATE_APP_SITE_NAME)

			from_email = '%s <%s>' %(name,request.POST.get('from_email', ''))
			recipient_list = request.POST.get('to','')
			message = default_msg['msg'] % (name,url)
			recipient_list = recipient_list.split(',')                                     

			if not recipient_list and from_email: 
			    raise Http404
            
			send_mail(subject , message, from_email, recipient_list, fail_silently=False)

			msg_send=default_msg['sent']

			form = ContentMailForm()
		else:
			error=default_msg['error']

	return render_to_response('real_estate_app/sendcontent.html', {
											'send':msg_send,
											'error':error,
		                                    'form': form,
								},
								context_instance=RequestContext(request)
	)
