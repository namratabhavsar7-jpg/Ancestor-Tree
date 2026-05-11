from django.db import models


class FamilyMember(models.Model):

    # ================= PERSONAL DETAILS =================

    first_name = models.CharField(max_length=100, blank=True, null=True)

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    last_name = models.CharField(max_length=100, blank=True, null=True)

    religion = models.CharField(max_length=100, blank=True, null=True)

    nationality = models.CharField(max_length=100, blank=True, null=True)

    goatra = models.CharField(max_length=100, blank=True, null=True)

    relationship_title = models.CharField(max_length=100, blank=True, null=True)

    gender = models.CharField(max_length=20, blank=True, null=True)
    other_gender = models.CharField(max_length=100, blank=True, null=True)

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='family_members/',
        blank=True,
        null=True
    )

    # ================= CONTACT DETAILS =================

    contact_number_1 = models.CharField(max_length=15, blank=True, null=True)

    contact_number_2 = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(blank=True, null=True)

    current_address = models.TextField(blank=True, null=True)

    # ================= LOCATION DETAILS =================

    address_type = models.CharField(max_length=20, choices=[('City', 'City'), ('Village', 'Village')], blank=True, null=True)

    state = models.CharField(max_length=100, blank=True, null=True)

    district = models.CharField(max_length=100, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)

    taluka = models.CharField(max_length=100, blank=True, null=True)

    village = models.CharField(max_length=100, blank=True, null=True)

    block_number = models.CharField(max_length=100, blank=True, null=True)

    society = models.CharField(max_length=200, blank=True, null=True)

    landmark = models.CharField(max_length=200, blank=True, null=True)

    area = models.CharField(max_length=150, blank=True, null=True)

    pincode = models.CharField(max_length=10, blank=True, null=True)

    native = models.CharField(max_length=100, blank=True, null=True)

    # ================= JOB DETAILS =================

    occupation = models.CharField(max_length=100, blank=True, null=True)

    job_type = models.CharField(max_length=50, blank=True, null=True)

    division = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    property_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    # ================= BANK DETAILS =================

    bank_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    account_holder_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    branch_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # ================= UPI DETAILS =================

    upi_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    upi_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # ================= IDENTITY DETAILS =================

    aadhar_card_number = models.CharField(max_length=12, blank=True, null=True)

    pan_card_number = models.CharField(max_length=10, blank=True, null=True)

    # ================= NIVED DETAILS =================

    kuldevi_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    favorite_food = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # ================= RELATIONSHIPS =================

    father = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_as_father'
    )

    mother = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_as_mother'
    )

    spouse = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner'
    )

    # ================= SYSTEM =================

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # ================= MODEL NAME =================

    def __str__(self):

        return f"{self.first_name} {self.last_name}"

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