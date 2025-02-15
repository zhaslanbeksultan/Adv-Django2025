import pdfkit
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings

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