from django.db import models


class FormsData(models.Model):
    formName = models.CharField(max_length=225)
    formContent = models.TextField()

    def __str__(self):
        return self.formName

    class Meta:
        db_table = 'FormsTable'


class ResponsesData(models.Model):
    form_response = models.JSONField()

    class Meta:
        db_table = 'response_table'


class UserForms(models.Model):
    form_user = models.CharField(max_length=225)
    form_name = models.CharField(max_length=225)
    form_description = models.TextField()
    form_content = models.TextField()
    user_responses = models.ManyToManyField(ResponsesData)
    has_files = models.BooleanField()

    def __str__(self):
        return self.form_name

    class Meta:
        db_table = 'users_forms'
