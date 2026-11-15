# Back-end-Development-Capstone

Django application for the Djirection band, integrating the Pictures and Songs Flask services.

## Run

```sh
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata concerts
python manage.py runserver 127.0.0.1:8000
```

Start Pictures on port 8081 and Songs on port 8082. Override PICTURES_API_URL and SONGS_API_URL for other hosts.

Pages: Home, Songs with Lyrics modals, Photos, signup/login/logout, authenticated Concerts and attendance updates, and Django Admin login. Create an administrator separately with `python manage.py createsuperuser` if needed.

For deployment, provide DJANGO_SECRET_KEY, DJANGO_DEBUG=0, DJANGO_ALLOWED_HOSTS, DJANGO_CSRF_TRUSTED_ORIGINS and the service URLs. The Docker image serves port 8000. Configure the registry image and django-settings Secret before applying deployment.yml. Cloud deployment has not yet been verified.

Migrations, Django system checks and local service integration checks pass. Original course instructions are retained in LAB.md. Based on the IBM course starter; see LICENSE.
