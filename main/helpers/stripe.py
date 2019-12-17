import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_API_SECRET


class StripeWrapper:
    @staticmethod
    def charge_create(token, amount, description=""):
        return stripe.Charge.create(
            source=token,
            amount=amount,
            currency='jpy',
            description=description,
        )

    # 請求書を取得
    @staticmethod
    def get_invoice_by_id(invoice_id):
        return stripe.Invoice.retrieve(invoice_id)

    # 次回請求書を取得
    @staticmethod
    def get_upcoming_invoice_by_subscription(subscription_id):
        return stripe.Invoice.upcoming(subscription=subscription_id)

    # subscriptionごとの請求書リストを取得
    @staticmethod
    def get_invoice_list_by_subscription_id(subscription_id,
                                            limit=10,
                                            starting_after=None):
        return stripe.Invoice.list(
            subscription=subscription_id,
            limit=limit,
            starting_after=starting_after)

    @classmethod
    def get_all_invoice_list_by_subscription_id(cls, subscription_id,
                                                limit=10):
        res = []
        invoice_list = cls.get_invoice_list_by_subscription_id(subscription_id)
        res.extend(invoice_list.data)
        while invoice_list.has_more:
            invoice_list = cls.get_invoice_list_by_subscription_id(
                subscription_id=subscription_id,
                limit=limit,
                starting_after=invoice_list.data[-1].id)
            res.extend(invoice_list.data)
        return res

    @staticmethod
    def refund_create(charge_id):
        return stripe.Refund.create(charge=charge_id)

    @staticmethod
    def product_create(name, _type='service'):
        return stripe.Product.create(
            name=name,
            type=_type,
        )

    @staticmethod
    def product_list(limit=10, active=True, starting_after=None):
        return stripe.Product.list(
            limit=limit, active=True, starting_after=starting_after)

    @classmethod
    def get_product_by_name(cls, name):
        p_list = cls.product_list()
        while p_list.has_more:
            for product in p_list.data:
                if product.name == name:
                    return product
            p_list = cls.product_list(starting_after=p_list.data[-1].id)
        for product in p_list.data:
            if product.name == name:
                return product
        return None

    @staticmethod
    def plan_create(amount, product_id, currency='jpy', interval='month'):
        return stripe.Plan.create(
            product=product_id,
            amount=amount,
            interval=interval,
            currency=currency,
        )

    @staticmethod
    def plan_list(limit=10, active=True, starting_after=None):
        return stripe.Plan.list(
            limit=limit, active=active, starting_after=starting_after)

    @classmethod
    def get_plan_by_product_id_and_amount(cls, product_id, amount):
        p_list = cls.plan_list()
        while p_list.has_more:
            for plan in p_list.data:
                if plan.product == product_id and plan.amount == amount:
                    return plan
            p_list = cls.plan_list(starting_after=p_list.data[-1].id)
        for plan in p_list.data:
            if plan.product == product_id and plan.amount == amount:
                return plan
        return None

    @staticmethod
    def token_create(number, exp_month, exp_year, cvc):
        return stripe.Token.create(
            card={
                'number': number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
            }, )

    @staticmethod
    def customer_create(token, description=""):
        return stripe.Customer.create(
            source=token,
            description=description,
        )

    @staticmethod
    def customer_retrieve(id, description=""):
        return stripe.Customer.retrieve(id)

    @staticmethod
    def customer_modify(id, **kwargs):
        return stripe.Customer.modify(id, **kwargs)

    @staticmethod
    def subscription_create(customer_id, plan_id):
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{
                "plan": plan_id
            }],
        )

    @staticmethod
    def subscription_list(limit=10,
                          status="active",
                          starting_after=None,
                          **kwargs):
        if status is not None:
            kwargs["status"] = status
        return stripe.Subscription.list(
            limit=limit, starting_after=starting_after, **kwargs)

    @staticmethod
    def subscription_retrieve(id):
        return stripe.Subscription.retrieve(id)

    @staticmethod
    def subscription_modify(id, **kwargs):
        return stripe.Subscription.modify(id, **kwargs)

    @classmethod
    def get_subscription_by_customer_id_and_plan_id(cls,
                                                    customer_id,
                                                    plan_id,
                                                    status=None):
        s_list = cls.subscription_list(status=status)
        while s_list.has_more:
            for subscription in s_list.data:
                print(subscription.id)
                if subscription.customer == customer_id and subscription.plan.id == plan_id:
                    return subscription
            s_list = cls.subscription_list(
                starting_after=s_list.data[-1].id, status=status)
        for subscription in s_list.data:
            print(subscription.id)
            if subscription.customer == customer_id and subscription.plan.id == plan_id:
                return subscription
        return None

    # subscriptionを削除
    @staticmethod
    def delete_subscription(subscription_id):
        stripe.Subscription.delete(subscription_id)
