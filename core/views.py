from rest_framework import viewsets
from .models import Class, Student, Teacher
from .serializers import ClassSerializer, StudentSerializer, TeacherSerializer
from .models import Class, Student, Teacher, Subject  # Added Subject
from .serializers import ClassSerializer, StudentSerializer, TeacherSerializer, SubjectSerializer # Added SubjectSerializer
from .models import Class, Student, Teacher, Subject, Attendance, Grade
from .serializers import ClassSerializer, StudentSerializer, TeacherSerializer, SubjectSerializer, AttendanceSerializer, GradeSerializer
import requests # New import
from rest_framework.decorators import action # New import
from rest_framework.response import Response # New import
from .models import Class, Student, Teacher, Subject, Attendance, Grade, Payment # Added Payment
from .serializers import (
    ClassSerializer, StudentSerializer, TeacherSerializer, 
    SubjectSerializer, AttendanceSerializer, GradeSerializer, PaymentSerializer
)



# THE LOGIC LAYER (Views)
# These classes decide what happens when a request comes in.


class ClassViewSet(viewsets.ModelViewSet):
    """
    Handles: GET (List), POST (Create), PUT (Update), DELETE
    URL: /api/classes/
    """
    # 1. The Queryset: What data are we looking at? (All classes)
    queryset = Class.objects.all()
    # 2. The Serializer: How do we translate this data?
    serializer_class = ClassSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    Handles: GET, POST, PUT, DELETE for Students
    URL: /api/students/
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    Handles: GET, POST, PUT, DELETE for Teachers
    URL: /api/teachers/
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Handles: GET, POST, PUT, DELETE for Subjects
    URL: /api/subjects/
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    URL: /api/attendance/
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class GradeViewSet(viewsets.ModelViewSet):
    """
    URL: /api/grades/
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # This is a Custom Action.
    # It creates a new URL: /api/payments/verify_payment/
    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        # 1. Get the reference from the user
        reference = request.data.get('reference')
        
        if not reference:
            return Response({'error': 'No reference provided'}, status=400)

        # 2. Find the payment in our database
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment record not found'}, status=404)

        # 3. Talk to Paystack to confirm
        PAYSTACK_SECRET_KEY = sk_test_dfe9371315db792a6a7dab8dd2f9f74abb57470f 
        headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        response_data = response.json()

        # 4. Check Paystack's answer
        if response_data['status'] is True and response_data['data']['status'] == 'success':
            # It's real money! Update our database.
            payment.status = 'VERIFIED'
            payment.save()
            return Response({'status': 'Payment Verified', 'amount': payment.amount})
        else:
            return Response({'error': 'Verification failed'}, status=400)