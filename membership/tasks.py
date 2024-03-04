import stripe
from celery import shared_task
from django.conf import settings
from djstripe.models import Price, Product


@shared_task
def sync_donation_tier_to_stripe(donationtier_id):
    from membership.models import DonationTier

    donation_tier = DonationTier.objects.get(id=donationtier_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_product_search = stripe.Product.search(
        query="active:'true' AND name:'Recurring Donation'"
    )
    if len(stripe_product_search["data"]) > 1:
        raise LookupError("Incorrect number of stripe products found")
    if len(stripe_product_search["data"]) < 1:
        stripe_product = stripe.Product.create(
            name="Recurring Donation",
            active=True,
            description=(
                "Recurring Donation to Philly Bike Action, "
                "a registered charity in The Commonwealth of Pennsylvania. "
                "Contributions to Philly Bike Action are not deductible "
                "as charitable contributions for federal income tax purposes."
            ),
            shippable=False,
            statement_descriptor="Philly Bike Action",
        )
    else:
        stripe_product = stripe.Product.retrieve(stripe_product_search["data"][0]["id"])

    product = Product()._get_or_retrieve(stripe_product.id)

    price_search = [
        p
        for p in stripe.Price.search(query=f"product:'{stripe_product.id}'")["data"]
        if p.get("metadata", {}).get("donationtier_id", None) == str(donationtier_id)
        and p.get("recurring", {}).get("interval", None) == donation_tier.get_recurrence_display()
    ]
    if len(price_search) > 1:
        raise LookupError("Incorrect number of stripe prices found")
    elif len(price_search) < 1:
        price = Price.create(
            product=product,
            currency="USD",
            unit_amount=int(donation_tier.cost),
            recurring={"interval": donation_tier.get_recurrence_display(), "interval_count": 1},
            metadata={"donationtier_id": str(donationtier_id)},
        )
    else:
        price = Price()._get_or_retrieve(price_search[0]["id"])

    donation_tier.stripe_price = price
    donation_tier.save()
