from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    wallet_address = models.CharField(max_length=255, blank=True)


class Organization(models.Model):
    class OrganizationCategory(models.TextChoices):
        HOSPITAL = "1", "Hospital"
        PHARMACY = "2", "Pharmacy"
        INSURANCE = "3", "Insurance"

    category = models.CharField(choices=OrganizationCategory.choices, max_length=2)
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.TextField()
    location = models.TextField()
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

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
    name = models.CharField(max_length=255)
    address = models.TextField()
    date_of_birth = models.DateField()
    proof_of_id = models.FileField(upload_to='proof_of_id/')
    proof_of_address = models.FileField(upload_to='proof_of_address/')
    health_license = models.FileField(upload_to='health_license/', null=True, blank=True)
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

