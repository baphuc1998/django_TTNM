from django.urls import path, include
from . import views
# from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/user/', views.UserListView.as_view() , name='list_user'),
    path('api/user/<int:pk>/', views.UserDetailView.as_view() , name='detail_user'),
    path('api/user/register/', views.UserCreateView.as_view(), name='register_user' ),
    path('api/student/register/', views.StudentCreateView.as_view() ),
    path('api/user/profile/', views.UserProfileAPI.as_view() ),
    path('api/user/teacher/', views.TeacherListView.as_view() ),
    path('api/user/password/<int:pk>/', views.UserResetPassword.as_view() ),

    path('api/edup/', views.EduProgramListView.as_view(), name='list_eduprogram'),#danh sách các chương trình đào tạo
    path('api/edup/create/', views.EduProgramCreateView.as_view(), name='list_eduprogram'),
    path('api/edup/<int:pk>/', views.EduProgramDetailView.as_view(), name='detail_eduprogram'),

    path('api/course/', views.CourseListView.as_view(), name='list_course'), #danh sách khóa học được admin tạo
    path('api/course/create/', views.CourseCreateView.as_view(), name='list_course'),
    path('api/course/<int:pk>/', views.CourseDetailView.as_view(), name='detail_course'),
    path('api/teacher/course/', views.TeacherCourseListView.as_view()),

    path('api/stup/', views.StudyProgramListView.as_view(), name='list_studyprogram'), #danh sách các đăng ký của sinh viên
    path('api/stup/registered/', views.SPListView.as_view(), name='list_registered_studyprogram'), #danh sách các đăng ký của sinh viên
    path('api/stup/create/', views.StudyProgramCreateView.as_view(), name='list_studyprogram'),
    path('api/stup/<int:pk>/', views.StudyProgramDetailView.as_view(), name='detail_studyprogram'),

    path('api/manager/stup/', views.ManagerStudyProgramListView.as_view(), name='manager_list_studyprogram'), #danh sách các đăng ký của sinh viên
    path('api/manager/stup/<int:pk>/', views.ManagerStudyProgramDetailView.as_view(), name='manager_detail_studyprogram'),


    path('api/class/', views.ClassListView.as_view(), name='list_class' ), #danh sách lớp, gv có thể chấm điểm trực tiếp trên danh sách này.
    path('api/class/<int:pk>/', views.ClassDetailView.as_view(), name='detail_class' ),

    path('api/subject/', views.SubjectListView.as_view(), name='list_subject'), #danh sách các môn học
    path('api/subject/create/', views.SubjectCreateView.as_view(), name='list_subject'),
    path('api/subject/<int:pk>/', views.SubjectDetailView.as_view(), name='detail_subject'),
    path('api/teacher/subject/', views.SubjectofTeacherList.as_view()),

    path('api/schedule/', views.ScheduleListView.as_view(), name='list_schedule'), #danh sách thời khóa biểu
    path('api/schedule/create/', views.ScheduleCreateView.as_view(), name='list_schedule'),
    path('api/schedule/<int:pk>/', views.ScheduleDetailView.as_view(), name='detail_schedule'),

    path('api/department/', views.DepartmentListView.as_view(), name='list_department'), #danh sách giảng viên của một bộ môn
    path('api/department/create/', views.DepartmentCreateView.as_view(), name='list_department'),
    path('api/department/<int:pk>/', views.DepartmentDetailView.as_view(), name='detail_department'),

    path('api/subscore/', views.SubScoreListView.as_view(), name='list_subscore'), #xem điểm của từng môn học (KQ học tập)
    path('api/summary/', views.GPAView.as_view(), name='list_subscore'), #remove

    path('api/transcript/', views.TranscriptListView.as_view(), name='list_transcript'), #xem điểm tổng kết (GPA & tín chỉ tích lũy)
    path('api/transcript/<int:pk>/', views.TranscriptDetailView.as_view(), name='detail_transcript'),


    #path('api/user/login', obtain_jwt_token),
    path('api/user/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Test URLS
    path("api/test/edup/", views.ProgramAPI.as_view()),
    path('api/test/edup/<int:pk>/', views.EduProgramDetailView.as_view(), name='test_eduprogram'),
]