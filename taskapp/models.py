from django.db import models

# Create your models here.



from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    bio=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(null=False,blank=False)


def _str_(self):
    return self.name
