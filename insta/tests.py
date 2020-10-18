from django.test import TestCase
from . models import Image, Profile, Comment, Like

# Create your tests here.
class ProfileTestClass(TestCase):
    '''
    class that test the characteristics of the Profile model
    '''

    def setUp(self):
        '''
        method that runs at the begginning of each test
        '''
        self.profile = Profile(profile_photo ='test_profile_photo', bio = 'test_bio')

    def test_save_profile(self):
        '''
        method that tests save method of the Profile model
        '''
        self.profile.save_profile()
        all_profiles = Profile.objects.all()
        self.assertTrue(len(all_profiles)>0)

        
    def test_delete_profile(self):
        '''
        method that tests the delete_profile method
        '''
        self.profile.save_profile()
        profile2 = Profile(profile_photo ='test_profile_photo2',bio = 'test_bio2')
        profile2.save_profile()
        self.profile.delete_profile()
        all_profiles = Profile.objects.all()
        self.assertTrue(len(all_profiles)==1)

    def test_find_profile(self):
        '''
        method that tests the find_profile method
        '''
        self.profile.save_profile()
        profile2 = Profile(profile_photo ='test_profile_photo2',bio = 'test_bio2')
        profile2.save_profile()
        search_profile = Profile.find_profile('test_bio2')
        self.assertTrue(len(search_profile)==1)
