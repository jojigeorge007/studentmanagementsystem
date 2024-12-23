from django.db import models
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import RegexValidator
import phonenumbers
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
phone_regex = RegexValidator(
        regex=r'^\d{9,15}$', 
        message="Phone number must be between 9 and 15 digits."
    )

def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:  # 10 MB
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    return value

class Country_Codes(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    calling_code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.country_name} ({self.calling_code})"
    
    class Meta:
        ordering = ['calling_code']

class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('razorpay','razorpay'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]



class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be provided')

        # Normalize the email if provided
        if email:
            email = self.normalize_email(email)

        # Handle phone number validation if provided and not a superuser
        if phone_number and not extra_fields.get('is_superuser'):
            full_number = f"{extra_fields.get('country_code')}{phone_number}"
            try:
                parsed_number = phonenumbers.parse(full_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number.")
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise ValidationError("Invalid phone number format.")

        # Create and return the user object
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError('Superuser must have an email address.')

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)


class User(AbstractBaseUser):
    created_at = models.DateTimeField(auto_now_add=True)
    # Role-based fields
    is_officestaff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    
    # Admin-related fields
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Any other fields common to both roles
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=30)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=20,blank=True,null=True)
    pin_code = models.CharField(max_length=10)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)
    joining_date = models.DateField(null=True,blank=True)
    watsapp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True,validators=[phone_regex], null=True, blank=True)
    country_code = models.ForeignKey('Country_Codes', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    groups = models.ManyToManyField(
        Group,
        related_name='app1_user_groups',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Override user_permissions field with a unique related_name
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='app1_user_permissions'  # Add a unique related_name
    )
    
    def __str__(self):
        return self.email if self.email else self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class OfficeStaff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_staff')
    custom_id = models.CharField(max_length=10, unique=True, editable=False, blank=True) 
    photo = models.ImageField(upload_to='os-photo/', null=True, blank=True, validators=[validate_file_size])
    id_copy = models.FileField(upload_to='id-officestaff/', blank=True, null=True, validators=[validate_file_size])
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    verification_id = models.CharField(max_length=255, blank=True, null=True)  
    verificationid_number = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if not self.custom_id:
            # Generate the custom ID format
            self.custom_id = f'OS{self.user.id}'  # Format: FR{id}

        super(OfficeStaff, self).save(*args, **kwargs)


    def __str__(self):
        return self.custom_id 


class Librarian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarian')
    custom_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)  # Custom ID field   
    photo = models.ImageField(upload_to='l-photo/', null=True, blank=True, validators=[validate_file_size])  # Profile image field
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    verification_id = models.CharField(max_length=255, blank=True, null=True)  
    verificationid_number = models.CharField(max_length=50, blank=True, null=True)  # ID number field
    id_copy = models.FileField(upload_to='id-librarian/', blank=True, null=True, validators=[validate_file_size]) 
    created_date = models.DateTimeField(default=timezone.now)

    
    
    def save(self, *args, **kwargs):
        if not self.custom_id:
            
            self.custom_id = f'L{self.user.id}'

        super(Librarian, self).save(*args, **kwargs)

    def __str__(self):
        return self.custom_id 



    


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_number = models.IntegerField(unique=True, editable=False)  # Unique admission number
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)  # Custom ID field
    photo = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    class_level = models.IntegerField()
    admission_date = models.DateField()
    address = models.TextField()
    id_document = models.CharField(max_length=255, blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    id_proof_file = models.FileField(upload_to='id-student/', blank=True, null=True, validators=[validate_file_size])
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_relation = models.CharField(max_length=100, null=True, blank=True)
    guardian_number = models.CharField(max_length=15, unique=True, validators=[phone_regex], null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            # Generate a new admission number
            last_admission = Student.objects.all().order_by('-admission_number').first()
            self.admission_number = last_admission.admission_number + 1 if last_admission else 1
        
        if not self.custom_id:
            # Generate custom_id using admission_number
            self.custom_id = f"ST{self.admission_number:05d}"  # e.g., ST00001

        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.custom_id

    

class LibraryHistory(models.Model):
    BOOK_STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='library_history')
    book_name = models.CharField(max_length=200)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20,choices=BOOK_STATUS_CHOICES,default='borrowed')
    is_paid =  models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.return_date and self.return_date < timezone.now().date():
            self.status = 'overdue'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.first_name}'s book: {self.book_name}"
    


class FeesHistory(models.Model):
    FEE_TYPE_CHOICES = (
            ('tuition', 'Tuition'),
            ('library', 'Library'),
            ('exam', 'Exam'),
            ('other', 'Other')
        )
        
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees_history')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
        
    def __str__(self):
        return f"{self.student.first_name} - {self.fee_type} Fee"