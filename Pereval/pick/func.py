def get_path_upload_photos(instance, file):
    return f'photos/pereval-{instance.pereval.id}/{file}'