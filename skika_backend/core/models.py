from django.db import models

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=[('citizen', 'Citizen'), ('admin', 'Admin')])
    ward = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.role}"

class Report(models.Model):
    STATUS_CHOICES = [('Received', 'Received'), ('Under Review', 'Under Review'), ('Action Taken', 'Action Taken')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=20, unique=True)
    ward = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    audit_trail = models.TextField(default='Initial creation')

    def __str__(self):
        return f"{self.ref_id} - {self.status}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    ward = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    satisfaction = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.report.ref_id}"