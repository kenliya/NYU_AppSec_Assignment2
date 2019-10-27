import random
import unittest
import app
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client() 
        #self.app.config['TESTING'] = True
        self.app.application.config['WTF_CSRF_METHODS'] = []
        self.app.testing = True
        self.app.debug = True
    
    def tearDown(self):
        pass
    
    def test_register_page(self):
        res = self.app.get("/register")
        print(res)
        assert res.status_code == 200
    
    def test_register(self):
        test_data = {'uname': "test", 'pword':"1234567", 'phone': "1234567890"}
        response = self.app.post('/register', data=test_data)
        print(response)
        self.assertIn(b'hidden', response.data)
    
    def test_login(self):
        test_data = {'uname': "test", 'pword':"1234567", 'phone': "1234567890"}
        response = self.app.post('/register', data=test_data)
        print(response)
        response = self.app.post('/login', data = test_data)
        print(response)
        self.assertIn(b'result', response.data)
        
    
    #def test_statuscode(self):
        
if __name__ == '__main__':
	unittest.main()