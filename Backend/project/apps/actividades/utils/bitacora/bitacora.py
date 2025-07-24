# logging_utils.py
from apps.actividades.models import SystemLog, LogLevel, LogCategory

def log_system_event(message, level_name="INFO", source="Sistema", category_name="General", traceback=None, metadata=None):
    """
    Registra un evento en la bitácora del sistema
    """
    level, _ = LogLevel.objects.get_or_create(
        name=level_name.upper(),
        defaults={
            'description': f'Nivel {level_name}',
            'priority': {
                'DEBUG': 1,
                'INFO': 2,
                'WARNING': 3,
                'ERROR': 4,
                'CRITICAL': 5
            }.get(level_name.upper(), 2)
        }
    )
    
    category, _ = LogCategory.objects.get_or_create(
        name=category_name,
        defaults={'description': f'Eventos de {category_name}'}
    )
    
    SystemLog.objects.create(
        level=level,
        source=source,
        message=message,
        category=category,
        traceback=traceback,
        metadata=metadata or {}
    )

def log_user_action(user, action, details, request=None, category_name="General", metadata=None):
    """
    Registra una acción de usuario manualmente
    """
    from apps.actividades.models import UserLog, LogCategory
    
    ip = None
    user_agent = None
    
    if request:
        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
    
    category, _ = LogCategory.objects.get_or_create(
        name=category_name,
        defaults={'description': f'Acciones de usuario en {category_name}'}
    )
    
    UserLog.objects.create(
        user=user,
        action=action,
        details=details,
        ip_address=ip,
        user_agent=user_agent,
        category=category,
        metadata=metadata or {}
    )