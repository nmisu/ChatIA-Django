from django.urls import path
from .views import (
    landing_view, register_view, index_view, 
    new_chat_view, chat_detail_view, update_chat_title, 
    remove_chat, user_profile_view, support_page,
    export_conversation_json, rate_message,
    compare_models_view,
    toggle_pin_chat, toggle_archive_chat,
    generate_shared_link, shared_chat_view
)

urlpatterns = [
    path('', landing_view, name='landing'),
    path('registro/', register_view, name='register'),
    path('chats/', index_view, name='home'),
    path('new/', new_chat_view, name='create_conversation'),
    path('c/<int:conv_id>/', chat_detail_view, name='conversation_detail'),
    path('edit/<int:conv_id>/', update_chat_title, name='rename_conversation'),
    path('drop/<int:conv_id>/', remove_chat, name='delete_conversation'),
    path('me/', user_profile_view, name='profile'),
    path('info/', support_page, name='help'),
    path('c/<int:conv_id>/json/', export_conversation_json, name='export_conversation_json'),
    path('rate/<int:message_id>/<str:action>/', rate_message, name='rate_message'),
    path('compare/', compare_models_view, name='compare_models'),
    path('pin/<int:conv_id>/', toggle_pin_chat, name='toggle_pin'),
    path('archive/<int:conv_id>/', toggle_archive_chat, name='toggle_archive'),
    path('c/<int:conv_id>/share/', generate_shared_link, name='generate_shared_link'),
    path('share/<uuid:link_id>/', shared_chat_view, name='shared_chat_view'),
]