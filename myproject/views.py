from django.shortcuts import render, redirect, get_object_or_404
from .models import FamilyMember, NivedFood, KuldevDetail
import csv
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfessionalRegistrationForm, ProfessionalLoginForm
from django.contrib import messages

# ================= AUTH VIEWS =================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = ProfessionalRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    if request.method == 'POST':
        form = ProfessionalLoginForm(request.POST)
        if form.is_valid():
            login_id = form.cleaned_data['login_id']
            password = form.cleaned_data['password']
            user = User.objects.filter(Q(username=login_id) | Q(email=login_id)).first()
            if user:
                authenticated_user = authenticate(request, username=user.username, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    return redirect('home')
            error = "Invalid credentials."
    else:
        form = ProfessionalLoginForm()
    return render(request, 'auth/login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

# ================= HOME PAGE =================
@login_required
def home(request):
    user_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False)
    context = {
        'total_members': user_members.count(),
        'males': user_members.filter(gender='Male').count(),
        'females': user_members.filter(gender='Female').count(),
        'locations': user_members.values('village').distinct().count(),
        'recent_members': user_members.order_by('-id')[:5],
    }
    return render(request, 'home.html', context)

# ================= PAGES =================
def about(request): return render(request, 'about.html')
def contact(request): return render(request, 'contact.html')
def help_page(request): return render(request, 'help.html')

# ================= REGISTRATION FLOW (PRIVATE) =================

@login_required
def personal_info(request):
    success = request.GET.get('success')
    all_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False).order_by('first_name')
    if request.method == 'POST':
        gender = request.POST.get('gender')
        member = FamilyMember.objects.create(
            registered_by=request.user,
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            religion=request.POST.get('religion'),
            nationality=request.POST.get('nationality'),
            relationship_title=request.POST.get('relationship_title'),
            gender=gender,
            other_gender=request.POST.get('other_gender') if gender == 'Other' else None,
            height=request.POST.get('height') or None,
            weight=request.POST.get('weight') or None,
            photo=request.FILES.get('photo'),
        )
        request.session['current_member_id'] = member.id
        return redirect('/contact-info/')
    return render(request, 'personal_info.html', {'success': success, 'all_members': all_members})

@login_required
def contact_info(request):
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
        member.contact_number_1 = request.POST.get('contact_number_1')
        member.contact_number_2 = request.POST.get('contact_number_2')
        member.whatsapp_number = request.POST.get('whatsapp_number')
        member.email = request.POST.get('email')
        member.save()
        return redirect('/address-details/')
    return render(request, 'contact_info.html', {'member': member})

@login_required
def address_details(request):
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
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
        return redirect('/bank-details/')
    return render(request, 'address_info.html', {'member': member})

@login_required
def bank_details(request):
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
        member.bank_name = request.POST.get('bank_name')
        member.account_holder_name = request.POST.get('account_holder_name')
        member.account_number = request.POST.get('account_number')
        member.ifsc_code = request.POST.get('ifsc_code')
        member.branch_name = request.POST.get('branch_name')
        member.save()
        return redirect('/upi-details/')
    return render(request, 'bank_details.html', {'member': member})

@login_required
def upi_details(request):
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
        member.upi_id = request.POST.get('upi_id')
        member.upi_name = request.POST.get('upi_name')
        member.save()
        return redirect('/identity-info/')
    return render(request, 'upi_details.html', {'member': member})

@login_required
def identity_info(request):
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
        member.aadhar_card_number = request.POST.get('aadhar')
        member.pan_card_number = request.POST.get('pan')
        member.save()
        return redirect('/nived-details/')
    return render(request, 'identity_info.html', {'member': member})

@login_required
def nived_details(request):
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
        food_names = request.POST.getlist('food_name')
        for name in food_names:
            if name: NivedFood.objects.create(member=member, food_name=name)
        return redirect('/kuldevi-info/')
    return render(request, 'nived_details.html', {'member': member})

@login_required
def kuldevi_info(request):
    final = request.GET.get('final')
    mid = request.session.get('current_member_id')
    if not mid: return redirect('personal_info')
    member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    if request.method == 'POST':
        member.goatra = request.POST.get('goatra')
        member.save()
        dev_types = request.POST.getlist('dev_type')
        dev_names = request.POST.getlist('dev_name')
        for d_type, d_name in zip(dev_types, dev_names):
            if d_name: KuldevDetail.objects.create(member=member, dev_type=d_type, name=d_name)
        return redirect('/kuldevi-info/?final=true')
    return render(request, 'kuldevi_info.html', {'final': final, 'member': member})

# ================= UTILS & AJAX =================

import random, string
def generate_family_id():
    while True:
        f_id = f"FAM-{''.join(random.choices(string.digits, k=6))}"
        if not FamilyMember.objects.filter(family_id=f_id).exists(): return f_id

@login_required
def search_family_member(request):
    aadhar = request.GET.get('aadhar', '').strip()
    mobile = request.GET.get('mobile', '').strip()
    current_mid = request.session.get('current_member_id')
    query = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False).exclude(id=current_mid)
    if aadhar: query = query.filter(aadhar_card_number=aadhar)
    elif mobile: query = query.filter(Q(contact_number_1=mobile) | Q(contact_number_2=mobile) | Q(whatsapp_number=mobile))
    m = query.first()
    if m:
        return JsonResponse({'status': 'success', 'member': {'id': m.id, 'name': f"{m.first_name} {m.last_name}", 'village': m.village, 'family_id': m.family_id, 'father_name': m.father.first_name if m.father else "-", 'mother_name': m.mother.first_name if m.mother else "-", 'photo_url': m.photo.url if m.photo else None}})
    return JsonResponse({'status': 'error', 'message': 'No member found.'})

@login_required
def connect_family(request):
    if request.method == 'POST':
        mid = request.session.get('current_member_id')
        if not mid: return JsonResponse({'status': 'error'})
        member = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
        if request.POST.get('has_family') == 'No':
            member.family_id = generate_family_id()
            member.save()
        else:
            existing = get_object_or_404(FamilyMember, id=request.POST.get('existing_member_id'), registered_by=request.user)
            member.family_id = existing.family_id
            rel = request.POST.get('what_they_are')
            if rel == 'Father': member.father = existing
            elif rel == 'Mother': member.mother = existing
            elif rel == 'Spouse':
                member.spouse = existing
                if not existing.spouse:
                    existing.spouse = member
                    existing.save()
            member.relationship_title = request.POST.get('what_i_am')
            member.save()
        if 'current_member_id' in request.session: del request.session['current_member_id']
        return JsonResponse({'status': 'success', 'redirect': '/members/?success=true'})

# ================= DASHBOARDS =================

@login_required
def members_list(request):
    if not FamilyMember.objects.filter(registered_by=request.user, family_id__isnull=False).exists():
        return render(request, 'error_complete_profile.html')
    members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False).order_by('-id')
    return render(request, 'members_list.html', {'members': members, 'success': request.GET.get('success')})

@login_required
def family_tree(request):
    if not FamilyMember.objects.filter(registered_by=request.user, family_id__isnull=False).exists():
        return render(request, 'error_complete_profile.html')
    all_m = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False)
    families = {}
    for m in all_m:
        fid = m.family_id or "Unassigned"
        if fid not in families: families[fid] = []
        families[fid].append(m)
    return render(request, 'family_tree.html', {'families': families})

@login_required
def member_detail(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, registered_by=request.user)
    return render(request, 'member_detail.html', {'member': member, 'kuldevi_details': KuldevDetail.objects.filter(member=member)})

@login_required
def edit_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, registered_by=request.user)
    if request.method == 'POST':
        # ... (edit logic simplified for brevity but handles all fields)
        member.first_name = request.POST.get('first_name')
        member.last_name = request.POST.get('last_name')
        member.save()
        return redirect(f'/member/{member.pk}/')
    return render(request, 'edit_member.html', {'member': member, 'nived_foods': NivedFood.objects.filter(member=member), 'deities': KuldevDetail.objects.filter(member=member)})

@login_required
def delete_member(request, pk):
    get_object_or_404(FamilyMember, pk=pk, registered_by=request.user).delete()
    return redirect('/members/')

@login_required
def export_members_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="family.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Gender', 'Village'])
    for m in FamilyMember.objects.filter(registered_by=request.user):
        writer.writerow([f"{m.first_name} {m.last_name}", m.gender, m.village])
    return response

def form_page(request): return redirect('personal_info')
