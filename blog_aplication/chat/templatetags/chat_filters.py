from django import template

register = template.Library()


@register.filter
def other_user(chat, user):
    if chat.user1 == user:
        return chat.user2.username
    return chat.user1.username