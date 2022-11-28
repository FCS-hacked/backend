import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from backend import settings
from unauth.utils import check_password


class CustomUser(AbstractUser):
    wallet_address = models.CharField(max_length=255, blank=True)
    HOTP_secret = models.CharField(max_length=32, blank=True)
    HOTP_counter = models.IntegerField(default=0)
    email = models.EmailField("email address", blank=True, unique=True)
    two_factor_enabled = models.BooleanField(default=True)
    upload_till_now = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.HOTP_secret:
            self.initialize_hotp()
        super(CustomUser, self).save(*args, **kwargs)

    def verify_otp(self, otp):
        if os.getenv("DEBUG_OTP", "False") == "True" or not self.two_factor_enabled:
            return True
        import pyotp
        result = pyotp.HOTP(self.HOTP_secret).verify(otp, self.HOTP_counter)
        if result:
            self.HOTP_counter += 1
            self.save()
        return result

    def initialize_hotp(self):
        import pyotp
        self.HOTP_secret = pyotp.random_base32()
        self.HOTP_counter = 0
        self.save()
        return pyotp.HOTP(self.HOTP_secret).provisioning_uri(self.email, issuer_name="Hacked")

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def get_wallet_verification_payload(self, unix_time) -> int:
        from hashlib import sha256
        pre_payload = f"a|{self.id}|get_wallet_verification_payload|{settings.SECRET_KEY}|{unix_time}|z"
        return int(sha256(pre_payload.encode()).hexdigest(), 16)

    def fetch_wallet_address(self, unix_time, rpc=settings.DEFAULT_RPC, throw=False):
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(rpc))

        contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=settings.CONTRACT_ABI)
        try:
            return contract.functions.read_directory(self.get_wallet_verification_payload(unix_time)).call()
        except Exception as e:
            if throw:
                raise e
            print(e)
            return self.fetch_wallet_address(settings.PRIVATE_RPC, throw=True)


class Organization(models.Model):
    class OrganizationCategory(models.TextChoices):
        HOSPITAL = "1", "Hospital"
        PHARMACY = "2", "Pharmacy"
        INSURANCE = "3", "Insurance"

    category = models.CharField(choices=OrganizationCategory.choices, max_length=2)
    # name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.TextField()
    location = models.TextField()
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="organization")

    # Handle size
    licenses = models.FileField(upload_to='licenses/', null=True, blank=True)
    permits = models.FileField(upload_to='permits/', null=True, blank=True)


class PersonalUser(models.Model):
    class PersonalUserCategory(models.TextChoices):
        PATIENT = "1", "Patient"
        PROFESSIONAL = "2", "Professional"

    category = models.CharField(choices=PersonalUserCategory.choices, max_length=2)
    # name = models.CharField(max_length=255)
    address = models.TextField()
    date_of_birth = models.DateField()
    proof_of_identity = models.FileField(upload_to='proof_of_id/')
    proof_of_address = models.FileField(upload_to='proof_of_address/')
    health_license = models.FileField(upload_to='health_license/', null=True, blank=True)
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="personal_user")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)


class CustomUserProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'
