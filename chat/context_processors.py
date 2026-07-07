from .models import Conversation, Message

def global_metrics(request):
    """
    Calcula las métricas globales para pasarlas al pie de página en todas las vistas.
    """
    # Métricas públicas (totales de la app)
    metrics = {
        'total_convs': Conversation.objects.count(),
        'total_msgs': Message.objects.count(),
        'user_convs': 0,
        'user_msgs': 0,
    }
    
    # Si el usuario tiene sesión iniciada, calculamos las suyas propias
    if request.user.is_authenticated:
        metrics['user_convs'] = Conversation.objects.filter(user=request.user).count()
        # Filtramos los mensajes que pertenecen a las conversaciones de este usuario
        metrics['user_msgs'] = Message.objects.filter(conversation__user=request.user).count()
        
    return metrics