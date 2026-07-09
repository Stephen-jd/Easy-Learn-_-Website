from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Project(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    ]
    name = models.CharField(max_length=255, help_text="e.g., SMVITM - Udupi")
    duration_days = models.IntegerField(help_text="Duration in days")
    start_date = models.DateField()
    end_date = models.DateField()
    technology = models.CharField(max_length=255, help_text="e.g., Django, Python Fullstack")
    semester_year = models.CharField(max_length=100, help_text="e.g., 4th Sem, 6th Sem")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.technology})"

class TrainerProfile(models.Model):
    QUOTED_TYPE_CHOICES = [
        ('Daily', 'Daily Rate (INR)'),
        ('Monthly', 'Monthly Rate (INR)'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    photo = models.ImageField(upload_to='trainers/photos/', blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, help_text="12-digit Aadhaar Number")
    aadhaar_file = models.FileField(upload_to='trainers/aadhaar/', blank=True, null=True)
    pan_card = models.CharField(max_length=10, help_text="10-digit PAN Card Number")
    
    # Bank Details
    bank_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=50)
    bank_ifsc = models.CharField(max_length=20, help_text="IFSC Code")
    upi_id = models.CharField(max_length=100, help_text="UPI ID (e.g. user@okaxis)")
    
    # Quote Details
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in INR")
    quoted_type = models.CharField(max_length=10, choices=QUOTED_TYPE_CHOICES, default='Daily')
    
    # Projects mapping
    projects = models.ManyToManyField(Project, blank=True, related_name='trainers')
    
    # Administrative control
    is_approved = models.BooleanField(default=True, help_text="Approved by admin")
    is_active = models.BooleanField(default=True, help_text="Active status")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"

    @property
    def is_deactivated_by_projects(self):
        """
        If all projects assigned to this trainer are Completed, the trainer should be deactivated automatically.
        """
        # If there are no projects, they are considered active unless manually deactivated
        assigned_projects = self.projects.all()
        if not assigned_projects.exists():
            return False
        
        # If all assigned projects are 'Completed', trainer is deactivated
        return not assigned_projects.filter(status='Active').exists()

    @property
    def is_trainer_accessible(self):
        """
        True if trainer is active and not deactivated by all projects being over.
        """
        return self.is_active and self.is_approved and not self.is_deactivated_by_projects

class DailyWorkload(models.Model):
    SESSIONS_CHOICES = [
        (2, '2 Sessions per Day'),
        (3, '3 Sessions per Day'),
    ]
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_workloads')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='daily_workloads')
    date = models.DateField()
    sessions_count = models.IntegerField(choices=SESSIONS_CHOICES, default=2)
    topics_covered = models.TextField(blank=True, null=True, help_text="Summary of topics covered")
    subtopics_covered = models.TextField(blank=True, null=True, help_text="Summary of subtopics covered")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('trainer', 'project', 'date')

    def __str__(self):
        return f"{self.trainer.username} - {self.project.name} - {self.date}"

class SessionDetail(models.Model):
    workload = models.ForeignKey(DailyWorkload, on_delete=models.CASCADE, related_name='session_details')
    session_num = models.IntegerField()  # 1, 2, or 3
    time_slot = models.CharField(max_length=100, help_text="e.g. 09:00 AM - 11:00 AM")
    batch = models.CharField(max_length=100, help_text="e.g. Batch A")
    content_covered = models.TextField()

    class Meta:
        ordering = ['session_num']
        unique_together = ('workload', 'session_num')

    def __str__(self):
        return f"Session {self.session_num} - {self.time_slot} - {self.batch}"

class ClassWorkNote(models.Model):
    workload = models.ForeignKey(DailyWorkload, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='workloads/notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notes for {self.workload.id} - {self.file.name}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Travel', 'Travel/Transport'),
        ('Accommodation', 'Accommodation/Hotel'),
        ('Food', 'Food/Meals'),
        ('Trainer Fee', 'Trainer Fee/Honorarium'),
        ('Materials', 'Training Materials/Infrastructure'),
        ('Miscellaneous', 'Miscellaneous Expenses'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.project.name} - {self.category} - ₹{self.amount} ({self.date})"

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Paid', 'Paid'),
    ]
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invoices')
    month = models.CharField(max_length=7, help_text="e.g., YYYY-MM format")
    total_working_days = models.IntegerField(default=0)
    total_holidays = models.IntegerField(default=0)
    sick_leaves = models.IntegerField(default=0, help_text="Sick or other medical leaves (deductible)")
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice - {self.trainer.username} - {self.project.name} - {self.month} ({self.status})"
