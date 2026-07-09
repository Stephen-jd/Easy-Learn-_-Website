from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from decimal import Decimal
from core.models import Project, TrainerProfile, DailyWorkload, ClassWorkNote, Expense, Invoice

class ModelAndCalculationTests(TestCase):
    def setUp(self):
        # Create active project
        self.project_active = Project.objects.create(
            name="SMVITM - Udupi",
            duration_days=30,
            start_date=datetime.date(2026, 5, 1),
            end_date=datetime.date(2026, 5, 30),
            technology="Django",
            semester_year="6th Sem",
            status="Active"
        )
        # Create another project that will be completed
        self.project_completed = Project.objects.create(
            name="BLDEA - Vijayapur",
            duration_days=15,
            start_date=datetime.date(2026, 4, 1),
            end_date=datetime.date(2026, 4, 15),
            technology="Python Fullstack",
            semester_year="4th Sem",
            status="Completed"
        )

        # Create trainer users
        self.user_trainer_active = User.objects.create_user(
            username="trainer_active",
            email="trainer@easylearn.com",
            password="testpassword123",
            first_name="Active",
            last_name="Trainer"
        )
        self.profile_active = TrainerProfile.objects.create(
            user=self.user_trainer_active,
            aadhaar_number="123456789012",
            pan_card="ABCDE1234F",
            bank_name="Test Bank",
            bank_account_number="9876543210",
            bank_ifsc="TSTB0001234",
            upi_id="active@okbank",
            quoted_amount=Decimal('1500.00'),
            quoted_type="Daily",
            is_approved=True,
            is_active=True
        )
        self.profile_active.projects.add(self.project_active)

        self.user_trainer_inactive = User.objects.create_user(
            username="trainer_inactive",
            email="inactive@easylearn.com",
            password="testpassword123",
            first_name="Inactive",
            last_name="Trainer"
        )
        self.profile_inactive = TrainerProfile.objects.create(
            user=self.user_trainer_inactive,
            aadhaar_number="210987654321",
            pan_card="XYZWV5678G",
            bank_name="Another Bank",
            bank_account_number="1234567890",
            bank_ifsc="ANTB0005678",
            upi_id="inactive@okbank",
            quoted_amount=Decimal('30000.00'),
            quoted_type="Monthly",
            is_approved=True,
            is_active=True
        )
        self.profile_inactive.projects.add(self.project_completed)

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@easylearn.com",
            password="adminpassword123"
        )

    def test_trainer_profile_properties(self):
        """
        Verify the properties is_deactivated_by_projects and is_trainer_accessible work.
        """
        # Active trainer is assigned to an active project
        self.assertFalse(self.profile_active.is_deactivated_by_projects)
        self.assertTrue(self.profile_active.is_trainer_accessible)

        # Inactive trainer is assigned ONLY to a completed project
        self.assertTrue(self.profile_inactive.is_deactivated_by_projects)
        self.assertFalse(self.profile_inactive.is_trainer_accessible)

        # Deactivating manually
        self.profile_active.is_active = False
        self.profile_active.save()
        self.assertFalse(self.profile_active.is_trainer_accessible)

    def test_invoice_calculation_daily_rate(self):
        """
        Verify invoice raises correctly with dynamic Daily quotes and deduction rules.
        """
        # Log 5 working days for the active trainer (Daily quote: 1500 INR/day)
        for i in range(1, 6):
            DailyWorkload.objects.create(
                trainer=self.user_trainer_active,
                project=self.project_active,
                date=datetime.date(2026, 5, i),
                sessions_count=2,
                topics_covered=f"Topic {i}",
                subtopics_covered=f"Subtopic {i}"
            )

        client = Client()
        client.login(username="trainer_active", password="testpassword123")
        
        # Raise invoice for May 2026 with 1 sick leave
        response = client.post(reverse('raise_invoice'), {
            'project': self.project_active.id,
            'month': '2026-05',
            'total_holidays': 2,
            'sick_leaves': 1
        })
        self.assertEqual(response.status_code, 302) # Redirects to trainer dashboard

        invoice = Invoice.objects.get(trainer=self.user_trainer_active, project=self.project_active, month='2026-05')
        self.assertEqual(invoice.total_working_days, 5)
        self.assertEqual(invoice.sick_leaves, 1)
        # 5 days * 1500 = 7500. 1 leave * 1500 = 1500 deduction. Total = 6000.
        self.assertEqual(invoice.deductions, Decimal('1500.00'))
        self.assertEqual(invoice.total_amount, Decimal('6000.00'))
        self.assertEqual(invoice.status, 'Pending')

    def test_invoice_calculation_monthly_rate(self):
        """
        Verify invoice calculations with Monthly quote.
        """
        # Let's temporarily activate profile_inactive by adding an active project
        self.profile_inactive.projects.add(self.project_active)
        self.profile_inactive.save()
        self.assertFalse(self.profile_inactive.is_deactivated_by_projects)

        # Log 10 working days for May
        for i in range(1, 11):
            DailyWorkload.objects.create(
                trainer=self.user_trainer_inactive,
                project=self.project_active,
                date=datetime.date(2026, 5, i),
                sessions_count=2,
                topics_covered=f"Topic {i}",
                subtopics_covered=f"Subtopic {i}"
            )

        client = Client()
        client.login(username="trainer_inactive", password="testpassword123")

        # Quoted amount is 30,000 Monthly. Daily equivalent is 30,000 / 24 = 1250 INR/day.
        # Raise invoice with 2 sick leaves
        response = client.post(reverse('raise_invoice'), {
            'project': self.project_active.id,
            'month': '2026-05',
            'total_holidays': 1,
            'sick_leaves': 2
        })
        self.assertEqual(response.status_code, 302)

        invoice = Invoice.objects.get(trainer=self.user_trainer_inactive, project=self.project_active, month='2026-05')
        self.assertEqual(invoice.total_working_days, 10)
        self.assertEqual(invoice.sick_leaves, 2)
        # Deductions = 2 * (30000 / 24) = 2 * 1250 = 2500. Net total = 30000 - 2500 = 27500.
        self.assertEqual(invoice.deductions, Decimal('2500.00'))
        self.assertEqual(invoice.total_amount, Decimal('27500.00'))

    def test_access_restriction_trainer_dashboard(self):
        """
        Verify access restrictions to the trainer dashboard.
        """
        client = Client()

        # Anonymous access should redirect to login
        response = client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        # Inactive trainer (assigned only to completed project) login
        client.login(username="trainer_inactive", password="testpassword123")
        response = client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 200)
        # Should render deactivation message template core/deactivated.html
        self.assertTemplateUsed(response, 'core/deactivated.html')

        # Admin login shouldn't access trainer dashboard; should redirect
        client.login(username="admin", password="adminpassword123")
        response = client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin_dashboard'))

    def test_access_restriction_admin_dashboard(self):
        """
        Verify access restrictions to the admin dashboard.
        """
        client = Client()

        # Anonymous access
        response = client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        
        # Trainer access should be denied & redirect to landing
        client.login(username="trainer_active", password="testpassword123")
        response = client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('landing'))

        # Superuser access should succeed
        client.login(username="admin", password="adminpassword123")
        response = client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/admin_dashboard.html')

