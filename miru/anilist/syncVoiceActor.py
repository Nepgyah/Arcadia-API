from talent.models import VoiceActor

def SyncVoiceActor(va_data):
    try:
        arcadia_va = VoiceActor.objects.get(
            first_name = va_data.get('name').get('first'),
            last_name = va_data.get('name').get('last')
        )
        print(f"Previous va found: {arcadia_va}")

    except VoiceActor.DoesNotExist:
        arcadia_va = VoiceActor.objects.create(
            first_name = va_data.get('name').get('first'),
            last_name = va_data.get('name').get('last'),
            cover_img_url = va_data.get('image').get('large')
        )
        print(f"Creating new va: {arcadia_va}")

    return arcadia_va