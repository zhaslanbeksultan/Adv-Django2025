import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from users.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer

def home_page(request):
    return render(request, 'mysite/home.html')
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'mysite/register.html')

    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        # return redirect('login')
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def get(self, request):
        return render(request, 'mysite/login.html')
    #
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = auth.authenticate(username=serializer.validated_data['username'],
    #                              password=serializer.validated_data['password'])
    #     if user:
    #         auth.login(request, user)  # Useful for checking `user.is_authenticated` in templates
    #
    #         # Generate tokens
    #         refresh = RefreshToken.for_user(user)
    #         access = refresh.access_token
    #
    #         # Set tokens as HttpOnly cookies
    #         response = redirect('home')
    #         response.set_cookie(
    #             key='access_token',
    #             value=str(access),
    #             httponly=True,
    #             secure=True,  # Set to True in production (requires HTTPS)
    #             samesite='Lax'
    #         )
    #         response.set_cookie(
    #             key='refresh_token',
    #             value=str(refresh),
    #             httponly=True,
    #             secure=True,
    #             samesite='Lax'
    #         )
    #         return response
    #     else:
    #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return redirect('login')

def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'mysite/profile.html', {'user': request.user})
    else:
        return redirect('login')

def profile_pdf_view(request):
    # Render the HTML template with user data
    html_content = render_to_string('mysite/profile_pdf.html', {'user': request.user})

    # Define path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='E:\\wkhtmltox\\bin\\wkhtmltopdf.exe')  # Adjust this for your OS

    # Convert HTML to PDF
    pdf = pdfkit.from_string(html_content, False, configuration=config)

    # Return PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="profile.pdf"'
    return response