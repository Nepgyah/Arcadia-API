from talent.models import VoiceActor

def SyncVoiceActor(va_data):
    
    try:
        arcadia_va = VoiceActor.objects.get(
            first_name = va_data.get('name').get('first'),
            last_name = va_data.get('name').get('last')
        )
        
        if arcadia_va.cover_img_url is None:
            arcadia_va.cover_img_url = va_data.get('image').get('large')
            arcadia_va.save()

    except VoiceActor.DoesNotExist:
        arcadia_va = VoiceActor.objects.create(
            first_name = va_data.get('name').get('first'),
            last_name = va_data.get('name').get('last'),
            cover_img_url = va_data.get('image').get('large')
        )

    return arcadia_va