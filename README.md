# chewsters

Full-stack restaurant ordering app using
[Django](https://www.djangoproject.com/),
[Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/),
and [HTMX](https://htmx.org/docs).

## Code Location:

Boundary: `/chewapp/boundary/name_of_view.py`
Controller: `/chewapp/boundary/name_of_view.py`
Entity: `/chewapp/models.py`
Test Scripts: `/chewapp/boundary/*_test.py`
Mock Data Script (non-inclusive of photos to make zip smaller) : `/mockdatascript.py`

## Quickstart

To run the code, you'll need:

- Python 3.10 or newer

# Install dependencies

cd chewsters
pip install -r requirements.txt

# Run database migrations

python manage.py migrate

# Create a user account

python manage.py createsuperuser

# Attach the Account object to the Django user account

python manage.py shell

> > > from django.contrib.auth.models import User
> > > from chewapp.models import Account, UserProfile
> > > user = User.objects.get(id=1) # The user you created in the prev. step
> > > profile = UserProfile.objects.get(id=5) # Superuser profile w/ all perms
> > > Account(user=user, profile=profile).save() # Create and save

# Run the server

python manage.py runserver

````

Once the server is running, you should be able to access it by opening
[http://localhost:8000/](http://localhost:8000/) in your browser.

## Testing

Set up tests by ending their file names with `_test.py`.

```bash
# Run tests
python manage.py test -p '*_test.py'
````

## Building the Docker image

```bash
docker build -t chewsters .
```
