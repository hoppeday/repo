from __future__ import unicode_literals

from django.db import models
import re #this means regular expressions and its imported from python
import bcrypt

class UserManager(models.Manager):
    def createUser(self, postData): #this will handle the creation of our user
        #so now we use postDAta to interact with whatever information we want.
        password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()) #change this  test perimeter and change it 
        self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = password)

    def loginVal(self, postData):
        results = {'errors': [], 'status': False, 'user': None}
        email_matches = self.filter(email = postData['email'])
        if len(email_matches) == 0:
            results['errors'].append('Please check your email and password and try again')
            results['status'] = True
        else:
            results['user'] = email_matches[0] #that we are grabbing that first thing in the array
            if not bcrypt.checkpw(postData['password'].encode(), results['user'].password.encode()): #this is to check an email from out database adn compare with whats in the input
                results['errors'].append('Please check your email and password and try again')
                results['status'] = True
        return results
        

#we use postData but can be named anything and will need to be consistent
    def registerVal(self, postData):
        results = {'errors':[], 'status':False}  #this is what he's creating and will equal to a dictionary. within the dictionary we create a key. The reason why status is set to False is because there is not current error. Error is a list and status is a boolean
        if len(postData['first_name']) < 2:
            results['status'] = True
            results['errors'].append('First name is too short')
        if len(postData['last_name']) < 2:
            results['status'] = True
            results['errors'].append('Last name is too short')
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']): #we are building a listener 
            results['status'] = True
            results['errors'].append('This is not a valid email')

        if len(postData['password']) < 3:
            results['status'] = True
            results['errors'].append('Password is too short')
        
        if postData['password'] != postData['c_password']:
            results['status'] = True
            results['errors'].append('Passwords does not match')
        
        user = self.filter(email=postData['email'])  #we are just using a variable and we are using self because we are inside the object 
        if len(user) > 0: #what this means is that if it does find an user then throw an error
            results['status'] = True
            results['errors'].append('Email already in use')


        return results


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 60)
    objects = UserManager()