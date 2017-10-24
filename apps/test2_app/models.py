from __future__ import unicode_literals
from django.db import models
from ..oct_app.models import User

class PetManager(models.Manager):
    def createPet(self, postData):
        self.create(name = postData['name'], pet_type = postData['pet_type'])

    def validate(self, postData):
        results = {'errors':[], 'status':False}  #this is what he's creating and will equal to a dictionary. within the dictionary we create a key. The reason why status is set to False is because there is not current error. Error is a list and status is a boolean
        if len(postData['name']) <= 0:
            results['status'] = True
            results['errors'].append('All fields required')
        if len(postData['name']) < 2:
            results['status'] = True
            results['errors'].append('Please choose a name longer than two characters')
        if len(postData['pet_type']) <= 0:
            results['status'] = True
            results['errors'].append('All fields required')

        pet = self.filter(name=postData['name'])   
        if len(pet) > 0: 
            results['status'] = True
            results['errors'].append('Name already in use')
        
        return results #dont forget to return results


class Pet(models.Model):
    name = models.CharField(max_length = 255)
    pet_type = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name="pets", default=1)  #forgeing key allows us to use a one to many relationships. Related name tells us the name of the field that is. and we are using pets because user have many pets but we can name it whatever we want
    #this pets name will be used later to be retrived later in our HTML
    objects = PetManager()

