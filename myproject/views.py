from django.shortcuts import render, redirect, get_object_or_404
from .models import FamilyMember, NivedFood, KuldevDetail
import csv
from django.http import HttpResponse

# ================= HOME PAGE =================
def home(request):
    total_members = FamilyMember.objects.filter(first_name__isnull=False).count()
    males = FamilyMember.objects.filter(gender='Male').count()
    females = FamilyMember.objects.filter(gender='Female').count()
    locations = FamilyMember.objects.values('village').distinct().count()
    recent_members = FamilyMember.objects.filter(first_name__isnull=False).order_by('-id')[:5]

    context = {
        'total_members': total_members,
        'males': males,
        'females': females,
        'locations': locations,
        'recent_members': recent_members,
    }
    return render(request, 'home.html', context)

# ================= ABOUT PAGE =================
def about(request):
    return render(request, 'about.html')

# ================= CONTACT PAGE =================
def contact(request):
    if request.method == 'POST':
        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')

# ================= HELP PAGE =================
def help_page(request):
    return render(request, 'help.html')

#===================personal info (STEP 1: CREATE) =============
def personal_info(request):
    success = request.GET.get('success')
    all_members = FamilyMember.objects.filter(first_name__isnull=False).order_by('first_name')
    
    if request.method == 'POST':
        gender = request.POST.get('gender')
        other_gender = request.POST.get('other_gender') if gender == 'Other' else None
            
        member = FamilyMember.objects.create(
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            religion=request.POST.get('religion'),
            nationality=request.POST.get('nationality'),
            relationship_title=request.POST.get('relationship_title'),
            gender=gender,
            other_gender=other_gender,
            height=request.POST.get('height') or None,
            weight=request.POST.get('weight') or None,
            photo=request.FILES.get('photo'),
            father_id=request.POST.get('father'),
            mother_id=request.POST.get('mother'),
            spouse_id=request.POST.get('spouse'),
        )
        # Store member ID in session for next steps
        request.session['current_member_id'] = member.id
        return redirect('/contact-info/?success=true')
    return render(request, 'personal_info.html', {'success': success, 'all_members': all_members})

#===================contact info (STEP 2: UPDATE) =============
def contact_info(request):
    success = request.GET.get('success')
    member_id = request.session.get('current_member_id')
    
    if not member_id and request.method == 'POST':
        return redirect('personal_info')

    if request.method == 'POST':
        member = get_object_or_404(FamilyMember, id=member_id)
        member.contact_number_1 = request.POST.get('contact_number_1')
        member.contact_number_2 = request.POST.get('contact_number_2')
        member.whatsapp_number = request.POST.get('whatsapp_number')
        member.email = request.POST.get('email')
        member.address = request.POST.get('address')
        member.current_address = request.POST.get('current_address')
        member.save()
        return redirect('/address-details/?success=true')
    return render(request, 'contact_info.html', {'success': success})

#===================address details (STEP 3: UPDATE) =============
def address_details(request):
    success = request.GET.get('success')
    member_id = request.session.get('current_member_id')
    
    if not member_id and request.method == 'POST':
        return redirect('personal_info')

    if request.method == 'POST':
        member = get_object_or_404(FamilyMember, id=member_id)
        member.address_type = request.POST.get('address_type')
        member.state = request.POST.get('state')
        member.district = request.POST.get('district')
        member.taluka = request.POST.get('taluka')
        member.village = request.POST.get('village')
        member.block_number = request.POST.get('block_number')
        member.society = request.POST.get('society')
        member.landmark = request.POST.get('landmark')
        member.city = request.POST.get('city')
        member.area = request.POST.get('area')
        member.pincode = request.POST.get('pincode')
        member.save()
        return redirect('/bank-details/?success=true')
    return render(request, 'address_info.html', {'success': success})

#===================bank details (STEP 4: UPDATE) =============
def bank_details(request):
    success = request.GET.get('success')
    member_id = request.session.get('current_member_id')
    
    if not member_id and request.method == 'POST':
        return redirect('personal_info')

    if request.method == 'POST':
        member = get_object_or_404(FamilyMember, id=member_id)
        member.bank_name = request.POST.get('bank_name')
        member.account_holder_name = request.POST.get('account_holder_name')
        member.account_number = request.POST.get('account_number')
        member.ifsc_code = request.POST.get('ifsc_code')
        member.branch_name = request.POST.get('branch_name')
        member.save()
        return redirect('/upi-details/?success=true')
    return render(request, 'bank_details.html', {'success': success})

#===================upi details (STEP 5: UPDATE) =============
def upi_details(request):
    success = request.GET.get('success')
    member_id = request.session.get('current_member_id')
    
    if not member_id and request.method == 'POST':
        return redirect('personal_info')

    if request.method == 'POST':
        member = get_object_or_404(FamilyMember, id=member_id)
        member.upi_id = request.POST.get('upi_id')
        member.upi_name = request.POST.get('upi_name')
        member.save()
        return redirect('/nived-details/?success=true')
    return render(request, 'upi_details.html', {'success': success})

#===================nived details (STEP 6: LINK) =============
def nived_details(request):
    success = request.GET.get('success')
    member_id = request.session.get('current_member_id')
    
    if request.method == 'POST':
        food_names = request.POST.getlist('food_name')
        member = None
        if member_id:
            member = FamilyMember.objects.filter(id=member_id).first()
            
        for name in food_names:
            if name:
                NivedFood.objects.create(
                    member=member,
                    food_name=name
                )
        return redirect('/kuldevi-info/?success=true')
    return render(request, 'nived_details.html', {'success': success})

#===================kuldevi details (STEP 7: LINK & FINISH) =============
def kuldevi_info(request):
    success = request.GET.get('success')
    member_id = request.session.get('current_member_id')
    
    if request.method == 'POST':
        goatra = request.POST.get('goatra')
        dev_types = request.POST.getlist('dev_type')
        dev_names = request.POST.getlist('dev_name')
        
        # If we have a member in progress, use it. Otherwise create new.
        if member_id:
            member = get_object_or_404(FamilyMember, id=member_id)
            member.goatra = goatra
            member.save()
        else:
            member = FamilyMember.objects.create(goatra=goatra)
            
        # Save Kuldevi/Kuldev entries linked to the member
        for d_type, d_name in zip(dev_types, dev_names):
            if d_name:
                KuldevDetail.objects.create(member=member, dev_type=d_type, name=d_name)
        
        # CLEAR SESSION AFTER COMPLETION
        if 'current_member_id' in request.session:
            del request.session['current_member_id']
            
        return redirect('/members/?success=true')
    return render(request, 'kuldevi_info.html', {'success': success})

#=================== members list =============
def members_list(request):
    success = request.GET.get('success')
    members = FamilyMember.objects.filter(first_name__isnull=False).order_by('-id')
    return render(request, 'members_list.html', {'members': members, 'success': success})

#=================== family tree =============
def family_tree(request):
    members = FamilyMember.objects.filter(first_name__isnull=False)
    return render(request, 'family_tree.html', {'members': members})

#=================== member detail =============
def member_detail(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    kuldevi_details = KuldevDetail.objects.filter(member=member)
    return render(request, 'member_detail.html', {
        'member': member,
        'kuldevi_details': kuldevi_details
    })

#=================== edit member =============
def edit_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        # Personal
        member.first_name = request.POST.get('first_name')
        member.last_name = request.POST.get('last_name')
        member.gender = request.POST.get('gender')
        member.goatra = request.POST.get('goatra')
        # Contact
        member.contact_number_1 = request.POST.get('contact_number_1')
        member.whatsapp_number = request.POST.get('whatsapp_number')
        member.email = request.POST.get('email')
        # Location
        member.state = request.POST.get('state')
        member.district = request.POST.get('district')
        member.village = request.POST.get('village')
        member.pincode = request.POST.get('pincode')
        # Finance
        member.bank_name = request.POST.get('bank_name')
        member.account_number = request.POST.get('account_number')
        member.upi_id = request.POST.get('upi_id')
        
        if request.FILES.get('photo'):
            member.photo = request.FILES.get('photo')
            
        member.save()
        return redirect(f'/member/{member.pk}/?success=updated')
    return render(request, 'edit_member.html', {'member': member})

#=================== delete member =============
def delete_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    member.delete()
    return redirect('/members/?success=deleted')

#=================== export CSV =============
def export_members_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="family_members.csv"'
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Relationship', 'Gender', 'Goatra', 'Contact', 'State', 'District', 'City/Village'])
    members = FamilyMember.objects.filter(first_name__isnull=False)
    for m in members:
        writer.writerow([m.first_name, m.last_name, m.relationship_title, m.gender, m.goatra, m.contact_number_1, m.state, m.district, m.village])
    return response

# ================= OLD FORM PAGE (Legacy) =================
def form_page(request):
    return redirect('personal_info')
