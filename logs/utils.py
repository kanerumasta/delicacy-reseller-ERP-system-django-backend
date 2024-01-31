from .models import TransactionLog

def log_transaction(user, action, details):
    TransactionLog.objects.create(user=user, action=action, details=details)