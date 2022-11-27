from django.db import models

from authentication.models import CustomUser
from backend import settings


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    shared_with = models.ManyToManyField(CustomUser, related_name="shared_documents", blank=True)
    sha_256 = models.CharField(max_length=64, null=True, blank=True)
    signed_by_professional = models.BooleanField(default=False)
    signed_by_hospital = models.BooleanField(default=False)
    signed_by_pharmacy = models.BooleanField(default=False)
    signed_by_insurance_firm = models.BooleanField(default=False)

    def is_signed_by(self, custom_user):
        return custom_user.wallet_address in self.get_signers()

    def save(self, *args, **kwargs):
        import hashlib
        self.sha_256 = hashlib.sha256(self.document.read()).hexdigest()
        super(Document, self).save(*args, **kwargs)

    def get_signers(self, rpc=settings.DEFAULT_RPC, throw=False):
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(rpc))

        contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=settings.CONTRACT_ABI)
        try:
            return contract.functions.get_file_signers(int(self.sha_256, 16)).call()
        except Exception as e:
            if throw:
                raise e
            print(e)
            return self.get_signers(settings.PRIVATE_RPC, throw=True)
