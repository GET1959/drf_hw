from rest_framework.serializers import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val and "youtube.com" not in tmp_val:
            raise ValidationError("Используется ссылка на внешний ресурс.")

