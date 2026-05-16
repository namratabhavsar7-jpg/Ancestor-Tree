from .models import FamilyMember, FamilyRelationship, FamilyUnit, ChildRelation
from django.db.models import Q

class FamilyTreeEngine:
    """
    CONSOLIDATED FAMILY UNIT GRAPH ENGINE
    Implements FamilyUnit-based traversal and graph generation.
    """
    
    @staticmethod
    def create_family_unit(father, mother):
        if not father and not mother: return None
        family = FamilyUnit.objects.filter(husband=father, wife=mother, active=True).first()
        if not family:
            family = FamilyUnit.objects.create(husband=father, wife=mother)
        return family

    @staticmethod
    def add_child(father, mother, child):
        family = FamilyTreeEngine.create_family_unit(father, mother)
        if family:
            ChildRelation.objects.get_or_create(child=child, family=family)

    @staticmethod
    def get_siblings(person):
        child_relation = ChildRelation.objects.filter(child=person).first()
        if not child_relation: return []
        siblings = ChildRelation.objects.filter(family=child_relation.family).exclude(child=person)
        return [x.child for x in siblings]

    @staticmethod
    def get_parents(person):
        relation = ChildRelation.objects.filter(child=person).first()
        if not relation: return []
        family = relation.family
        return [family.husband, family.wife]

    @staticmethod
    def generate_graph_json(center_member=None):
        nodes = []
        links = []
        
        # PERSON NODES
        members = FamilyMember.objects.all()
        for person in members:
            nodes.append({
                "id": f"person_{person.id}",
                "label": f"{person.first_name} {person.last_name}",
                "type": "person",
                "gender": person.gender,
                "photo": person.photo.url if person.photo else None
            })

        # FAMILY UNIT NODES & LINKS
        for family in FamilyUnit.objects.all():
            family_node = f"family_{family.id}"
            nodes.append({
                "id": family_node,
                "label": "Family Unit",
                "type": "family"
            })

            if family.husband:
                links.append({"source": f"person_{family.husband.id}", "target": family_node, "type": "husband"})
            if family.wife:
                links.append({"source": f"person_{family.wife.id}", "target": family_node, "type": "wife"})

            for child_rel in ChildRelation.objects.filter(family=family):
                links.append({"source": family_node, "target": f"person_{child_rel.child.id}", "type": "child"})

        return {"nodes": nodes, "links": links, "center_id": f"person_{center_member.id}" if center_member else None}

class RelationEngine:
    @staticmethod
    def identify(a, b):
        """Universal Relation Identifier (A ka B se kya rishta hai)"""
        if a == b: return "Self"

        # 1. IMMEDIATE BLOOD RELATIONS
        parents = FamilyTreeEngine.get_parents(a)
        if b in parents: return "Parent"
        
        # Check if B is my child
        b_parents = FamilyTreeEngine.get_parents(b)
        if a in b_parents: return "Child"
        
        siblings = FamilyTreeEngine.get_siblings(a)
        if b in siblings:
            return "Brother" if b.gender == 'Male' else "Sister"

        # 2. SPOUSE & IN-LAWS
        if a.spouse == b or b.spouse == a: return "Spouse (Husband/Wife)"
        
        if a.spouse:
            spouse_parents = FamilyTreeEngine.get_parents(a.spouse)
            if b in spouse_parents:
                return "Father-in-law" if b.gender == 'Male' else "Mother-in-law"
            if b in FamilyTreeEngine.get_siblings(a.spouse):
                return "Brother-in-law" if b.gender == 'Male' else "Sister-in-law"

        # 3. UNCLE / AUNT / COUSIN LOGIC
        a_father = a.father
        if a_father:
            f_siblings = FamilyTreeEngine.get_siblings(a_father)
            if b in f_siblings: return "Chacha/Tau" if b.gender == 'Male' else "Bua"
            # Cousins
            b_parents = FamilyTreeEngine.get_parents(b)
            for bp in b_parents:
                if bp and bp in f_siblings: return "Cousin (Paternal)"

        a_mother = a.mother
        if a_mother:
            m_siblings = FamilyTreeEngine.get_siblings(a_mother)
            if b in m_siblings: return "Mama" if b.gender == 'Male' else "Mausi"
            # Cousins
            b_parents = FamilyTreeEngine.get_parents(b)
            for bp in b_parents:
                if bp and bp in m_siblings: return "Cousin (Maternal)"

        # 4. GRANDPARENTS
        for p in parents:
            if p and b in FamilyTreeEngine.get_parents(p):
                return "Grandparent"

        return "Extended Relative"

class RecursiveFamilyMergeEngine:
    @staticmethod
    def auto_merge(member):
        visited = set()
        RecursiveFamilyMergeEngine.merge_graph(member, visited)

    @staticmethod
    def merge_graph(member, visited):
        if member.id in visited: return
        visited.add(member.id)

        # STEP 1 — CONNECT FATHER & CREATE UNIT
        if not member.father and member.father_first_name:
            father = FamilyMember.objects.filter(first_name__iexact=member.father_first_name, village=member.village).first()
            if father:
                member.father = father
                # Discover Mother
                spouse_rel = FamilyUnit.objects.filter(Q(husband=father) | Q(wife=father), active=True).first()
                if spouse_rel:
                    mother = spouse_rel.wife if spouse_rel.husband == father else spouse_rel.husband
                    if not member.mother: member.mother = mother
                
                FamilyTreeEngine.add_child(member.father, member.mother, member)

        # STEP 2 — CONNECT MOTHER & CREATE UNIT
        if not member.mother and member.mother_first_name:
            mother = FamilyMember.objects.filter(first_name__iexact=member.mother_first_name, village=member.village).first()
            if mother:
                member.mother = mother
                # Discover Father
                spouse_rel = FamilyUnit.objects.filter(Q(husband=mother) | Q(wife=mother), active=True).first()
                if spouse_rel:
                    father = spouse_rel.husband if spouse_rel.wife == mother else spouse_rel.wife
                    if not member.father: member.father = father
                
                FamilyTreeEngine.add_child(member.father, member.mother, member)

        member.save()

        # RECURSIVE MERGE
        if member.father: RecursiveFamilyMergeEngine.merge_graph(member.father, visited)
        if member.mother: RecursiveFamilyMergeEngine.merge_graph(member.mother, visited)
        
        children = FamilyMember.objects.filter(Q(father=member) | Q(mother=member))
        for child in children:
            RecursiveFamilyMergeEngine.merge_graph(child, visited)
