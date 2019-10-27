import random
import unittest
import app
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        #app.config['TESTING'] = True
        self.app = app.app.test_client()
        self.app.testing = True
        self.app.debug = True
        
	#def test_register(self):
	#	res = self.web.get("/register")
	#	assert res.status_code == 200
    
    def tearDown(self):
        pass
    
    def test_register(self):
        test_data = {'uname': "test", 'pword':"1234567", 'phone': "1234567890"}
        response = self.app.post('/register', data=test_data)
        self.assertIn('failure', response.data)
    
    #def test_statuscode(self):
        
if __name__ == '__main__':
	unittest.main()