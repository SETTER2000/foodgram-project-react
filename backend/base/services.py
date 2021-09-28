from django.core.exceptions import ValidationError


def get_path_upload_img(instance, file):
    """Путь к файлу картинки, шаблон: <media/images/user_id/photo.jpg>."""
    return f'images/{instance.id}/{file}'


def validate_size_image(file):
    """Ограничения размера загружаемой картинки."""
    mb_limit = 2
    if file.size > mb_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {mb_limit}MB')

