#!/usr/bin/env python
import os
import sys
import unittest
from prophet_model import model_train, model_predict

class ModelTest(unittest.TestCase):
    """
    Test the essential model functionality
    """
        
    def test_train_model(self):
        """
        Test the train functionality
        """

        ## train the model
        val=model_train()
        self.assertTrue(val)
       
    def test_predict(self):
        """
        Test the predict function input
        """
    
        result = model_predict("all","2017","10","11")

        self.assertTrue(result.yhat.values[0] >= 0.0)
        # self.assertTrue(result.yhat.values[0] > 5300)

    def test_predict_country(self):
        """
        test the predict function input with unallowed country
        """
    
        result = model_predict("finland","2020","09","11")
        self.assertEqual(result,"Could not find country called finland")

    def test_predict_date(self):
        """
        Test the predict function input with unallowed date
        """
    
        result = model_predict("all","2010","09","10")
        self.assertEqual(result,"Date not available")

### Run the tests
if __name__ == '__main__':
    unittest.main()
