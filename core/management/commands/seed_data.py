import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Project, TrainerProfile, DailyWorkload, Expense, Invoice, ClassWorkNote

class Command(BaseCommand):
    help = 'Seeds the database with professional training portal data for Easy Learn Academy.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Wiping old data to ensure clean slate...')
        
        # Clear existing data to remove dummy values
        Invoice.objects.all().delete()
        Expense.objects.all().delete()
        ClassWorkNote.objects.all().delete()
        DailyWorkload.objects.all().delete()
        TrainerProfile.objects.all().delete()
        User.objects.all().delete()
        Project.objects.all().delete()

        self.stdout.write('Creating professional database records...')

        # 1. Create Operations Manager (Admin)
        admin_user = User.objects.create_superuser(
            username='admin',
            email='manager.projects@easy-learn-academy.com',
            password='adminpassword123',
            first_name='Admin',
            last_name='Manager'
        )
        self.stdout.write(self.style.SUCCESS('Admin user created successfully! (User: admin / Pass: adminpassword123)'))

        # 2. Create the 4 Real Projects
        p1 = Project.objects.create(
            name="SMVITM - Udupi",
            duration_days=45,
            start_date=datetime.date(2026, 4, 1),
            end_date=datetime.date(2026, 5, 20),
            technology="Python Full Stack & Django",
            semester_year="6th Semester",
            status="Active"
        )
        self.stdout.write(self.style.SUCCESS(f'Project "{p1.name}" created.'))

        p2 = Project.objects.create(
            name="BLDEA - Vijayapur",
            duration_days=30,
            start_date=datetime.date(2026, 1, 10),
            end_date=datetime.date(2026, 2, 10),
            technology="Java Full Stack & Hibernate",
            semester_year="8th Semester",
            status="Completed"
        )
        self.stdout.write(self.style.SUCCESS(f'Project "{p2.name}" created.'))

        p3 = Project.objects.create(
            name="RYMEC - Bellari",
            duration_days=35,
            start_date=datetime.date(2026, 5, 1),
            end_date=datetime.date(2026, 6, 10),
            technology="Web Development & React",
            semester_year="4th Semester",
            status="Active"
        )
        self.stdout.write(self.style.SUCCESS(f'Project "{p3.name}" created.'))

        p4 = Project.objects.create(
            name="ASBLDEA - Vijayapur",
            duration_days=40,
            start_date=datetime.date(2026, 5, 5),
            end_date=datetime.date(2026, 6, 20),
            technology="Fullstack Web Application & Django",
            semester_year="6th Semester",
            status="Active"
        )
        self.stdout.write(self.style.SUCCESS(f'Project "{p4.name}" created.'))

        # 3. Create Trainer - Stephen Jebadurai
        trainer_user = User.objects.create_user(
            username='stephenjebadurai',
            email='stephenjebadurai.projects@easy-learn-academy.com',
            password='trainerpassword123',
            first_name='Stephen',
            last_name='Jebadurai'
        )
        trainer_profile = TrainerProfile.objects.create(
            user=trainer_user,
            aadhaar_number='123456789012',
            pan_card='ABCDE1234F',
            bank_name='State Bank of India',
            bank_account_number='32145678901',
            bank_ifsc='SBIN0001234',
            upi_id='stephenjebadurai@oksbi',
            quoted_amount=2000.00,
            quoted_type='Daily',
            is_approved=True,
            is_active=True
        )
        # Assign Stephen to the active projects
        trainer_profile.projects.add(p1)
        trainer_profile.projects.add(p3)
        trainer_profile.projects.add(p4)
        
        self.stdout.write(self.style.SUCCESS('Trainer "stephenjebadurai" created successfully! (User: stephenjebadurai / Pass: trainerpassword123)'))

        # 4. Create realistic daily workloads for Stephen Jebadurai on SMVITM - Udupi
        workloads_data = [
            (datetime.date(2026, 4, 15), 2, "HTML5 Semantic Elements & CSS Layouts", "Layout design using CSS Grid and Flexbox for corporate templates"),
            (datetime.date(2026, 4, 16), 2, "JavaScript DOM Operations", "Event listeners, element creation, dynamic page styling with JS"),
            (datetime.date(2026, 4, 17), 3, "Advanced JavaScript & Async Programming", "Promises, Fetch API, Async/Await and consuming external REST APIs"),
            (datetime.date(2026, 4, 20), 2, "Introduction to Django MTV", "Django structure, URLs configuration, views and template routing"),
            (datetime.date(2026, 4, 21), 2, "Django Database Models", "SQLite integration, Django ORM, migrations, and model relationships"),
            (datetime.date(2026, 4, 22), 2, "Django Forms & Validation", "Building forms, CSRF protection, and backend validation logic"),
            (datetime.date(2026, 4, 23), 3, "Django User Authentication System", "User login, registration, password hashing, and session management"),
            (datetime.date(2026, 4, 24), 2, "Building APIs with Django REST Framework", "DRF setup, serializers, API views, and response structures"),
        ]

        for date, sessions, topics, subtopics in workloads_data:
            DailyWorkload.objects.create(
                trainer=trainer_user,
                project=p1,
                date=date,
                sessions_count=sessions,
                topics_covered=topics,
                subtopics_covered=subtopics
            )
        self.stdout.write(self.style.SUCCESS('Daily workloads created for Stephen Jebadurai on SMVITM - Udupi.'))

        # 5. Create some professional expenses for these projects
        expenses_data = [
            (p1, datetime.date(2026, 4, 15), 'Travel', 1850.00, 'Train fare for Trainer Stephen (Mangaluru to Udupi & return)'),
            (p1, datetime.date(2026, 4, 20), 'Accommodation', 3500.00, '2 nights hotel stay for offline training bootcamp'),
            (p3, datetime.date(2026, 5, 5), 'Travel', 2800.00, 'Travel expenses for Bellari college onboarding'),
            (p3, datetime.date(2026, 5, 10), 'Food', 1500.00, 'Refreshments for students and coordinators during React bootcamp'),
            (p4, datetime.date(2026, 5, 8), 'Materials', 4200.00, 'Course handbooks and handbook printouts for ASBLDEA'),
        ]

        for project, date, category, amount, desc in expenses_data:
            Expense.objects.create(
                project=project,
                date=date,
                category=category,
                amount=amount,
                description=desc
            )
        self.stdout.write(self.style.SUCCESS('Professional expense records seeded.'))

        self.stdout.write(self.style.SUCCESS('Easy Learn Academy database seeded successfully!'))
