import os
import random
import string

random_str = lambda N: ''.join(
    random.choice(string.ascii_lowercase + string.digits) for _ in range(N))


def upload_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f'product_images/{instance.product.product_code}/{instance.image_number}{file_extension.lower()}'


def generate_random_username():
    length = 7
    characters = string.digits
    return 'u' + ''.join(random.choice(characters) for _ in range(length))
