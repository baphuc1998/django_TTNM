from django.shortcuts import render
from . serializers import *
from rest_framework import generics, mixins
from .models import *
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max, Sum, Avg, F, Q
from .patigations import *
from datetime import datetime, timedelta


class UserListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserList_S
    permission_classes = (permissions.IsAuthenticated,IsAdmin,)
    pagination_class = Patigation_10_item
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    search_fields   = ['position']

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

class UserProfileAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserList_S
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetail_S
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrAdmin,)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        obj = CustomUser.objects.get(id=pk)
        obj.is_active = False
        obj.save()
        raise exceptions.ValidationError("You deleted this item") 

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreate_S
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdmin,)

class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentCreate_S
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,Pms_Register,)

class TeacherListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserList_S
    permission_classes = (permissions.IsAuthenticated,IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(is_active=True, position='teacher')

class EduProgramListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = EduProgram.objects.all()
    serializer_class = EduProgramList_S
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return self.queryset.all()

class EduProgramCreateView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = EduProgram.objects.all()
    serializer_class = EduProgramCreate_S
    permission_classes = (IsAdmin,)

    def post(self, request):
        return self.create(request)

class EduProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EduProgram.objects.all()
    serializer_class = EduProgramDetail_S
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrAdmin_EducationProgram,)

    def put(self, request, pk=None):
        return self.update(request, pk)

    # def delete(self, request, pk=None):
    #     obj = EduProgram.objects.get(id=pk)
    #     # obj.save()
    #     raise exceptions.ValidationError("You deleted this item") 

class CourseListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Course.objects.all()
    serializer_class = CourseList_S
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.order_by('-id')

class CourseCreateView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Course.objects.all()
    serializer_class = CourseCreate_S
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,CanCreateOrNot,)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        obj = serializer.save()
        subjects = Subject.objects.filter(program_id = obj.program_id)
        serializer.save(subject = subjects)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetail_S
    permission_classes = (permissions.AllowAny,CanCreateOrNot,)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def partial_update(self, request, *args, **kwargs):   
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class TeacherCourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = TeacherCourseList_S
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        dpt = Department.objects.filter(teacher = self.request.user).first()
        return self.queryset.filter(program_id = dpt.eduprogram, end_year__gte=datetime.now()-timedelta(days=1))


class StudyProgramListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramList_S
    permission_classes = (permissions.IsAuthenticated,IsStudentOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('isActive','status',)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(student_id= self.request.user)

class SPListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramList_S
    permission_classes = (permissions.IsAuthenticated,IsStudentOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('isActive','status',)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(student_id=self.request.user, status='registered')

class StudyProgramCreateView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramCreate_S
    permission_classes = (permissions.IsAuthenticated,IsStudentOrAdmin,)

    # def get_queryset(self):
    #     return self.queryset.all()

    def post(self, request):
        _course = request.data['course_id']
        _course = Course.objects.get(id=_course)
        if StudyProgram.objects.filter(course_id=_course, student_id=request.user).count() > 0:
            return Response("You can not register this course second time")
        StudyProgram.objects.create(student_id=request.user, course_id=_course, status='liked', isActive=False)
        return Response("Successful", status=status.HTTP_200_OK)

class StudyProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramDetail_S
    permission_classes = (permissions.IsAuthenticated,StudentUpdateStup,)

    # def put(self, request, pk=None):
    #     obj = self.get_object()
    #     _status = request.data['status']
    #     obj.status = _status
    #     obj.save()
    #     user = obj.student_id
        
    #     if obj.status == "registered":
    #         if ClassList.objects.filter(studyprogram__student_id= user, course=obj.course_id).count() < 1:
    #             if Transcript.objects.filter(student_id=user, studyprogram_id= obj).count() > 0:
    #                 return Response("Can not register this course", status=status.HTTP_400_BAD_REQUEST)
    #             Transcript.objects.create(student_id=user, studyprogram_id= obj)
    #             for subject in obj.course_id.subject.all():
    #                 ClassList.objects.create(studyprogram=obj,subject=subject,year=obj.course_id.start_year, course = obj.course_id )
    #         else:
    #             return Response("Can not register this course", status=status.HTTP_400_BAD_REQUEST)
        #return self.update(request, pk)

    def partial_update(self, request, *args, **kwargs):   
        kwargs['partial'] = True
        obj = self.get_object()
        try:
            _status = request.data['status']
            if _status == 'paused':
                obj.status = 'paused'
                obj.save()
                return Response("The course has been suspended", status=status.HTTP_200_OK)
            else:
                pass
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
        return self.update(request, *args, **kwargs)

class ManagerStudyProgramListView(generics.ListAPIView ):
    queryset = StudyProgram.objects.all()
    serializer_class = Manager_StudyProgramList_S
    permission_classes = (permissions.IsAuthenticated,IsAdminOrManager)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status','isActive',)

    def get_queryset(self):
        return self.queryset.all().order_by("-id")

class ManagerStudyProgramDetailView(generics.RetrieveUpdateDestroyAPIView ):
    queryset = StudyProgram.objects.all()
    serializer_class = Manager_StudyProgramDetail_S
    permission_classes = (permissions.IsAuthenticated,CanUpdateStup,)
    
    #def put(self, request, pk=None):
    def partial_update(self, request, *args, **kwargs):   
        kwargs['partial'] = True

        obj = self.get_object()
        _status = request.data['status']
        obj.status = _status
        obj.isActive = True
        obj.save()
        user = obj.student_id
        stups = StudyProgram.objects.filter(~Q(id=obj.id), student_id=user)
        if obj.status == "registered":
            for stup in stups:
                stup.status = "paused"
                stup.save()
        
        if obj.status == "registered":
            if ClassList.objects.filter(studyprogram__student_id= user, course=obj.course_id).count() < 1:
                if Transcript.objects.filter(student_id=user, studyprogram_id= obj).count() > 0:
                    return Response("successful", status=status.HTTP_200_OK)
                Transcript.objects.create(student_id_id=user.id, studyprogram_id= obj)
                for subject in obj.course_id.subject.all():
                    ClassList.objects.create(studyprogram=obj,subject=subject,year=obj.course_id.start_year, course = obj.course_id )
                    Sub_Score.objects.create(subject_id=subject,studyprogram_id=obj)
            else:
                return Response("successful", status=status.HTTP_200_OK)

        return Response("successful", status=status.HTTP_200_OK)
    
class ClassListView(generics.ListAPIView):
    queryset = ClassList.objects.all()
    serializer_class = ClassList_S
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends =  (DjangoFilterBackend,)
    filter_fields = ('subject','course',)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        elif self.request.user.position == "teacher":
            try:
                return self.queryset.filter(subject__teacher_id = self.request.user, course__program_id = self.request.user.dpt_in_teacher.first().eduprogram )
            except:
                return None
        else:
            return self.queryset.filter(studyprogram__student_id = self.request.user)

class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassList.objects.all()
    serializer_class = ClassDetail_S
    permission_classes = (permissions.IsAuthenticated, CanUpdateScore,)

    def update(self, request, pk=None):
        obj = self.get_object()
        _score = request.data['score']
        obj.score = _score
        obj.save()
        if Sub_Score.objects.filter(subject_id= obj.subject, studyprogram_id= obj.studyprogram).count() > 0:
            subscore = Sub_Score.objects.filter(subject_id= obj.subject, studyprogram_id= obj.studyprogram).first()
            subscore.score = _score
            subscore.save()
            gpa = Sub_Score.objects.filter(studyprogram_id= obj.studyprogram).aggregate(Avg('score'))
            Transcript.objects.filter(studyprogram_id=obj.studyprogram).update(GPA= gpa['score__avg'])
            if gpa['score__avg'] > 5 and not subscore.is_completed:
                subscore.is_completed = True
                subscore.save()
                Transcript.objects.filter(studyprogram_id=obj.studyprogram).update(accumutation=F('accumutation')+obj.subject.credit)
        else:
            subscore = Sub_Score.objects.create(subject_id= obj.subject, score= obj.score, studyprogram_id= obj.studyprogram)
            subscore.save()
            gpa = Sub_Score.objects.filter(studyprogram_id= obj.studyprogram).aggregate(Avg('score'))
            Transcript.objects.filter(studyprogram_id=obj.studyprogram).update(GPA= gpa['score__avg'])
            if gpa['score__avg'] > 5 and not subscore.is_completed:
                subscore.is_completed = True
                subscore.save()
                Transcript.objects.filter(studyprogram_id=obj.studyprogram).update(accumutation=F('accumutation')+obj.subject.credit)
        return Response("Successful",status=status.HTTP_200_OK)

class SubjectListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Subject.objects.all()
    serializer_class = SubjectList_S
    #permission_classes = (IsAdmin,)
    pagination_class = Patigation_10_item
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('program_id',)

    def get_queryset(self):
        return self.queryset.all()

    # def post(self, request):
    #     return self.create(request)

class SubjectofTeacherList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectList_S
    pagination_class = Patigation_10_item
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(teacher_id=self.request.user)

class SubjectCreateView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Subject.objects.all()
    serializer_class = SubjectCreate_S
    permission_classes = (permissions.IsAuthenticated,IsAdmin,)

    # def get_queryset(self):
    #     return self.queryset.all()

    def post(self, request):
        return self.create(request)

class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectDetail_S
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrAdmin,)

    def put(self, request, pk=None):
        try:
            print(request.data['program_id'])
            prg = request.data['program_id']
            obj = self.get_object()
            obj.program_id.set(prg)
            obj.save()
        except:
            pass
        return self.update(request, pk)

    # def perform_update(self, serializer):
    #     serializer.save()

    # def delete(self, request, pk=None):
    #     obj = Subject.objects.get(id=pk)
    #     obj.save()
    #     raise exceptions.ValidationError("You deleted this item") 


class ScheduleListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleList_S
    permission_classes = (permissions.IsAuthenticated,CanPostSchedule ,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('course',)

    def get_queryset(self):
        return self.queryset.all()

    def post(self, request):
        return self.create(request)

class ScheduleCreateView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleCreate_S
    permission_classes = (permissions.IsAuthenticated,IsAdmin,)

    # def get_queryset(self):
    #     return self.queryset.all()

    def post(self, request):
        return self.create(request)

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleDetail_S


class DepartmentListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Department.objects.all()
    serializer_class = DepartmentList_S

    def get_queryset(self):
        return self.queryset.all()

class DepartmentCreateView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Department.objects.all()
    serializer_class = DepartmentCreate_S
    permission_classes = (permissions.IsAuthenticated,IsAdmin,)

    def post(self, request):
        return self.create(request)

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetail_S

class SubScoreListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin ):
    queryset = Sub_Score.objects.all()
    serializer_class = SubScoreList_S

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(studyprogram_id__student_id=self.request.user).order_by('-id')

class TranscriptListView(generics.ListAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptList_S
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(student_id= self.request.user)

class TranscriptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptDetail_S

class GPAView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        accumutation = Sub_Score.objects.filter(studyprogram_id__student_id=request.user).values('studyprogram_id__course_id__name').annotate(accumutation=Sum('subject_id__credit'))
        gpa = Sub_Score.objects.filter(studyprogram_id__student_id=request.user).values('studyprogram_id__course_id__name').annotate(GPA=Avg('score'))
        #return Response({gpa, accumutation})
        return Response({'GPA': gpa if gpa else 0,
                        'Accumutation' : accumutation
                    })

#***********Test Part************
from rest_framework.response import Response
from rest_framework import status

class ProgramAPI(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = EduProgram.objects.all()
    serializer_class = ProgramGet

    def get_queryset(self):
        return self.queryset.all()
    
    def post(self, request):
        serializer = ProgramPOST(data = request.data, context={'request': request})
        if serializer.is_valid():
            self.object = serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response("You was created", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        # self.object = serializer.save()
        # return self.create(request)
        # if serializer.is_valid():
        #     self.object = serializer.save()
        #     headers = self.get_success_headers(serializer.data)
        #     # Here we serialize the object with the proper depth = 2
        #     new_c = ProgramGet(self.object, context={'request': request})
        #     return Response(new_c.data, status = status.HTTP_201_CREATED, headers = headers)
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)