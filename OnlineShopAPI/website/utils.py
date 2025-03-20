import random
import string


def upload_to(instance, filename):
    return f'product_images/{instance.product.product_code}/{filename}'  # TODO: Handle Filename


def generate_random_username():
    length = 7
    characters = string.digits
    return 'u' + ''.join(random.choice(characters) for _ in range(length))
