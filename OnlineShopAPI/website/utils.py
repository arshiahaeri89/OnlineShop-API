def upload_to(instance, filename):
    return f'product_images/{instance.product.product_code}/{filename}' # TODO: Handle Filename
