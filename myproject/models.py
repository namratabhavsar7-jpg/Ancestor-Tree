from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class FamilyMember(models.Model):
    # ================= 1. PERSONAL DETAILS =================
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    other_gender = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    is_alive = models.BooleanField(default=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to='family_members/', blank=True, null=True)
    
    # ================= 2. CONTACT DETAILS =================
    contact_number_1 = models.CharField(max_length=15, blank=True, null=True)
    contact_number_2 = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # ================= 3. LOCATION DETAILS =================
    address_type = models.CharField(max_length=20, choices=[('City', 'City'), ('Village', 'Village')], blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    taluka = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    block_number = models.CharField(max_length=100, blank=True, null=True)
    society = models.CharField(max_length=200, blank=True, null=True)
    landmark = models.CharField(max_length=200, blank=True, null=True)
    area = models.CharField(max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    native = models.CharField(max_length=100, blank=True, null=True)

    # ================= 4. PROFESSION & FINANCE =================
    occupation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    account_holder_name = models.CharField(max_length=150, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    branch_name = models.CharField(max_length=150, blank=True, null=True)
    upi_id = models.CharField(max_length=150, blank=True, null=True)
    upi_name = models.CharField(max_length=150, blank=True, null=True)

    # ================= 5. IDENTITY & LEGACY =================
    aadhar_card_number = models.CharField(max_length=12, blank=True, null=True)
    pan_card_number = models.CharField(max_length=10, blank=True, null=True)
    goatra = models.CharField(max_length=100, blank=True, null=True)
    relationship_title = models.CharField(max_length=100, blank=True, null=True)
    
    # Parent Names as Strings
    father_first_name = models.CharField(max_length=100, blank=True, null=True)
    father_middle_name = models.CharField(max_length=100, blank=True, null=True)
    father_last_name = models.CharField(max_length=100, blank=True, null=True)
    mother_first_name = models.CharField(max_length=100, blank=True, null=True)
    mother_middle_name = models.CharField(max_length=100, blank=True, null=True)
    mother_last_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Legacy fields
    kuldevi_name = models.CharField(max_length=150, blank=True, null=True)
    favorite_food = models.CharField(max_length=150, blank=True, null=True)

    # ================= 6. RELATIONSHIPS (Legacy FKs) =================
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_members', null=True, blank=True)
    family_id = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_mother')
    spouse = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='partner')
    generation = models.IntegerField(default=1)

    # ================= 7. SYSTEM =================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.father:
            self.generation = self.father.generation + 1
        elif self.mother:
            self.generation = self.mother.generation + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FamilyUnit(models.Model):
    husband = models.ForeignKey(FamilyMember, related_name='husband_units', on_delete=models.CASCADE, null=True, blank=True)
    wife = models.ForeignKey(FamilyMember, related_name='wife_units', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Unit: {self.husband} & {self.wife}"

class ChildRelation(models.Model):
    child = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='unit_relations')
    family = models.ForeignKey(FamilyUnit, on_delete=models.CASCADE, related_name='child_relations')

    def __str__(self):
        return f"{self.child} in {self.family}"

class FamilyRelationship(models.Model):
    RELATION_TYPES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('spouse', 'Spouse'),
        ('adopted_parent', 'Adopted Parent'),
    ]
    from_person = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='relationships_from')
    to_person = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='relationships_to')
    relation_type = models.CharField(max_length=50, choices=RELATION_TYPES)
    active = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_person} -> {self.relation_type} -> {self.to_person}"

class KuldevDetail(models.Model):
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='kuldev_details', null=True, blank=True)
    dev_type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.dev_type}: {self.name}"

class NivedFood(models.Model):
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='nived_foods', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    food_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.category}: {self.food_name}" if self.category else self.food_name
