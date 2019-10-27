from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import CustomUser, Department
from django.shortcuts import get_object_or_404

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view,obj):
        return request.user.is_superuser

class IsOwnerOrAdmin(BasePermission):
    # def has_permission(self, request, view):
    #     if (request.user.is_staff and request.user.vip_account) or request.user.is_superuser:
    #         return True
    #     else:
    #         return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        #Chỉ owner và admin mới có thể sửa, xóa
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_superuser

class IsOwnerOrAdmin_EducationProgram(BasePermission):
    # def has_permission(self, request, view):
    #     if (request.user.is_staff and request.user.vip_account) or request.user.is_superuser:
    #         return True
    #     else:
    #         return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        #Chỉ owner và admin mới có thể sửa, xóa
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.teacher_id == request.user or request.user.is_superuser

class CanCreateOrNot(permissions.BasePermission):

    def has_permission(self, request, view):
        #chỉ admin mới có thể create Education program
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

class Pms_Register(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous == True:
            return True
        return False

class IsStudentOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.position == "student" or request.user.is_superuser:
            return True
        return False

class CanUpdateStup(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.course_id.program_id.manager == request.user or request.user.is_superuser

class StudentUpdateStup(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.student_id == request.user or request.user.is_superuser

class IsAdminOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            return request.user.is_superuser or request.user.manager_in_edup != None
        except:
            return False

class CanUpdateScore(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in obj.subject.teacher_id.all() and Department.objects.filter(eduprogram=obj.course.program_id, teacher=request.user).count() > 0


class CanPostSchedule(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser