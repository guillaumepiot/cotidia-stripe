# import django_filters

# from django.db.models import Q

# from cotidia.admin.views import (
#     AdminListView,
#     AdminDetailView,
#     AdminCreateView,
#     AdminUpdateView,
#     AdminDeleteView,
# )

# from cotidia.testimonial.models import Testimonial
# from cotidia.testimonial.forms.admin.testimonial import (
#     TestimonialAddForm,
#     TestimonialUpdateForm,
# )


# class TestimonialFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(
#         label="Search",
#         method="filter_all"
#     )

#     class Meta:
#         model = Testimonial
#         fields = ['name', 'active']

#     def filter_all(self, queryset, name, value):
#         return queryset.filter(
#             Q(name__icontains=value) |
#             Q(role__icontains=value) |
#             Q(comment__icontains=value)
#         )


# class TestimonialList(AdminListView):
#     columns = (
#         ('Name', 'name'),
#         ('Role', 'role'),
#         ('Active', 'active'),
#     )
#     model = Testimonial
#     filterset = TestimonialFilter
#     template_type = "centered"


# class TestimonialDetail(AdminDetailView):
#     model = Testimonial
#     fieldsets = [
#         {
#             "legend": "Testimonial details",
#             "fields": [
#                 [
#                     {
#                         "label": "Name",
#                         "field": "name",
#                     }
#                 ],
#                 {
#                     "label": "Role",
#                     "field": "role",
#                 },
#                 {
#                     "label": "Comment",
#                     "field": "comment",
#                 },
#                 {
#                     "label": "Active",
#                     "field": "active",
#                 },
#             ]
#         },
#         {
#             "legend": "Photo",
#             "fields": [
#                 {
#                     "label": "Photo",
#                     "field": "photo",
#                 }
#             ]
#         }
#     ]


# class TestimonialCreate(AdminCreateView):
#     model = Testimonial
#     form_class = TestimonialAddForm


# class TestimonialUpdate(AdminUpdateView):
#     model = Testimonial
#     form_class = TestimonialUpdateForm


# class TestimonialDelete(AdminDeleteView):
#     model = Testimonial
