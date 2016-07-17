# -*- coding: utf-8 -*-
from . import LinkedDataEntityPipeline
import unittest
import os

class LinkedDataEntityPipelineTestCase(unittest.TestCase):
    pipeline = None
    name = "LinkedData Entity Pipeline tests"

    def setUp(self):
        self.pipeline = None

    def tearDown(self):
        self.pipeline = None


    def test_pipeline_execute_with_valid_entity_name(self):
        """
        Test the execution of the LinkedData Entity Pipeline
        """
        input = "Asti"
        self.pipeline = LinkedDataEntityPipeline(input=input,name=self.name, withTypesAnnotation=True, withThumbnailAnnotation=True, withPropertiesAnnotation=True, withPropertyValuesAnnotation=True)
        self.pipeline.execute()

        output = self.pipeline.getOutput()
        print("LINKEDDATA", output)
        self.assertFalse(True)
