# Django real estate app for websites #

## NEW ON 1.3.0 ##
  * Set Realtors responsability of Proprety.
  * Show the lasted visited Proprety.
  * Create a Portlet Object to get a easy way to user to create and manage apresentation area.

## What more ##

A quick and complete website for Real Estate, easily to install and configure, here you can:

  * TEMPLATE TAGS dynamically prepared for custom and easily utilization.
  * Easy featured a property.
  * Customize images sizes of property.
  * Customize thumbnails sizes of property
  * Easy a custom search for property.
  * Easy intregation and mark a property in Google Maps.
  * Rapid custumization of fields.


## Configuration ##
This configuration has to been put on "settings.py" file of your project:

  * TEMPLATE CONTEXT PROCESSORS: **This is important for real\_estate\_app functioning, this is used to pass all next settings variables.**

```
    TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    'real_estate_app.context_processors.custom_processor',
    )
```

  * TEMPLATES REAL ESTATE APP:
> For default real\_estate\_app has _**REAL\_APP\_MEDIA\_PREFIX**_ global variable defined to render a necessary media for perfect functioning.
    * Set on server media the media dir location of real\_estate\_app.
> > > Exemple: 'Alias /media-real/ <localization of apps>/real\_estate\_app/media/'
    * Or you can custom this localization of media to server, just set on settings project the val _**REAL\_APP\_MEDIA\_PREFIX**_.
```
      Default: '/media-real/'.
      Exemple: REAL_APP_MEDIA_PREFIX='/real/' 
```

  * CUSTOM SITE NAME
    * Set on settings of project the val _**REAL\_ESTATE\_SITE\_NAME**_
```
      Default: '' 
      Exemple: REAL_ESTATE_SITE_NAME='Test of site name' 
```

  * CUSTOM A MAX PROPETY SHOWING ON LIST OF SEARCH, AND OTHERS:
    * Set on settings of project the val _**PROPERTY\_NUM\_LATEST**_
```
      Default: 25
      Exemple: PROPERTY_NUM_LATEST=10
```

  * CUSTOM A IMAGES SIZE OF DESTAQUE
    * Set on settings of project the val _**REAL\_ESTATE\_IMAGES\_SIZE**_
```
      Default: (626,286)
      Exemple: REAL_ESTATE_IMAGES_SIZE=(900,300)
```

  * GMAPS INTREGATE:
    * Set on settings of project the val _**EASY\_MAPS\_GOOGLE\_KEY**_
```
      Default: None
      Exemple: EASY_MAPS_GOOGLE_KEY = <KEY OF GMAP>
```

  * REAL\_ESTATE\_VIEWED\_PRODUCTS

  * Set on settings of project the val _**REAL\_ESTATE\_VIEWED\_PRODUCTS**_
```
    This is used for get amount of lasted viewed Proprety showed on list.
    Default:4
    Exemple: REAL_ESTATE_VIEWED_PRODUCTS = 10
```

# Some potentials of this app #