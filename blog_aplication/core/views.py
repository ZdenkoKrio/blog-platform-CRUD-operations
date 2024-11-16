from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "core/home.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        captcha = request.POST.get('captcha')

        if captcha != "8":
            messages.error(request, "Incorrect captcha. Please try again.")
            return render(request, self.template_name)

        try:
            send_mail(
                subject=f"Contact Form Submission from {name}",
                message=message,
                from_email=email,
                recipient_list=[settings.CONTACT_EMAIL],
            )
            messages.success(request, "Your message has been sent successfully!")

        except Exception as e:
            messages.error(request, f"Failed to send message: {str(e)}")

        return render(request, self.template_name)
