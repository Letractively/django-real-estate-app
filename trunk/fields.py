# -*- coding: utf-8; -*-                                       
import re                                                      
                                                               
from django.core.validators import email_re                    
from django.forms import CharField, Textarea, ValidationError  
from django.utils.translation import ugettext as _             

email_separator_re = re.compile(r'[^\w\.\-\+@_]+')             
                                                               
def _is_valid_email(email):                                    
    return email_re.match(email)                               
                                                               
class EmailsListField(CharField):                                                    
                                                                                     
    widget = Textarea                                                                
                                                                                     
    def clean(self, value):                                                          
        super(EmailsListField, self).clean(value)                                    
                                                                                     
        emails = email_separator_re.split(value)                                     
                                                                                     
        if not emails:                                                               
            raise ValidationError(_(u'Enter at least one e-mail address.'))          
                                                                                     
        for email in emails:                                                         
            if not _is_valid_email(email):                                           
                raise ValidationError(_('%s is not a valid e-mail address.') % email)
                                                                                     
        return emails                                                                

