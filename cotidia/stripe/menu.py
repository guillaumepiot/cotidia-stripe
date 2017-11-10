from django.core.urlresolvers import reverse


def admin_menu(context):
    return [
        # {
        #     "text": "Testimonials",
        #     "icon": "quote-left",
        #     "url": reverse("testimonial-admin:testimonial-list"),
        #     "permissions": [
        #         "testimonial.add_testimonial",
        #         "testimonial.change_testimonial"
        #     ],
        # },
    ]
