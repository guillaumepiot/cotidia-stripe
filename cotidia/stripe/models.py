from django.db import models


class Customer(models.Model):
    user = models.OneToOneField('account.User', null=True)
    description = models.CharField(max_length=255)

    stripe_id = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-created_at']

    def get_stripe_customer(self):
        return stripe.Customer.retrieve(self.stripe_id)


class Subscription(models.Model):
    customer = models.ForeignKey('stripe.Customer', null=True)

    stripe_id = models.CharField(max_length=255)

    plan_id = models.CharField(max_length=255)

    current_period_start = models.IntegerField()
    current_period_end = models.IntegerField()
    cancel_at_period_end = models.IntegerField(null=True)
    canceled_at = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.description} - {self.plan_id}"

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']

    def get_stripe_subscription(self):
        return stripe.Subscription.retrieve(self.stripe_id)

# class Testimonial(models.Model):
#     name = models.CharField(max_length=50)
#     role = models.CharField(max_length=50, null=True)
#     comment = models.TextField(max_length=500)
#     photo = models.ImageField(blank=True)
#     active = models.BooleanField(default=True)

#     order_id = models.IntegerField(null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Testimonial'
#         verbose_name_plural = 'Testimonials'
#         ordering = ['order_id', 'name']

#     def save(self, *args, **kwargs):
#         """Clean old image if replaced."""
#         if self.pk:
#             original = Testimonial.objects.get(pk=self.pk)
#             if original.photo and original.photo != self.photo:
#                 # Use save=False to avoid recursion loop
#                 original.photo.delete(save=False)
#         super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         """Remove image."""
#         if self.photo:
#             self.photo.delete(save=False)
#         super().delete(*args, **kwargs)
