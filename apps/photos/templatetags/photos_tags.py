from real_estate_app.apps.models import Photo

class PhotoNode(template.Node):
        def __init__(self, var_name, obj_id=None ,num=None):
                self.var_name=var_name
                self.id = obj_id

                if num:
                        self.num = int(num)
                else:
                        self.num = None


        def render(self, context):
                if self.id:
                        obj = template.resolve_variable(self.id, context)

                if self.id:
                        photo = Photo.objects.published().filter(album=int(obj))
                       
                else:
                        photo = Photo.objects.published()

                context[self.var_name] = photo[:self.num]
                return ''

def do_get_photos(parser, token):

        bits = token.contents.split()
        if len(bits) == 5:
                if bits[1] != 'from':
                        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'from'" % bits[0]
                if bits[3] != 'as':
                        raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]
                return PhotoNode(obj_id=bits[2],var_name=bits[4])
        if len(bits) == 6:
                if bits[2] != 'from':
                        raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'from'" % bits[0]
                if bits[4] != 'as':
                        raise template.TemplateSyntaxError, "Fourth argument to '%s' tag must be 'as'" % bits[0]
                return PhotoNode(num=bits[1], var_name=bits[5], obj_id=bits[3])
        elif len(bits)==3:
                if bits[1]!='as':
                        raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
                return PhotoNode(var_name=bits[2])
        else:
                raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

register.tag('get_photos',do_get_photos)
