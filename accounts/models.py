from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
#for use from regex
import re
import random
import shortuuid
# library used to generate short unique ids instead of long uuid strings




def random_mobile():
    # generate a random iranian mobile number
    # starts with 09 and then generates 9 random digits
    return "09" + "".join(str(random.randint(0, 9)) for _ in range(9))


def random_id_code():
    # generate a random 10 digit national id code
    # used as default value when id_code is not provided
    return "".join(str(random.randint(0, 9)) for _ in range(10))

def validate_mobile(value):
    pattern = r'^09\d{9}$'
    #phone is start with 09 Then comes 9 digits.
    if not re.match(pattern, value):
        raise ValidationError("The mobile number is not valid")


def validate_id_code(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError("id code must be exactly 10 digits.")


class CustomManager(BaseUserManager):

    def create_user(self, id_code, email, mobile, password=None,**kwargs):
        if not id_code:
            raise ValueError("id_code can not be empty.")
        if not email:
            raise ValueError("email can not be empty.")
        if not mobile:
            raise ValueError("Mobile number is required.")

        validate_id_code(id_code)
        validate_mobile(mobile)
        email = self.normalize_email(email)
        user = self.model(id_code=id_code,email=email,mobile=mobile,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_superuser(self, id_code, email,mobile, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        
        if password is None:
            raise ValueError("Superuser must have a password.")
        
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(id_code, email,mobile, password, **kwargs)



# ۱. ابتدا این تابع رو بالای کلاس UserModel اضافه کن
def generate_short_uuid():
    return shortuuid.uuid()

class UserModel(AbstractBaseUser, PermissionsMixin):

    id_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_id_code],
        default=random_id_code  
    )
    mobile = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_mobile],
        default=random_mobile  
    )
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
     
    uuid_id = models.CharField(
        max_length=22,
        default=generate_short_uuid, 
        unique=True,
        editable=False
    )

    USERNAME_FIELD = "id_code"
    REQUIRED_FIELDS = ["email", "mobile"]

    objects = CustomManager()

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE,related_name="profile")
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="profile/",null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


    def __str__(self):
        return f"{self.user.id_code} - {self.first_name} {self.last_name}"

