from re import M
from unicodedata import name
from django.db import models
from .storage import OverwriteStorage
from PIL import Image
from enum import Enum
from django.core.validators import FileExtensionValidator
# Create your models here.
class AttendanceStatus(Enum):
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'
class SelectionStatus(Enum):
    SELECTED_IN_CITY_LEVEL = 'SELECTED_IN_CITY_LEVEL'
    SELECTED_IN_ZONAL_FINAL = 'SELECTED_IN_ZONAL_FINAL'
    SELECTED_IN_FINAL='SELECTED_IN_FINAL'
    NOT_SELECTED = 'NOT_SELECTED'

class RazorpayPlayerRelation(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    order_id = models.CharField(max_length=300,blank=True, null=True)
class MasterCategory(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    en = models.CharField(max_length=100, null=True)
    include = models.BooleanField(null=True, default=False, db_index=True)

    def __repr__(self) -> str:
        return str(self.en)

    def __str__(self) -> str:
        return str(self.en)
    class Meta:
        verbose_name=("Master Category")
        verbose_name_plural=("Master Categories")

class MasterRoles(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    en = models.CharField(max_length=100, null=True)
    include = models.BooleanField(null=True, default=False, db_index=True)

    def __repr__(self) -> str:
        return str(self.en)

    def __str__(self) -> str:
        return str(self.en)
    class Meta:
        verbose_name=("Master Role")
        verbose_name_plural=("Master Roles")


class MasterSeason(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    en = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)
    include = models.BooleanField(null=True, default=False, db_index=True)

    def __repr__(self) -> str:
        return str(self.en)

    def __str__(self) -> str:
        return str(self.en)


class MasterState(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True,)
    name = models.CharField(max_length=200, null=True, db_index=True)
    country_id = models.CharField(max_length=300, null=True)
    include = models.BooleanField(null=True, default=False, db_index=True)

    def __repr__(self) -> str:
        return str(self.name)

    def __str__(self) -> str:
        return str(self.name)


class MasterCity(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    city = models.CharField(max_length=200, null=True, db_index=True)
    # state_id=models.IntegerField(null=True)
    state = models.ForeignKey(
        MasterState, null=True, verbose_name="State ID", on_delete=models.SET_NULL, db_index=True)
    include = models.BooleanField(null=True, default=False, db_index=True)
    

    def __repr__(self) -> str:
        return str(self.city)

    def __str__(self) -> str:
        return str(self.city)
    class Meta:
        verbose_name=("Master City")
        verbose_name_plural=("Master Cities")


class MasterPosition(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True,)
    position = models.CharField(max_length=200, null=True, db_index=True)
    label = models.CharField(max_length=200, null=True, db_index=True)
    type = models.CharField(max_length=200, null=True, db_index=True)

    def __repr__(self) -> str:
        return str(self.label)

    def __str__(self) -> str:
        return str(self.label)

class MasterDateLimit(models.Model):
    id = models.CharField(max_length=150, primary_key=True, db_index=True)

    lowerlimit = models.DateField(db_index=True)
    upperlimit = models.DateField(db_index=True)
    season = models.ForeignKey(
        MasterSeason, null=True, verbose_name="master_season_id_limit", db_index=True, on_delete=models.SET_NULL)


    def __repr__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return str(self.id)
class MasterGroup(models.Model):
    id = models.CharField(max_length=150, primary_key=True, db_index=True)
    group = models.CharField(max_length=300, null=True, db_index=True)
    year = models.CharField(max_length=300, null=True, db_index=True)
    start = models.DateField(db_index=True)
    end = models.DateField(db_index=True)
    include = models.BooleanField(null=True, default=True, db_index=True)
    orderid = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, default="Female", db_index=True)

    def __repr__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return str(self.id)


class MasterGroupCity(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    cityid = models.ForeignKey(
        MasterCity, null=True, verbose_name="master_city_id", db_index=True, on_delete=models.SET_NULL)
    groupid = models.ForeignKey(
        MasterGroup, null=True, verbose_name="master group id", db_index=True, on_delete=models.SET_NULL)

    include = models.BooleanField(null=True, default=True, db_index=True)
    editable = models.BooleanField(null=True,blank=True, default=True, db_index=True)
    dateofevent=models.DateField(null=True,blank=True,db_index=True)

    def __repr__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name=("Master Group City")
        verbose_name_plural=("Master Group Cities")


class MasterLabels(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    en = models.TextField(null=True, blank=True,)
    hi = models.TextField(blank=True,null=True)
    mr = models.TextField(blank=True,null=True)
    asm = models.TextField(blank=True,null=True)
    ben = models.TextField(blank=True,null=True)
    odia = models.TextField(blank=True,null=True)
    bodo = models.TextField(blank=True,null=True)

    extrainfo = models.CharField(max_length=200,blank=True, null=True)

    def __repr__(self) -> str:
        return str(self.en)

    def __str__(self) -> str:
        return str(self.en)
    class Meta:
        verbose_name=("Master Label")
        verbose_name_plural=("Master Labels")


class MasterDocument(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    en = models.CharField(max_length=300,blank=True, null=True)
    hi = models.CharField(max_length=300,blank=True, null=True)
    mr = models.CharField(max_length=300,blank=True, null=True)
    asm = models.CharField(max_length=300,blank=True, null=True)
    ben = models.CharField(max_length=300,blank=True, null=True)
    odia = models.CharField(max_length=300,blank=True, null=True)
    bodo = models.CharField(max_length=300,blank=True, null=True)
    include = models.BooleanField(null=True,blank=True, default=True, db_index=True)

    def __repr__(self) -> str:
        return str(self.en)

    def __str__(self) -> str:
        return str(self.en)


class MasterColumn(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    columnid = models.CharField(max_length=300,blank=True, null=True, db_index=True)
    label_key = models.CharField(max_length=300,blank=True, null=True)
    includep1 = models.BooleanField(null=True,blank=True, default=True, db_index=True)
    includep2 = models.BooleanField(null=True,blank=True, default=True, db_index=True)
    type = models.CharField(max_length=300,blank=True, null=True)
    orderid = models.IntegerField(null=True,blank=True,)


# class Coach(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     userid = models.CharField(max_length=300)
#     password = models.CharField(max_length=300)
#     first_name = models.CharField(max_length=300, null=True)
#     last_name = models.CharField(max_length=300, null=True)
#     mobile = models.CharField(max_length=10, unique=True, default="")
#     email = models.EmailField(null=True)
#     academy = models.CharField(max_length=300, null=True)

class Upload(models.Model):
    unique = models.CharField(max_length=400, null=True, db_index=True)
    image = models.ImageField(storage=OverwriteStorage(), upload_to='images')
    fname = models.CharField(max_length=300, null=True,default="")
    lname = models.CharField(max_length=300, null=True,default="")
    mobilenumberupload = models.CharField(max_length=10, null=True, default="")
    

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Uploadfile(models.Model):
    unique = models.CharField(max_length=400, null=True, db_index=True)
    fname = models.CharField(max_length=300, null=True)
    lname = models.CharField(max_length=300, null=True)
    mobilenumberupload = models.CharField(max_length=10, null=True)
    file = models.ImageField(
        storage=OverwriteStorage(), upload_to='documents',)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.file.path)
        if img.height > 440 or img.width > 440:
            output_size = (440, 440)
            img.thumbnail(output_size)
            img.save(self.file.path)

class ScoutCourse(models.Model):
    id = models.CharField(max_length=100, primary_key=True,db_index=True)
    course=models.TextField(null=True, blank=True,)
    amount = models.CharField(max_length=100,null=True,blank=True)
    extra=models.CharField(max_length=100,null=True, blank=True,)
class ScoutDiscountType(models.Model):
    id = models.CharField(max_length=100, primary_key=True,db_index=True)
    type=models.CharField(max_length=100,null=True, blank=True,)
    length=models.CharField(max_length=100,null=True, blank=True,)
    extra=models.CharField(max_length=100,null=True, blank=True,)

class ScoutCourseDiscount(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    course=models.ForeignKey(ScoutCourse,null=True, verbose_name="ScoutCourses", db_index=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(
    ScoutDiscountType, null=True, verbose_name="ScoutDiscountTypes", db_index=True, on_delete=models.SET_NULL)
    discount=models.CharField(max_length=100,null=True, blank=True,)
class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.CharField(max_length=300,blank=True,)
    password = models.CharField(max_length=300,blank=True,)
    team=models.CharField(max_length=5,default='',blank=True)
    position1=models.CharField(max_length=50,default='',verbose_name="Position given",blank=True)
    present = models.BooleanField(default=False,null=True,blank=True)
    selection= models.CharField(max_length=25,null=True,blank=True, choices=[(status.name, status.value) for status in SelectionStatus])


#   tournament city
    tournament_city = models.ForeignKey( 
        MasterCity, null=True, verbose_name="master city", db_index=True, on_delete=models.SET_NULL)
    tournament_state = models.ForeignKey(
        MasterState, null=True, verbose_name="master state", related_name='state2', db_index=True, on_delete=models.SET_NULL)

#   profile
    gender = models.CharField(max_length=200, null=True, db_index=True)
    first_name = models.CharField(max_length=300, null=True)
    last_name = models.CharField(max_length=300, null=True,blank=True)
    height = models.CharField(max_length=10,blank=True, db_index=True)
    weight = models.CharField(max_length=10,blank=True, db_index=True)

#   Player Position
    primary_position = models.ForeignKey(MasterPosition, null=True, related_name='primary_position2',
                                         verbose_name="primary position", db_index=True, on_delete=models.SET_NULL)
    secondary_position = models.ForeignKey(MasterPosition, null=True, related_name='secondary_position',
                                           verbose_name="secondary position", db_index=True, on_delete=models.SET_NULL)

#   Contact Information
    mobile = models.CharField(max_length=10, null=True, default="")
    radiomobile = models.BooleanField(blank=True,null=True)
    whatsapp = models.CharField(max_length=10,blank=True, null=True)
    email = models.EmailField(null=True,blank=True,)
    ipv4 = models.GenericIPAddressField(max_length=100,blank=True, null=True)
    ipv6 = models.GenericIPAddressField(max_length=100,blank=True, null=True)
    ikfuniqueid = models.CharField(max_length=200, null=True, db_index=True)


#   Address
    address_line1 = models.TextField(blank=True,null=True)
    address_line2 = models.TextField(blank=True,null=True)
    state = models.ForeignKey(
        MasterState, null=True, verbose_name="state", related_name='state',blank=True, db_index=True, on_delete=models.SET_NULL)
    pincode = models.IntegerField(null=True,blank=True, db_index=True)

#   File location
    pic_file = models.CharField(max_length=300,blank=True, null=True)

    document_id_selected = models.ForeignKey(
        MasterDocument, null=True, verbose_name="document", db_index=True,blank=True, on_delete=models.SET_NULL)
    document_id_number = models.CharField(max_length=300,blank=True, null=True)
    document_id_file = models.CharField(max_length=300,blank=True, null=True)
    playeruploadid = models.CharField(max_length=300,blank=True, null=True)

# Coach Id
    coach_id=models.CharField(max_length=300,blank=True, null=True)
#   Dates
    dob = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    language = models.CharField(max_length=10,blank=True,)
    status = models.CharField(max_length=10, null=True,blank=True, db_index=True)

    season = models.ForeignKey(
        MasterSeason, null=True, verbose_name="master_season_id", db_index=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        MasterCategory, null=True, verbose_name="master_category_id", db_index=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(
        MasterGroup, null=True, verbose_name="master_group_id", db_index=True, on_delete=models.SET_NULL)
    whoisfilling = models.ForeignKey(
        MasterRoles, null=True, verbose_name="master_roles_id", db_index=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=300,blank=True, null=True)

    status = models.CharField(max_length=10, null=True,blank=True, db_index=True)
    razorpay_order_id = models.CharField(max_length=300,blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=300,blank=True, null=True)
    razorpay_signature = models.CharField(max_length=400,blank=True, null=True)
    error_code = models.CharField(max_length=300,blank=True, null=True)
    error_description = models.CharField(max_length=400,blank=True, null=True)
    error_source = models.CharField(max_length=300,blank=True, null=True)
    error_reason = models.CharField(max_length=300,blank=True, null=True)
    error_meta_order_id = models.CharField(max_length=300,blank=True, null=True)
    error_meta_payment_id = models.CharField(max_length=300,blank=True, null=True)
    amount = models.CharField(max_length=100,blank=True, null=True)
    razorpay_unique_id=models.CharField(max_length=100,blank=True, null=True)
    upload_id_frgn=models.ForeignKey(
        Upload, null=True, verbose_name="upload_id_frgn",blank=True, db_index=True, on_delete=models.SET_NULL)
    upload_file_id_frgn=models.ForeignKey(
        Uploadfile, null=True, verbose_name="uploadFile_id_frgn",blank=True, db_index=True, on_delete=models.SET_NULL)
    whatsapp_sent = models.BooleanField(null=True,blank=True, default=False, db_index=True)
    player_added_interakt = models.BooleanField(null=True,blank=True, default=False, db_index=True)
    referral = models.CharField(max_length=100,blank=True,null=True)
    discount = models.CharField(max_length=100,blank=True,null=True)
    pan=models.CharField(max_length=200,blank=True,null=True)
    extrafield1=models.CharField(max_length=200,blank=True,null=True)
    extrafield2=models.CharField(max_length=200,blank=True,null=True)

    course = models.ForeignKey( 
        ScoutCourse, null=True, verbose_name="Course", db_index=True, on_delete=models.SET_NULL)    
    

    def __repr__(self) -> str:
        return str(self.first_name)

    def __str__(self) -> str:
        return str(self.first_name)


class FailedPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    ikfuniqueid = models.CharField(max_length=200, null=True)
    razorpay_unique_id=models.CharField(max_length=100, null=True)
    playeruploadid = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, null=True, db_index=True)
    razorpay_order_id = models.CharField(max_length=300, null=True)
    razorpay_payment_id = models.CharField(max_length=300, null=True)
    razorpay_signature = models.CharField(max_length=400, null=True)
    error_code = models.CharField(max_length=300, null=True)
    error_description = models.CharField(max_length=400, null=True)
    error_source = models.CharField(max_length=300, null=True)
    error_reason = models.CharField(max_length=300, null=True)
    error_meta_order_id = models.CharField(max_length=300, null=True)
    error_meta_payment_id = models.CharField(max_length=300, null=True)
    amount = models.CharField(max_length=100, null=True)





class MasterAmount(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    city = models.ForeignKey(
        MasterCity, null=True, verbose_name="master_city_id", db_index=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(
        MasterSeason, null=True, verbose_name="master_season_id", db_index=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        MasterCategory, null=True, verbose_name="master_category_id", db_index=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(
        MasterGroup, null=True, verbose_name="master_group_id", db_index=True, on_delete=models.SET_NULL)
    coach_or_player = models.ForeignKey(
        MasterRoles, null=True, verbose_name="master_roles_id", db_index=True, on_delete=models.SET_NULL)
    amount = models.CharField(max_length=100, null=True)
    discount = models.CharField(max_length=100, null=True)

    include = models.BooleanField(null=True, default=True, db_index=True)

class MasterPartner(models.Model):
    id = models.CharField(max_length=100, primary_key=True,db_index=True)
    partner_name = models.CharField(max_length=300, null=True)
    mobile = models.CharField(max_length=100,blank=True, null=True)
    email=models.EmailField(max_length=300,blank=True,null=True)
    address=models.CharField(max_length=300,blank=True,null=True)
    city= models.ForeignKey(
        MasterCity, null=True, verbose_name="master_city_id", db_index=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(
        MasterSeason, null=True, verbose_name="master_season_id", db_index=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        MasterCategory, null=True, verbose_name="master_category_id", db_index=True, on_delete=models.SET_NULL)
    dateofevent=models.DateField(null=True,blank=True,db_index=True)

    
    include = models.BooleanField(null=True, default=True, db_index=True)
#user=models.ForeignKey(User,null=True,  verbose_name="files", on_delete=models.CASCADE)



class Lang(models.Model):
    id = models.CharField(max_length=100, primary_key=True, db_index=True)
    lang = models.CharField(max_length=100,)
class HomeBanner(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/homebanner', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True,)
    heading_1 = models.CharField(max_length=200, null=True, blank=True,)
    heading_2_colored = models.CharField(
        max_length=200, null=True, blank=True,)

    description = models.TextField(null=True, blank=True)
    button1_text = models.CharField(max_length=100, null=True, blank=True)
    button2_text = models.CharField(max_length=100, null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language21", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )


class TabelWorkshopsReg(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    First_Column = models.CharField(max_length=200, null=True, db_index=True)
    Second_Column = models.CharField(max_length=200, null=True, db_index=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language21", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )

class WorkShopsRegButton(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    button_text = models.CharField(max_length=200, null=True, db_index=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language21", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )


class WorkShopsRegFeatureStrip(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True,)
    keydata = models.CharField(max_length=200, null=True, db_index=True,)
    heading = models.CharField(max_length=100, null=True, blank=True,)
    paragraph = models.CharField(max_length=200, null=True, blank=True,)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/WorkshopFeatureStrip', null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language21", on_delete=models.SET_NULL, db_index=True,)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )


class WorkShopsRegExperts(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True,)
    keydata = models.CharField(max_length=200, null=True, db_index=True,)
    heading1 = models.CharField(max_length=100, null=True, blank=True,)
    heading2 = models.CharField(max_length=100, null=True, blank=True,)
    paragraph = models.CharField(max_length=500, null=True, blank=True,)
    button_text = models.CharField(max_length=200, null=True, db_index=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/LearnFromExperts', null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language21", on_delete=models.SET_NULL, db_index=True,)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )
    
class ActiveStatusNav(models.Model):
    id = models.CharField(primary_key=True, max_length=200, db_index=True)


class TrialsAndInitiativeType(models.Model):
    id = models.CharField(primary_key=True, max_length=200, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
class TrialsAndInitiativeNav(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    name = models.CharField(max_length=1000, null=True, blank=True,)
    href = models.CharField(max_length=100, null=True, blank=True,)
    description = models.TextField(null=True, blank=True)
    bottomtext = models.TextField(null=True, blank=True)
    listtext = models.TextField(null=True, blank=True)
    pagetype = lang = models.ForeignKey(
        TrialsAndInitiativeType, null=True, verbose_name="TrialsAndInitiativeType", on_delete=models.SET_NULL, db_index=True)
    activestatus = models.ForeignKey(
        ActiveStatusNav, null=True, verbose_name="ActiveStatusNav", on_delete=models.SET_NULL, db_index=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language21", on_delete=models.SET_NULL, db_index=True)

    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )


class WorkShopsReg_Images(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    name = models.CharField(max_length=200, null=True, blank=True, )

    size = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/WorkShopsReg_Images', null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language27", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )
class Winners_Workshop_Images(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/Winners_Workshop_Images', null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language27", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )
class Clubs(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/clubs', null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language27", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )

class Testimonials(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/Testimonials_Pics', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language27", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )

class Previous_Workshop_Images(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    keydata = models.CharField(max_length=200, null=True, db_index=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(
        storage=OverwriteStorage(), upload_to='ui/Previous_Workshop', null=True, blank=True)
    lang = models.ForeignKey(
        Lang, null=True, verbose_name="language27", on_delete=models.SET_NULL, db_index=True)
    attr1 = models.CharField(max_length=200, null=True, blank=True,)
    attr2 = models.CharField(max_length=200, null=True, blank=True, )
    attr3 = models.CharField(max_length=200, null=True, blank=True, )
    attr4 = models.CharField(max_length=200, null=True, blank=True, )





