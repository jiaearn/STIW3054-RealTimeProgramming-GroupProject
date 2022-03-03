from django.db import models
from victim_app.models import Victim


class AssistanceType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated at')
    
    def __str__(self):
        return self.name


class Assistance(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name', null=True, blank=True)
    ic = models.CharField(max_length=255, verbose_name='Ic', default="")
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)
    progress_percentage = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Progress Percentage', null=True, blank=True, default='0.0')
    victim_number = models.IntegerField(verbose_name='Victim Number')
    is_approved = models.BooleanField(verbose_name='Is Approved', default=False)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE, null=True, related_name='assistance_list')
    assistance_type = models.ForeignKey(AssistanceType, on_delete=models.CASCADE, related_name='assistance_type')
    assistance_given_date = models.DateField(verbose_name='Assistance Given Date', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated at')

    # def __str__(self):
    #     return self.user.username + "-" + self.assistance_type.name










