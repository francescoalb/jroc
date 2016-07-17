# -*- coding: utf-8 -*-

from . import tagger
from flask import request, Response
from jroc.pipelines.ner.NERPipeline import NERPipeline
from jroc.pipelines.pos.PosTaggerPipeline import PosTaggerPipeline

import json

@tagger.route("/")
def taggerMain():
    uris = {
        "tags": "/tags",
        "entities": "/entities"
    }
    json_response = json.dumps(uris)
    return Response(json_response, mimetype="application/json")

@tagger.route("/tags", methods=["POST"])
def taggerTags():
    shouldFilterStopwords = True if request.args.get('stopwords') == 'true' else False
    shouldShowLanguage = True if request.args.get('language') == 'true' else False

    data = request.data

    pipeline = PosTaggerPipeline(input=data, name="PosTagger Pipeline")
    pipeline.execute()
    output = pipeline.getOutput()

    tags = output.get('tags', [])

    result = {}
    result["uri"] = "%s" % (request.base_url, )
    result["data"] = tags
    result["meta"] = {}
    if shouldShowLanguage == True:
        result["meta"]["language"] = languageResult[0]

    json_response = json.dumps(result)
    return Response(json_response, mimetype="application/json")

@tagger.route("/entities", methods=["POST"])
def taggerEntities():
    shouldFilterStopwords = True if request.args.get('stopwords') == 'true' else False
    shouldShowLanguage = True if request.args.get('language') == 'true' else False
    showAdvancedResult = True if request.args.get("advanced") == 'true' else False
    showAnnotation = True if request.args.get("annotation") == 'true' else False

    data = request.data
    pipeline = NERPipeline(input=data, name="NER Pipeline", withEntityAnnotation=showAnnotation)
    pipeline.execute()
    output = pipeline.getOutput()

    language = output.get('language', None)
    entities = output.get('entities', [])

    if showAdvancedResult and len(entities) > 0:
        # Advanced formatting for each entity
        temp = []
        for entity in entities:
            temp.append({
                "name": entity,
                "uri": "%sentities/%s"  % (request.url_root, entity.replace(" ", "_"))
            })
        entities = temp

    result = {}
    result["uri"] = "%s" % (request.base_url, )
    result["data"] = entities
    result["data"]
    result["meta"] = {}

    if shouldShowLanguage == True:
        result["meta"]["language"] = languageResult[0]
    if showAnnotation == True:
        entities_annotated = output.get('entities-annotated', [])
        result["meta"]["annotation"] = entities_annotated


    json_response = json.dumps(result)
    return Response(json_response, mimetype="application/json")

@tagger.route("/analyze", methods=["POST"])
def taggerAnalyze():
    data = request.data
    data = data.replace("'","\"").replace("\n", "")
    json_result = json.loads(data)

    result = {}
    result["uri"] = "%s" % (request.base_url, )

    pipeline = NERPipeline(input=data, name="NER Pipeline")
    pipeline.execute()
    output = pipeline.getOutput()


    data = {}
    data["language"] = output.get('language', None)
    data["entities"] = output.get('entities', [])
    data["tags"] = output.get('tags', [])
    data["text_analyze"]  = output.get('pos', None)
    """
    if(requestObt == True):
        obt_result = obtManager.obtAnalyze()
        data["obt"] = obt_result

    if(requestTags == True):
        tags = obtManager.findTags()
        data["tags"] = tags

    if(requestEntities == True):
        entities = obtManager.findEntities()
        data["entities"] = entities
    """
    result["data"] = data

    json_response = json.dumps(result)

    return Response(json_response, mimetype="application/json")
