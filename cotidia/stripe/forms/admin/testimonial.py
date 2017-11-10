# from betterforms.forms import BetterModelForm

# from cotidia.testimonial.models import Testimonial


# class TestimonialAddForm(BetterModelForm):
#     class Meta:
#         model = Testimonial
#         exclude = ['created_at', 'updated_at']
#         fieldsets = (
#             ('info', {
#                 'fields': (
#                     'name',
#                     'role',
#                     'comment',
#                     'active'
#                 ),
#                 'legend': 'Testimonial details'
#             }),
#             ('photo', {
#                 'fields': (
#                     'photo',
#                 ),
#                 'legend': 'Photo'
#             }),
#         )


# class TestimonialUpdateForm(BetterModelForm):
#     class Meta:
#         model = Testimonial
#         exclude = ['created_at', 'updated_at']
#         fieldsets = (
#             ('info', {
#                 'fields': (
#                     'name',
#                     'role',
#                     'comment',
#                     'active'
#                 ),
#                 'legend': 'Testimonial details'
#             }),
#             ('photo', {
#                 'fields': (
#                     'photo',
#                 ),
#                 'legend': 'Photo'
#             }),
#         )
