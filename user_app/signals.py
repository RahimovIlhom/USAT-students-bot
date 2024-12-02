from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from .utils import redis_client


@receiver(post_save, sender=User)
def update_user_in_redis(sender, instance, created, **kwargs):
    """
    User saqlanganda yoki yangilanganda Redis ma'lumotlarini yangilaydi.
    """
    redis_key_status = f"user:{instance.tg_id}:status"
    redis_key_lang = f"user:{instance.tg_id}:chat_lang"
    redis_key_passport = f"user:{instance.tg_id}:passport"

    # Ma'lumotni Redisga yozish
    redis_client.set(redis_key_status, instance.status)
    if instance.chat_lang:
        redis_client.set(redis_key_lang, instance.chat_lang)
    if instance.student:
        redis_client.set(redis_key_passport, instance.student.passport)


@receiver(post_delete, sender=User)
def delete_user_from_redis(sender, instance, **kwargs):
    """
    User o'chirilganda Redisdan ma'lumotlarini olib tashlaydi.
    """
    redis_key_status = f"user:{instance.tg_id}:status"
    redis_key_lang = f"user:{instance.tg_id}:chat_lang"
    redis_key_passport = f"user:{instance.tg_id}:passport"

    # Redisdan kalitlarni o'chirish
    redis_client.delete(redis_key_status)
    redis_client.delete(redis_key_lang)
    redis_client.delete(redis_key_passport)
