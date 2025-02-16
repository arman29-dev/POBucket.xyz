from django.db.models import Model
import secrets


def create_pid(product: Model, max_length: int=6):
    pids = list(product.objects.values_list("pid"))
    while True:
        pid = secrets.token_urlsafe(max_length)
        if pids.__contains__(pid): continue
        else: return pid