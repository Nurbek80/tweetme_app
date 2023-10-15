-> django-admin start project <projectName> -  create django Project
-> python manage.py runserver
-> python manage.py startapp <appName>
-> python manage.py makemigrations
-> python manage.py migrate

-----------------------------------
 
REST API VIEW
    This views can be consumed by JavaScript/Swift/Java/ (iOS/Andriod)
    returns JSON Data

------------
Java Script appending to InnerHTML

var ele1 = "<h1>HI</h1>"
var ele2 = "<h1>HI</h1>"

const tweetsElement = document.getElementById("tweets")
tweetsElement.innerHTML =ele1+ele2
-----------


pip install django-cors-headers - to get rid of DJANGO - REACT Connection
https://pypi.org/project/django-cors-headers/

To run django with react run 
npm run build
Go to settins and add configs
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]

place static file from react build into django
and also index.html
    path('react/', TemplateView.as_view(template_name='react.html')),

Then run command python manage.py collectstatic
