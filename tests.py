from unittest.case import _AssertRaisesContext
from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm,BusRegistrationForm,AsosRegistrationForm
import unittest
from flask import Flask



#users testing-using unittest,for activation run that file
class test_models(unittest.TestCase):


#test for creating a post in the db
    def test_new_post(self):
        new_post=Post(id=112233,user_id=56789,title="Testing-Post",content="Post-Content",date_posted='April 21, 2018')
        assert new_post.id==112233,"should be equal"
        assert new_post.user_id==56789,"should be equal"
        assert new_post.title=="Testing-Post","should be equal"
        assert new_post.content=="Post-Content","should be equal"
        assert new_post.date_posted=='April 21, 2018'
        assert new_post.id != 1234, "should not be equal"
        assert new_post.user_id!=12212,"should not be equal"
        assert new_post.is_foster!=True, "should not be equal"
        assert new_post.is_discount!=True, "should not be equal"
        assert new_post.is_adopt!=True , "should not be equal"
        assert new_post.is_product!=True, "should not be equal"
        assert new_post.is_event!=True, "should not be equal"

 #test for making another type of post in the db
    def test_new_adopt_post(self):
        new_post=Post(id=435,user_id=69089,title="Testing-test",content="Post-post",date_posted='April 21, 2018',is_adopt=True)
        assert new_post.id==435,"should be equal"
        assert new_post.user_id==69089,"should be equal"
        assert new_post.title=="Testing-test","should be equal"
        assert new_post.content=="Post-post", "should be equal"
        assert new_post.date_posted=='April 21, 2018'
        assert new_post.id != 1234, "should not be equal"
        assert new_post.user_id!=12212, "should not be equal"
        assert new_post.is_foster!=True, "should not be equal"
        assert new_post.is_event!=True ,"should not be equal"
        assert new_post.is_adopt==True, "should be equal"  #check the flag that indicate of adopt post

    #test creation of a new user (test User "Ctor")
    def test_User(self):
        new_user=User(name="yosi",id=123,email="aaa@gmail.com", password="12345")
        assert new_user.password=="12345","should be equal"
        assert new_user.email=="aaa@gmail.com", "should be equal"
        assert new_user.id==123, "should be equal"
        assert new_user.name=="yosi", "should be equal"
        assert new_user.id!=1345, "should not be equal"
        assert new_user.is_asos != True ,"should not be equal"
        assert new_user.is_bus != True , "should not be equal"
        assert new_user.is_admin != True,"should not be equal"




        #test creation of a new bussines user (test User "Ctor"+ bus_id + is_bus flag)
    def test_bussines_User(self):
        new_user = User(name="Jhon", email="asd@walla.com", password="234", bus_id=4567, is_bus=True)
        assert new_user.password=="234","should be equal"
        assert new_user.email=="asd@walla.com", "should be equal"
        assert new_user.bus_id==4567, "should be equal"
        assert new_user.bus_id!=1345, "should not be equal"
        assert new_user.is_bus==True, "should be equal"     #check the flag that indicate of bussines user
        assert new_user.is_asos != True,"should not be equal"
        assert new_user.is_admin != True,"should not be equal"
        assert new_user.name=="Jhon", "should be equal"    

        #test creation of a new assosiationuser user (test User "Ctor"+ address + is_asos flag)
    def test_assosiation_User(self):
        new_user = User(name="Jim", email="avvv@yahooo.com", password="xzy456", address="Beer-Sheva", is_asos=True)
        assert new_user.password=="xzy456","should be equal"
        assert new_user.email=="avvv@yahooo.com", "should be equal"
        assert new_user.address=="Beer-Sheva", "should be equal"
        assert new_user.name=="Jim", "should be equal"
        assert new_user.address!="Dimona", "should not be equal"
        assert new_user.is_asos==True, "should be equal"     #check the flag that indicate of assosiationuser user

    

if __name__ == '__main__':
    unittest.main()