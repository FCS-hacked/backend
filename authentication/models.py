from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    wallet_address = models.CharField(max_length=255, blank=True)
    HOTP_secret = models.CharField(max_length=32, blank=True)
    HOTP_counter = models.IntegerField(default=0)
    email = models.EmailField("email address", blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.HOTP_secret:
            self.initialize_hotp()
        super(CustomUser, self).save(*args, **kwargs)

    def verify_otp(self, otp):
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

    def __str__(self):
        return self.name


class PersonalUser(models.Model):
    class PersonalUserCategory(models.TextChoices):
        PATIENT = "1", "Patient"
        PROFESSIONAL = "2", "Professional"

    category = models.CharField(choices=PersonalUserCategory.choices, max_length=2)
    # name = models.CharField(max_length=255)
    address = models.TextField()
    date_of_birth = models.DateField()
    proof_of_id = models.FileField(upload_to='proof_of_id/')
    proof_of_address = models.FileField(upload_to='proof_of_address/')
    health_license = models.FileField(upload_to='health_license/', null=True, blank=True)
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="personal_user")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
