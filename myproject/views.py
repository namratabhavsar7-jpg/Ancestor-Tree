from django.shortcuts import render, redirect, get_object_or_404
from .models import FamilyMember, NivedFood, KuldevDetail, FamilyRelationship
from .utils import FamilyTreeEngine
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

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    
    user_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False)
    
    context = {
        'total_members': user_members.count(),
        'males': user_members.filter(gender='Male').count(),
        'females': user_members.filter(gender='Female').count(),
        'locations': user_members.values('village').distinct().count(),
        'recent_members': user_members.order_by('-id')[:5],
        'is_dashboard': True
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
    if request.method == 'POST':
        # Create member with all fields at once (Single Page Flow)
        gender = request.POST.get('gender')
        member = FamilyMember.objects.create(
            registered_by=request.user,
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            date_of_birth=request.POST.get('date_of_birth') or None,
            age=request.POST.get('age') or None,
            is_alive=request.POST.get('is_alive') == 'True',
            religion=request.POST.get('religion'),
            nationality=request.POST.get('nationality'),
            gender=gender,
            other_gender=request.POST.get('other_gender') if gender == 'Other' else None,
            height=request.POST.get('height') or None,
            weight=request.POST.get('weight') or None,
            photo=request.FILES.get('photo'),
            father_first_name=request.POST.get('father_first_name'),
            father_middle_name=request.POST.get('father_middle_name'),
            father_last_name=request.POST.get('father_last_name'),
            mother_first_name=request.POST.get('mother_first_name'),
            mother_middle_name=request.POST.get('mother_middle_name'),
            mother_last_name=request.POST.get('mother_last_name'),
            
            contact_number_1=request.POST.get('contact_number_1'),
            contact_number_2=request.POST.get('contact_number_2'),
            whatsapp_number=request.POST.get('whatsapp_number'),
            email=request.POST.get('email'),
            
            address_type=request.POST.get('address_type'),
            state=request.POST.get('state'),
            district=request.POST.get('district'),
            taluka=request.POST.get('taluka'),
            village=request.POST.get('village'),
            block_number=request.POST.get('block_number'),
            society=request.POST.get('society'),
            landmark=request.POST.get('landmark'),
            area=request.POST.get('area'),
            pincode=request.POST.get('pincode'),
            
            occupation=request.POST.get('occupation'),
            job_type=request.POST.get('job_type'),
            monthly_income=request.POST.get('monthly_income') or None,
            bank_name=request.POST.get('bank_name'),
            account_holder_name=request.POST.get('account_holder_name'),
            account_number=request.POST.get('account_number'),
            ifsc_code=request.POST.get('ifsc_code'),
            branch_name=request.POST.get('branch_name'),
            upi_id=request.POST.get('upi_id'),
            upi_name=request.POST.get('upi_name'),
            
            aadhar_card_number=request.POST.get('aadhar'),
            pan_card_number=request.POST.get('pan'),
            goatra=request.POST.get('goatra')
        )
        
        # Handle Dynamic Rows
        food_names = request.POST.getlist('food_name')
        for name in food_names:
            if name: NivedFood.objects.create(member=member, food_name=name)
            
        dev_types = request.POST.getlist('dev_type')
        dev_names = request.POST.getlist('dev_name')
        for d_type, d_name in zip(dev_types, dev_names):
            if d_name: KuldevDetail.objects.create(member=member, dev_type=d_type, name=d_name)

        # 2. TRIGGER GLOBAL MERGE (AUTO)
        from .utils import RecursiveFamilyMergeEngine
        RecursiveFamilyMergeEngine.auto_merge(member)
        
        # 3. SET SESSION AND REDIRECT TO TRIGGER MODAL
        request.session['current_member_id'] = member.id
        return redirect('/personal-info/?success=true')
    
    # Context for rendering the page
    mid = request.session.get('current_member_id')
    all_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False).order_by('first_name')
    if mid: all_members = all_members.exclude(id=mid)
        
    return render(request, 'personal_info.html', {
        'success': request.GET.get('success'),
        'all_members': all_members
    })

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
    
    # Get all other members registered by this user to show as cards for linking
    all_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False).exclude(id=mid).order_by('first_name')
    
    if request.method == 'POST':
        member.goatra = request.POST.get('goatra')
        member.save()
        dev_types = request.POST.getlist('dev_type')
        dev_names = request.POST.getlist('dev_name')
        for d_type, d_name in zip(dev_types, dev_names):
            if d_name: KuldevDetail.objects.create(member=member, dev_type=d_type, name=d_name)
        return redirect('/kuldevi-info/?final=true')
    return render(request, 'kuldevi_info.html', {'final': final, 'member': member, 'all_members': all_members})

# ================= UTILS & AJAX =================

import random, string
def generate_family_id():
    while True:
        f_id = f"FAM-{''.join(random.choices(string.digits, k=6))}"
        if not FamilyMember.objects.filter(family_id=f_id).exists(): return f_id

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
            rel = request.POST.get('what_they_are') # e.g., "Father" (Existing is my Father)
            
            from .utils import FamilyTreeEngine, RecursiveFamilyMergeEngine
            
            if rel == 'Father':
                member.father = existing
                # Inherit heritage
                member.goatra = existing.goatra
                member.village = existing.village
            
            elif rel == 'Mother':
                member.mother = existing
                member.village = existing.village
            
            elif rel == 'Spouse':
                member.spouse = existing
                if not existing.spouse:
                    existing.spouse = member
                    existing.save()
            
            elif rel == 'Son' or rel == 'Daughter':
                if member.gender == 'Male':
                    existing.father = member
                elif member.gender == 'Female':
                    existing.mother = member
                existing.save()
            
            # Additional logic to handle "I am their Son/Daughter"
            iam = request.POST.get('what_i_am')
            if iam == 'Son' or iam == 'Daughter':
                if existing.gender == 'Male':
                    member.father = existing
                elif existing.gender == 'Female':
                    member.mother = existing
            elif iam == 'Father':
                member.gender = 'Male'
                if existing.gender == 'Male' or existing.gender == 'Female':
                    existing.father = member
            elif iam == 'Mother':
                member.gender = 'Female'
                if existing.gender == 'Male' or existing.gender == 'Female':
                    existing.mother = member

            member.save()
            existing.save()
            
            # Use the Recursive engine to fix the whole graph and family units
            RecursiveFamilyMergeEngine.auto_merge(member)

        if 'current_member_id' in request.session: del request.session['current_member_id']
        return JsonResponse({'status': 'success', 'redirect': '/members/?success=linked'})

@login_required
def search_by_aadhar(request):
    aadhar = request.GET.get('aadhar', '').replace(' ', '').strip()
    mobile = request.GET.get('mobile', '').replace(' ', '').strip()
    
    if not aadhar and not mobile:
        return JsonResponse({'status': 'error', 'message': 'Please provide Aadhaar or Mobile number.'})

    # 1. Search globally across the whole database
    q = Q()
    if aadhar: q |= Q(aadhar_card_number=aadhar)
    if mobile: q |= Q(contact_number_1=mobile) | Q(whatsapp_number=mobile)
    
    main_member = FamilyMember.objects.filter(q).first()
    
    if not main_member:
        return JsonResponse({'status': 'error', 'message': f'No member found matching Aadhaar "{aadhar}" or Mobile "{mobile}".'})

    # 2. Get EVERYONE in their family branch (Global database connectivity)
    family_members = []
    
    # If they have a family_id, get everyone with that ID
    if main_member.family_id:
        branch = FamilyMember.objects.filter(family_id=main_member.family_id).order_by('first_name')
        for m in branch:
            family_members.append({
                'id': m.id,
                'name': f"{m.first_name} {m.last_name}",
                'village': m.village or "N/A",
                'photo': m.photo.url if m.photo else None,
                'is_main': m.id == main_member.id,
                'father': m.father_first_name or "-",
                'mother': m.mother_first_name or "-"
            })
    else:
        # Fallback: Just show the matched person if no family_id yet
        family_members.append({
            'id': main_member.id,
            'name': f"{main_member.first_name} {main_member.last_name}",
            'village': main_member.village or "N/A",
            'photo': main_member.photo.url if main_member.photo else None,
            'is_main': True,
            'father': main_member.father_first_name or "-",
            'mother': main_member.mother_first_name or "-"
        })

    return JsonResponse({
        'status': 'success',
        'family_id': main_member.family_id,
        'members': family_members
    })

# ================= DASHBOARDS =================

@login_required
def members_list(request):
    user_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False)
    members = user_members.order_by('-id')
    current_mid = request.session.get('current_member_id')
    return render(request, 'members_list.html', {
        'members': members, 
        'success': request.GET.get('success'),
        'current_member_id': current_mid
    })

@login_required
def family_tree(request):
    user_members = FamilyMember.objects.filter(registered_by=request.user, first_name__isnull=False)
    families = {}
    for m in user_members:
        fid = m.family_id or "Unassigned"
        if fid not in families: families[fid] = []
        families[fid].append(m)
    return render(request, 'family_tree.html', {'families': families})

@login_required
def get_family_json(request):
    mid = request.GET.get('member_id')
    center_node = None
    if mid:
        center_node = get_object_or_404(FamilyMember, id=mid, registered_by=request.user)
    
    from .utils import FamilyTreeEngine
    # Generate graph using the new Unit-based Engine
    graph_data = FamilyTreeEngine.generate_graph_json(center_member=center_node)
    return JsonResponse(graph_data)

@login_required
def member_detail(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, registered_by=request.user)

    # Resolution using the new RelationEngine
    from .utils import RelationEngine
    dynamic_relations = []
    all_members = FamilyMember.objects.filter(registered_by=request.user)
    for other in all_members:
        if member.id != other.id:
            label = RelationEngine.identify(member, other)
            if label != "Extended Relative":
                dynamic_relations.append({'person': other, 'label': label})

    return render(request, 'member_detail.html', {
        'member': member,
        'kuldevi_details': KuldevDetail.objects.filter(member=member),
        'dynamic_relations': dynamic_relations
    })
@login_required
def edit_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, registered_by=request.user)
    request.session['current_member_id'] = member.id
    if request.method == 'POST':
        member.first_name = request.POST.get('first_name')
        member.middle_name = request.POST.get('middle_name')
        member.last_name = request.POST.get('last_name')
        member.date_of_birth = request.POST.get('date_of_birth') or None
        member.age = request.POST.get('age') or None
        member.is_alive = request.POST.get('is_alive') == 'True'
        member.gender = request.POST.get('gender')
        member.other_gender = request.POST.get('other_gender')
        member.religion = request.POST.get('religion')
        member.nationality = request.POST.get('nationality')
        member.height = request.POST.get('height') or None
        member.weight = request.POST.get('weight') or None
        if request.FILES.get('photo'): member.photo = request.FILES.get('photo')
        
        member.contact_number_1 = request.POST.get('contact_number_1')
        member.contact_number_2 = request.POST.get('contact_number_2')
        member.whatsapp_number = request.POST.get('whatsapp_number')
        member.email = request.POST.get('email')
        
        member.address_type = request.POST.get('address_type')
        member.state = request.POST.get('state')
        member.district = request.POST.get('district')
        member.taluka = request.POST.get('taluka')
        member.village = request.POST.get('village')
        member.city = request.POST.get('city')
        member.block_number = request.POST.get('block_number')
        member.society = request.POST.get('society')
        member.landmark = request.POST.get('landmark')
        member.area = request.POST.get('area')
        member.pincode = request.POST.get('pincode')
        
        member.occupation = request.POST.get('occupation')
        member.job_type = request.POST.get('job_type')
        member.monthly_income = request.POST.get('monthly_income') or None
        member.bank_name = request.POST.get('bank_name')
        member.account_holder_name = request.POST.get('account_holder_name')
        member.account_number = request.POST.get('account_number')
        member.ifsc_code = request.POST.get('ifsc_code')
        member.branch_name = request.POST.get('branch_name')
        member.upi_id = request.POST.get('upi_id')
        member.upi_name = request.POST.get('upi_name')
        
        member.aadhar_card_number = request.POST.get('aadhar')
        member.pan_card_number = request.POST.get('pan')
        member.goatra = request.POST.get('goatra')
        
        member.father_first_name = request.POST.get('father_first_name')
        member.father_middle_name = request.POST.get('father_middle_name')
        member.father_last_name = request.POST.get('father_last_name')
        member.mother_first_name = request.POST.get('mother_first_name')
        member.mother_middle_name = request.POST.get('mother_middle_name')
        member.mother_last_name = request.POST.get('mother_last_name')
        
        member.save()

        # Trigger Global Recursive Merge
        from .utils import RecursiveFamilyMergeEngine
        RecursiveFamilyMergeEngine.auto_merge(member)
        
        # Update dynamic rows (Nived & Deities)
        NivedFood.objects.filter(member=member).delete()
        food_names = request.POST.getlist('food_name')
        for name in food_names:
            if name: NivedFood.objects.create(member=member, food_name=name)
            
        KuldevDetail.objects.filter(member=member).delete()
        dev_types = request.POST.getlist('dev_type')
        dev_names = request.POST.getlist('dev_name')
        for d_type, d_name in zip(dev_types, dev_names):
            if d_name: KuldevDetail.objects.create(member=member, dev_type=d_type, name=d_name)

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
