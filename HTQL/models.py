from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices

class CustomUser(AbstractUser):
    name = models.CharField(max_length=60, null=True)
    phone = models.IntegerField(null=True)
    address = models.TextField(null=True)
    _Choices = Choices('admin', 'student', 'teacher')
    position = models.CharField(max_length=8,null=True,choices=_Choices)
    sub_id = models.CharField(max_length=7, null=True)
    image = models.ImageField(null=True)
    #department = models.ForeignKey(EduProgram, on_delete= models.CASCADE)

    # def __str__(self):
    #     return str(self.username)

class EduProgram(models.Model):
    name = models.CharField(max_length=50)
    manager = models.OneToOneField(CustomUser, on_delete= models.CASCADE, related_name='manager_in_edup')
    isActive = models.BooleanField(default=True)
    image = models.ImageField(null=True)
    #teacher = models.ManyToManyField(CustomUser, related_name='teacher_in_edup')

    def __str__(self):
        return self.name

class Department(models.Model):
    #name = models.CharField(max_length=100)
    teacher = models.ManyToManyField(CustomUser, related_name='dpt_in_teacher')
    eduprogram = models.ForeignKey(EduProgram, on_delete= models.CASCADE, related_name='dpt_in_edup')

class Subject(models.Model):
    name = models.CharField(max_length=50)
    credit = models.IntegerField()
    teacher_id = models.ManyToManyField(CustomUser, related_name='sub_in_teacher')
    program_id = models.ManyToManyField(EduProgram, related_name='sub_in_program')

    def __str__(self):
        return str(self.name)

class Course(models.Model):
    program_id = models.ForeignKey(EduProgram, on_delete= models.CASCADE, related_name='course_in_program')
    fee = models.IntegerField(null=True)
    start_year = models.DateField(null=True)
    end_year = models.DateField(null=True)
    isActive = models.BooleanField(default=True)
    subject = models.ManyToManyField(Subject)
    image = models.ImageField(null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.name)

class StudyProgram(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete= models.CASCADE, related_name='study_in_course')
    _Choices = Choices('liked', 'registered', 'paused')
    status = models.CharField(max_length=30,choices=_Choices)
    isActive = models.BooleanField(default=False)

class Transcript(models.Model):
    student_id = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    studyprogram_id = models.ForeignKey(StudyProgram, on_delete= models.CASCADE,null=True, related_name='transcript_in_study')
    GPA = models.FloatField(default=0)
    accumutation = models.IntegerField(default=0)
    graduate = models.BooleanField(default=False)


class Sub_Score(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete= models.CASCADE)
    transcript_id = models.ForeignKey(Transcript, on_delete= models.CASCADE, null=True,related_name='score_in_transcript')
    score = models.FloatField(null=True)
    studyprogram_id = models.ForeignKey(StudyProgram, on_delete= models.CASCADE, related_name='score_in_study')
    is_completed = models.BooleanField(default=False)

class ClassList(models.Model):
    studyprogram = models.ForeignKey(StudyProgram, on_delete= models.CASCADE, related_name='schedule_in_stup')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.DateField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_in_course', null=True)
    #class_id = models.CharField(max_length=20, null=True)
    score = models.FloatField(null= True)

class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedule_in_course')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.IntegerField(null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)
    room = models.CharField(max_length=6, null=True)
