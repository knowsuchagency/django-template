from ninja import Router
from ninja.responses import Response
from django.contrib.auth import get_user_model

router = Router()
User = get_user_model()