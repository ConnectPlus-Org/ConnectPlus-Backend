from rest_framework import serializers, status
from .models import *
from Authentication.utils import CustomValidation
import cloudinary
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        
class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = "__all__"
        
class ShortEducationSerializer(serializers.ModelSerializer):
    school_data = OrganizationSerializer(source = "school", read_only = True)
    
    class Meta:
        model = Education
        fields = ['school_data']
        
class ShortExperienceSerializer(serializers.ModelSerializer):
    company_data = OrganizationSerializer(source = "company", read_only = True)
    
    class Meta:
        model = Experience
        fields = ['company_data']

        
class EducationSerializer(serializers.ModelSerializer):
    
    school_data = OrganizationSerializer(source = "school", read_only = True)
    
    class Meta:
        model = Education
        exclude = ['tagline',]
        extra_kwargs = {'school': {'required': True},}

    def to_representation(self, instance):
       data = super().to_representation(instance)
       data.pop('user')
       return data
   
    def create(self, validated_data):
        try:
            education = super().create(validated_data)
        except IntegrityError:
            raise CustomValidation(detail="End date should be greater than starting date",
                                    field= "error",
                                    status_code=status.HTTP_406_NOT_ACCEPTABLE)
            
        main_profile = MainProfile.objects.update_or_create(profile = validated_data['user'].profile)
        main_profile[0].current_school = Education.objects.filter(user = validated_data['user']).order_by('-start_date')[0]
        main_profile[0].save()
        return education
    
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise CustomValidation(detail="End date should be greater than starting date",
                                    field= "error",
                                    status_code=status.HTTP_406_NOT_ACCEPTABLE)
            
class ExperienceSerializer(serializers.ModelSerializer):
    
    company_data = OrganizationSerializer(source = "company",read_only = True)
    class Meta:
        model = Experience
        exclude = ['tagline']
        extra_kwargs = {'company': {'required': True},
                        'currently_working': {'required': True},}
        
    def validate(self, attrs):
        try:
            if attrs['currently_working'] is True:
                attrs['end_date'] = None
            else:
                try:
                    end_date = attrs['end_date']
                except:
                    raise CustomValidation(detail="If currently_working is False, please provide end date",
                                                field= "error",
                                                status_code=status.HTTP_406_NOT_ACCEPTABLE)
                if attrs[('start_date')] > end_date:
                    raise CustomValidation(detail="End date should be greater than starting date",
                                            field= "error",
                                            status_code=status.HTTP_406_NOT_ACCEPTABLE)
                        
        except KeyError:
            pass
        return super().validate(attrs)
    
    def to_representation(self, instance):
       data = super().to_representation(instance)
       data.pop('user')
       if data['employment_type'] is not None:
          data['employment_type'] = Employment.objects.get(id = data['employment_type']).type
       skills = data['skills']
       for i in range(len(skills)):
            skills[i] = Skill.objects.get(id = skills[i]).skill_name
       data['skills'] = skills
       return data
    
    def create(self, validated_data):
        experience = super().create(validated_data)
        main_profile = MainProfile.objects.update_or_create(profile = validated_data['user'].profile)
        print(Experience.objects.filter(user = validated_data['user']).order_by('-start_date')[0])
        main_profile[0].current_company = Experience.objects.filter(user = validated_data['user']).order_by('-start_date')[0]
        main_profile[0].save()
        return experience
    
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise CustomValidation(detail="End date should be greater than starting date",
                                    field= "error",
                                    status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    
class CourseSerializer(serializers.ModelSerializer):
    organization_data = OrganizationSerializer(source = "organization",read_only = True)
    
    class Meta:
        model = Course
        fields = "__all__"
    
    
class TestScoreSerializer(serializers.ModelSerializer):
    
    organization_data = OrganizationSerializer(source = "organization",read_only = True)
    class Meta:
        model = TestScore
        fields = "__all__"

    
class SkillSerializer(serializers.ModelSerializer):
    
    owner = serializers.SerializerMethodField()
    anonymous = serializers.SerializerMethodField()
    viewer = serializers.SerializerMethodField()
    
    class Meta:
        model = Skill
        fields = "__all__"
        
        
    def get_owner(self, instance):
        return self.context['owner']
    
    def get_anonymous(self, instance):
        return self.context['anonymous']
    
    def get_viewer(self, instance):
        return self.context['viewer']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['endorsement_count'] = len(data.pop('endorsed_by'))
        data['endorsed'] = False
        
        if data['anonymous'] is False and data['owner'] is False:
            profile = Profile.objects.get(user__id = data['viewer'])
            skill = Skill.objects.get(id = data['id'])
            if profile.endorsement.filter(id = skill.id).exists():
                data['endorsed'] = True
        
        experience = []
        for i in instance.experience.all():
            dict = {"tagline":i.tagline, 
                    "organization_logo":cloudinary.CloudinaryImage(f"{i.company.logo}").build_url()}
            experience.append(dict)
        data['experience'] = experience
        return data

    
class ShortProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['avatar', 'headline', 'username',]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ['name'] = instance.full_name
        return data
    
    
class SingleSkillSerializer(serializers.ModelSerializer):
    
    endorsed_by = ShortProfileSerializer(many = True, read_only = True)
    
    class Meta:
        model = Skill
        fields = "__all__"
        
    def to_representation(self, instance):
            data = super().to_representation(instance)
            data['endorsement_count'] = len(data['endorsed_by'])
            experience = []
            for i in instance.experience.all():
                dict = {"tagline":i.tagline, 
                        "organization_logo":cloudinary.CloudinaryImage(f"{i.company.logo}").build_url()}
                experience.append(dict)
            data['experience'] = experience
            return data
        

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        exclude = ['id', 'phone_number','user']
        
class MainProfileSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer(read_only = True)
    current_school = ShortEducationSerializer(read_only = True)
    current_company = ShortExperienceSerializer(read_only = True)
    owner = serializers.SerializerMethodField()
    
    class Meta:
        model = MainProfile
        exclude = ['id']
        
    
    def get_owner(self, instance):
        return self.context['owner']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_viewers_count = len(data.pop(('viewers')))
        if data['owner'] is True:
           data["profile_viewers_count"] = profile_viewers_count
        return data

class ProfileViewersSerializer(serializers.ModelSerializer):
    
    viewer = ShortProfileSerializer(many = False, read_only = True)
    
    class Meta:
        model = ProfileView
        exclude = ['id', 'viewed_profile']
        
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['viewed_time'] = instance.viewed_time.strftime("%Y-%m-%d %H:%M:%S")
        
        return data
        
class EndorsementSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField()
    endorsed_by = ShortProfileSerializer(many = True, read_only = True)
    class Meta:
        model = Skill
        fields = "__all__"
        extra_kwargs = {'id': {'required': True},
                        'skill_name': {'required': False},}

    def validate(self, attrs):
        data = super().validate(attrs)
        skill = get_object_or_404(Skill,id = data['id'])
        if skill.user == data['user']:
            raise CustomValidation(detail="You can't endorse your own Skill",
                                    field= "error",
                                    status_code=status.HTTP_406_NOT_ACCEPTABLE)
        return data

    def create(self, validated_data):
        profile = Profile.objects.get(user = validated_data['user'])
        skill = Skill.objects.get(id = validated_data['id'])
        
        if profile.endorsement.filter(id = skill.id).exists():
            skill.endorsed_by.remove(profile)
        else:
            skill.endorsed_by.add(profile)
        return skill

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['skill_name'] = instance.skill_name
        return data