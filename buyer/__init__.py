from django.db.models import Model



# function to authenticate user
def authenticate(model=Model, **credentials) -> bool:
    if model.password == credentials.get('password'): return True
    else: return False