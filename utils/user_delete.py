# utils/user_delete.py
from django.db import transaction
from django.db.utils import IntegrityError
from recipes.models import Recipe

def safe_delete_user(user):
    if user.is_superuser:
        return {"success": False, "message": "Não é possível excluir um superusuário.", "blocking": []}
    try:
        with transaction.atomic():
            # Atualiza receitas para não referenciar o usuário
            Recipe.objects.filter(author=user).update(author=None)
            user.user_permissions.clear()
            user.groups.clear()
            if hasattr(user, 'logentry_set'):
                user.logentry_set.all().delete()
            user.delete()
        return {"success": True, "message": "Usuário excluído com sucesso!", "blocking": []}
    except IntegrityError as e:
        return {"success": False, "message": f"Erro de integridade: {str(e)}", "blocking": []}
    except Exception as e:
        return {"success": False, "message": f"Erro ao excluir: {str(e)}", "blocking": []}