from django.db import models

# Create your models here.


class Сategory(models.Model):
    category = models.CharField(max_length = 150)
    imgPath = models.CharField(max_length = 1000,blank=True)

    def __str__(self): 
        return self.category


class ProductGroups(models.Model):
    category  = models.ForeignKey(Сategory, on_delete=models.CASCADE) 
    group = models.CharField(max_length = 150)
    imgPath = models.CharField(max_length = 1000,blank=True)

    def __str__(self): 
        return self.group

class Products(models.Model):
    #category  = models.ForeignKey(Сategory, on_delete=models.CASCADE) 
    group = models.ForeignKey(ProductGroups, on_delete=models.CASCADE) 
    imgPath = models.CharField(max_length = 1000,blank=True)
    name = models.CharField(max_length = 300)
    mod = models.CharField(max_length = 150, blank=True)
    prise = models.CharField(max_length = 150)
    availability = models.BooleanField()
    promotion = models.BooleanField()
    description = models.TextField(blank=True)


    def __str__(self): 
        return self.name

class Articles(models.Model):
    name = models.CharField(max_length = 500)
    imgPath = models.CharField(max_length = 1000,blank=True)
    description = models.TextField(blank=True)