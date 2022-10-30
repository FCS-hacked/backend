from django.db import models

from authentication.models import CustomUser


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    shared_with = models.ManyToManyField(CustomUser, related_name="shared_documents", blank=True)
    sha_256 = models.CharField(max_length=64, null=True, blank=True)

    def is_signed_by(self, custom_user):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        import hashlib
        self.sha_256 = hashlib.sha256(self.document.read()).hexdigest()
        super(Document, self).save(*args, **kwargs)


class DocumentVerificationRequest(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="verification_requests")
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="verification_requests_raised")
    created_at = models.DateTimeField(auto_now_add=True)
    requested_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="verification_requests_received")
    transaction_hash = models.CharField(max_length=255, blank=True)

    @property
    def is_accepted(self):
        return self.transaction_hash != ""
