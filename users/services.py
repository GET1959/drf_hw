import stripe

from config.settings import STRIPE_API_KEY
from users.models import SendPayment

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(payment_subject: SendPayment):
    """ Возвращает id продукта в страйпе. """
    if payment_subject.lesson:
        name = payment_subject.lesson.title
    else:
        name = payment_subject.course.title

    stripe_product = stripe.Product.create(
        name=name
    )
    return stripe_product["id"]


def create_stripe_price(payment_subject: SendPayment, product: str):
    """ Создает цену в страйпе. """
    if payment_subject.lesson:
        product_price = payment_subject.lesson.price
    else:
        product_price = payment_subject.course.price

    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=int(product_price * 100),
        product=product,
    )
    return stripe_price


def create_stripe_session(price):
    """ Создает сессию на оплату в страйпе. """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
