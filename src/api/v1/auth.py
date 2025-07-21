from ninja import Router
from ninja.responses import Response
from django.contrib.auth import get_user_model

router = Router()
User = get_user_model()


@router.get("/user")
def get_current_user(request):
    """Get the current authenticated user"""
    if request.user.is_authenticated:
        return {
            "id": request.user.id,
            "email": request.user.email,
            "username": request.user.username,
        }
    return Response({"detail": "Not authenticated"}, status=401)