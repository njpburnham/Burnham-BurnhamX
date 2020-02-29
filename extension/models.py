from django.db import models


class Opportunity(models.Model):
  """
  This model holds information about an Opportunity
  """
  name = models.CharField(max_length=250)
  status = models.CharField(max_length=100) # this is more of a project status
  street = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=20)
  zip_code = models.CharField(max_length=12, null=True, blank=True)
  siebel_id = models.CharField(max_length=100)
  create_date = models.DateTimeField('date created', auto_now_add=True)
  modified_date = models.DateTimeField('date modified', auto_now=True)

  class Meta:
    ordering = ('create_date',)

  def __unicode__(self):
    return self.name

class Association(models.Model):
  """
  This model holds information about the association of an OPTY to an Email
  """
  email_id = models.CharField(max_length=150, db_index=True)
  thread_id = models.CharField(max_length=150, db_index=True)
  opportunity = models.ForeignKey(Opportunity, related_name='associations')
  created_user = models.CharField(max_length=150) # Mostly likely either an email address or `Siebel`
  is_active = models.BooleanField(default=True, db_index=True)
  create_date = models.DateTimeField('date created', auto_now_add=True)
  modified_date = models.DateTimeField('date modified', auto_now=True)

  class Meta:
    ordering = ('create_date',)

class Users(models.Model):
  """
  This class holds the users of the application
  """
  email = models.CharField(max_length=150)
  opportunities = models.ManyToManyField(Opportunity)
  create_date = models.DateTimeField('date created', auto_now_add=True)
  modified_date = models.DateTimeField('date modified', auto_now=True)
  