from rest_framework import serializers, exceptions
from . models import *
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField


class UserList_S(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='HTQL:detail_user',lookup_field='pk')

    class Meta:
        model = CustomUser
        fields = '__all__'
        #fields = '__all__'

class UserDetail_S(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','sub_id','username','position','is_active','phone','address','image','last_login','email','first_name','last_name')
        read_only_fields = ('id','sub_id','username','position','is_active','last_login',)
        #fields = '__all__'

class UserResetPass_S(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','sub_id','username','position','is_active','phone','address','image','last_login','email','first_name','last_name')
        read_only_fields = ('id','sub_id','username','position','last_login',)

class EduProgramList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_eduprogram',lookup_field='pk')
    class Meta:
        model = EduProgram
        fields = '__all__'
        read_only_fields = ('isActive',)
        depth = 2

class EduProgramCreate_S(ModelSerializer):

    # url = HyperlinkedIdentityField(view_name='HTQL:detail_eduprogram',lookup_field='pk')
    class Meta:
        model = EduProgram
        fields = '__all__'
        read_only_fields = ('isActive','image',)

class EduProgramDetail_S(ModelSerializer):

    class Meta:
        model = EduProgram
        fields = '__all__'

class CourseList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_course',lookup_field='pk')
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('isActive',)
        depth = 3

class TeacherCourseList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_course',lookup_field='pk')
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('isActive',)
        depth = 1

class CourseCreate_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_course',lookup_field='pk')
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('isActive','subject',)

class CourseDetail_S(ModelSerializer):

    class Meta:
        model = Course
        fields = ("id","name","fee","image","start_year","end_year","isActive","program_id","subject")
        depth = 2
        read_only_fields = ('isActive',)

class StudyProgramList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_studyprogram',lookup_field='pk')
    class Meta:
        model = StudyProgram
        fields = '__all__'
        read_only_fields = ('student_id','status','isActive',)
        depth = 2

class StudyProgramCreate_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_studyprogram',lookup_field='pk')
    class Meta:
        model = StudyProgram
        fields = '__all__'
        read_only_fields = ('student_id','status','isActive',)

class StudyProgramDetail_S(ModelSerializer):
    class Meta:
        model = StudyProgram
        fields = '__all__'
        read_only_fields = ('status',)
        depth = 2

class Manager_StudyProgramList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:manager_detail_studyprogram',lookup_field='pk')
    class Meta:
        model = StudyProgram
        fields = '__all__'
        #read_only_fields = ('student_id','status','i',)
        depth = 2

class Manager_StudyProgramDetail_S(ModelSerializer):
    class Meta:
        model = StudyProgram
        fields = '__all__'
        read_only_fields = ('student_id','course_id','isActive',)
        depth = 2

class ClassList_S(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='HTQL:detail_class',lookup_field='pk')
    class Meta:
        model = ClassList
        fields = '__all__'
        depth = 3

class ClassDetail_S(ModelSerializer):
    class Meta:
        model = ClassList
        fields = '__all__'
        read_only_fields = ('subject','studyprogram','year','course',)

class SubjectList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_subject',lookup_field='pk')
    class Meta:
        model = Subject
        fields = '__all__'
        depth = 2

class SubjectCreate_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_subject',lookup_field='pk')
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectDetail_S(ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id','name','credit','teacher_id','program_id')
        depth = 2

class ScheduleList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_schedule',lookup_field='pk')
    class Meta:
        model = Schedule
        fields = '__all__'
        depth = 2

class ScheduleCreate_S(ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleDetail_S(ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'
        depth = 2


class DepartmentList_S(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:detail_department',lookup_field='pk')
    class Meta:
        model = Department
        fields = '__all__'
        #read_only_fields = ('isActive',)
        #depth = 2

class DepartmentCreate_S(ModelSerializer):

    # url = HyperlinkedIdentityField(view_name='HTQL:detail_eduprogram',lookup_field='pk')
    class Meta:
        model = Department
        fields = '__all__'
        #read_only_fields = ('isActive','image',)

class DepartmentDetail_S(ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'

class SubScoreList_S(ModelSerializer):

    # url = HyperlinkedIdentityField(view_name='HTQL:detail_eduprogram',lookup_field='pk')
    class Meta:
        model = Sub_Score
        fields = '__all__'
        depth = 2
        #read_only_fields = ('isActive','image',)

class SubScoreDetail_S(ModelSerializer):

    class Meta:
        model = Sub_Score
        fields = '__all__'
        depth = 2

class TranscriptList_S(ModelSerializer):

    # url = HyperlinkedIdentityField(view_name='HTQL:detail_eduprogram',lookup_field='pk')
    class Meta:
        model = Transcript
        fields = '__all__'
        depth = 2
        #read_only_fields = ('isActive','image',)

class TranscriptDetail_S(ModelSerializer):

    class Meta:
        model = Transcript
        fields = '__all__'
        depth = 2



#******************************Test Depth*******************************
class ProgramGet(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='HTQL:test_eduprogram',lookup_field='pk')
    class Meta:
        model = EduProgram
        fields = '__all__'
        read_only_fields = ('isActive',)
        depth = 2

class ProgramPOST(ModelSerializer):

    # url = HyperlinkedIdentityField(view_name='HTQL:detail_eduprogram',lookup_field='pk')
    class Meta:
        model = EduProgram
        fields = ('teacher_id','name')
        read_only_fields = ('isActive',)


#******************************create part******************************
class UserCreate_S(ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username','password','email','position')
    

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        position = validated_data['position']

        next_id = ''
        if(position == 'teacher'):
            user = CustomUser.objects.filter(sub_id__contains='gv')
            if user.count() > 0:
                lastest = user.last()
                next_id = str(int(lastest.sub_id[2:]) + 1)
                while(len(next_id) < 4):
                    next_id = '0'+next_id
                next_id = 'gv'+next_id
            else:
                next_id = 'gv0001'

        elif(position == 'student'):
            user = CustomUser.objects.filter(sub_id__contains='sv')
            if user.count() > 0:
                lastest = user.last()
                next_id = str(int(lastest.sub_id[2:]) + 1)
                while(len(next_id) < 6):
                    next_id = '0'+next_id
                next_id = 'sv'+next_id
            else:
                next_id = 'sv000001'

        user_obj = CustomUser(username = username, email = email, position=position, sub_id=next_id)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class StudentCreate_S(ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username','password','email')
    

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        #position = validated_data['position']

        next_id = ''
        user = CustomUser.objects.filter(sub_id__contains='sv')
        if user.count() > 0:
            lastest = user.last()
            next_id = str(int(lastest.sub_id[2:]) + 1)
            while(len(next_id) < 6):
                next_id = '0'+next_id
            next_id = 'sv'+next_id
        else:
            next_id = 'sv000001'

        user_obj = CustomUser(username = username, email = email, position='student', sub_id=next_id)
        user_obj.set_password(password)
        user_obj.save()
        # ts = Transcript.objects.create(student_id = user_obj)
        # ts.save()
        return validated_data

# class CreateStudent_S(ModelSerializer):
#     user = CustomUser.objects.filter(sub_id__contains='sv')
#     if user.count() > 0:
#         lastest = user.last()
#         next_id = str(int(lastest.sub_id[2:]) + 1)
#         while(len(next_id) < 6):
#             next_id = '0'+next_id
#         next_id = 'sv'+next_id
#     else:
#         next_id = 'sv000001'
#     student = CustomUser(username=next_id, sub_id=next_id,position='sinhvien')
#     student.set_password('ct245')
#     student.save()