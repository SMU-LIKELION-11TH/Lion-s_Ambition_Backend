from store.models import *


def serializeEmailValidation(entity: EmailValidation) -> dict:
    return {
        "email": entity.email,
        "created_at": entity.created_at,
    }

def serializeUser(entity: User) -> dict:
    return {
        "id": entity.pk,
        "name": entity.name,
        "email": entity.email,
    }

def serializeOrder(entity: Order) -> dict:
    items = OrderItem.objects.filter(order=entity)
    total_price = 0
    for item in items:
        total_price += item.unit_price * item.quantity
    return {
        "id": entity.pk,
        "status": {
            "id": entity.status.pk,
            "name": entity.status.name,
        },
        "items": list(map(serializeOrderItem, items)),
        "total_price": total_price,
        "created_at": entity.created_at,
        "updated_at": entity.updated_at,
    }

def serializeOrderItem(entity: OrderItem) -> dict:
    return {
        "id": entity.pk,
        "product": {
            "id": entity.product.pk,
            "name": entity.product.name,
        },
        "unit-price": entity.unit_price,
        "quantity": entity.quantity,
    }

def serializeProduct(entity: Product) -> dict:
    return {
        "id": entity.pk,
        "category": serializeCategory(entity.category),
        "name": entity.name,
        "image_url": entity.primary_image_url,
        "price": entity.regular_price,
        "is_soldout": entity.is_soldout,
    }

def serializeCategory(entity: Category) -> dict:
    return {
        "id": entity.pk,
        "name": entity.name,
    }
