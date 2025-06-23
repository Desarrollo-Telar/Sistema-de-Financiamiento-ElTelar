from rest_framework.authtoken.models import Token

# MODELO USER
from apps.users.models import User

def generar_tokens():
    for user in User.objects.all():
        Token.objects.create(user=user)


if __name__ == '__main__':
    generar_tokens()