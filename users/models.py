from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError

# C0FFEE -> 12648430
def hex_to_int(value):
    if value is None:
        return None
    return int(value, 16)

# 12648430 -> C0FFEE
def int_to_hex(value):
    hex_val = format(value, 'X')
    # Pad with 0's, if needed
    hex_val = '0'*(6-len(hex_val)) + hex_val
    return hex_val


class RGBcolorField(models.CharField):
    description = 'A field for holding RGB color values'
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        self._validators = []
        self.validators.append(self.validate_all_values_hex)
        super().__init__(*args, **kwargs)

    def validate_all_values_hex(self, value):
        try:
            hex_to_int(value)
        except: 
            raise ValidationError('{} is not a hex value'.format(value))

    def db_type(self, connection):
        return 'UNSIGNED INTEGER(3)'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None 
        return int_to_hex(value)
    
    def get_prep_value(self, value):
        return hex_to_int(value)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    favorite_color = RGBcolorField(null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
