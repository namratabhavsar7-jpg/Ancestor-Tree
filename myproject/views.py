from django.shortcuts import render, redirect

from .models import FamilyMember


# ================= HOME PAGE =================

def home(request):

    return render(request, 'home.html')


# ================= ABOUT PAGE =================

def about(request):

    return render(request, 'about.html')

#===================personal info =============
def personal_info(request):
    success = request.GET.get('success')

    if request.method == 'POST':
        FamilyMember.objects.create(
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            religion=request.POST.get('religion'),
            nationality=request.POST.get('nationality'),
            goatra=request.POST.get('goatra'),
            relationship_title=request.POST.get('relationship_title'),
            gender=request.POST.get('gender'),
            height=request.POST.get('height') or None,
            weight=request.POST.get('weight') or None,
            photo=request.FILES.get('photo'),
        )
        return redirect('/personal_info/?success=true')

    return render(request, 'personal_info.html', {'success': success})

#===================contact info =============
def contact_info(request):
    success = request.GET.get('success')
    if request.method == 'POST':
        FamilyMember.objects.create(
            contact_number_1=request.POST.get('contact_number_1'),
            contact_number_2=request.POST.get('contact_number_2'),
            whatsapp_number=request.POST.get('whatsapp_number'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            current_address=request.POST.get('current_address'),
        )
        return redirect('/contact-info/?success=true')
    return render(request, 'contact_info.html', {'success': success})

#===================address details =============
def address_details(request):
    success = request.GET.get('success')
    if request.method == 'POST':
        FamilyMember.objects.create(
            native=request.POST.get('native'),
            village=request.POST.get('village'),
            city=request.POST.get('city'),
            taluka=request.POST.get('taluka'),
            district=request.POST.get('district'),
            pincode=request.POST.get('pincode'),
        )
        return redirect('/address-details/?success=true')
    return render(request, 'address_info.html', {'success': success})

#===================bank details =============
def bank_details(request):
    success = request.GET.get('success')
    if request.method == 'POST':
        FamilyMember.objects.create(
            bank_name=request.POST.get('bank_name'),
            account_holder_name=request.POST.get('account_holder_name'),
            account_number=request.POST.get('account_number'),
            ifsc_code=request.POST.get('ifsc_code'),
            branch_name=request.POST.get('branch_name'),
        )
        return redirect('/bank-details/?success=true')
    return render(request, 'bank_details.html', {'success': success})

#===================upi details =============
def upi_details(request):
    success = request.GET.get('success')
    if request.method == 'POST':
        FamilyMember.objects.create(
            upi_id=request.POST.get('upi_id'),
            upi_name=request.POST.get('upi_name'),
        )
        return redirect('/upi-details/?success=true')
    return render(request, 'upi_details.html', {'success': success})

# ================= FORM PAGE =================

def form_page(request):

    success = request.GET.get('success')

    if request.method == 'POST':

        FamilyMember.objects.create(

            # ================= PERSONAL DETAILS =================

            first_name=request.POST.get('first_name'),

            middle_name=request.POST.get('middle_name'),

            last_name=request.POST.get('last_name'),

            religion=request.POST.get('religion'),

            nationality=request.POST.get('nationality'),

            goatra=request.POST.get('goatra'),

            relationship_title=request.POST.get(
                'relationship_title'
            ),

            gender=request.POST.get('gender'),

            height=request.POST.get('height') or None,

            weight=request.POST.get('weight') or None,

            photo=request.FILES.get('photo'),

            # ================= CONTACT DETAILS =================

            contact_number_1=request.POST.get(
                'contact_number_1'
            ),

            contact_number_2=request.POST.get(
                'contact_number_2'
            ),

            whatsapp_number=request.POST.get(
                'whatsapp_number'
            ),

            email=request.POST.get('email'),

            address=request.POST.get('address'),

            current_address=request.POST.get(
                'current_address'
            ),

            # ================= LOCATION DETAILS =================

            native=request.POST.get('native'),

            village=request.POST.get('village'),

            city=request.POST.get('city'),

            taluka=request.POST.get('taluka'),

            district=request.POST.get('district'),

            pincode=request.POST.get('pincode'),

            # ================= JOB DETAILS =================

            occupation=request.POST.get('occupation'),

            job_type=request.POST.get('job_type'),

            division=request.POST.get('division'),

            monthly_income=request.POST.get(
                'monthly_income'
            ) or None,

            property_value=request.POST.get(
                'property_value'
            ) or None,

            # ================= BANK DETAILS =================

            bank_name=request.POST.get('bank_name'),

            account_holder_name=request.POST.get(
                'account_holder_name'
            ),

            account_number=request.POST.get(
                'account_number'
            ),

            ifsc_code=request.POST.get('ifsc_code'),

            branch_name=request.POST.get('branch_name'),

            # ================= UPI DETAILS =================

            upi_id=request.POST.get('upi_id'),

            upi_name=request.POST.get('upi_name'),

            # ================= IDENTITY DETAILS =================

            aadhar_card_number=request.POST.get(
                'aadhar_card_number'
            ),

            pan_card_number=request.POST.get(
                'pan_card_number'
            ),

        )

        return redirect('/form/?success=true')

    return render(

        request,

        'form.html',

        {

            'success': success

        }

    )