from django.db.models import Model
from django.contrib.auth.hashers import check_password


# function to authenticate user
def authenticate(model=Model, **credentials) -> bool:
    if check_password(credentials.get('password'), model.password):
        return True
    else: return False