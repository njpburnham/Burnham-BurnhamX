from django.db import models

class Customer(models.Model):
  name = models.CharField(max_length=100)
  create_date = models.DateTimeField('date created', auto_now_add=True)
  modified_date = models.DateTimeField('date modified', auto_now=True)

  class Meta:
    ordering = ('create_date',)