def get_account_type(user):
    if user.is_staff:
        return "admin"
    if hasattr(user, 'customer_profile'):
        return "customer"
    if hasattr(user, 'merchant_profile'):
        return "merchant"
    return "unknown"