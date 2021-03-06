#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import make_response
import json
import document_analyzer, dictionary, datamuse, syn_ant

app = Flask(__name__)

### dictionary methods ###

# example request:
# curl -i http://localhost:5000/dictionary/5
@app.route('/dictionary/<int:n>', methods=['GET'])
def get_nlength(n):
	return dictionary.get_n_length_json(n)

### document_analyzer methods ###

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"URLs": ["https://www.araba.com", "https://www.arabam.com", "http://www.oyunskor.com/araba-oyunlari", "https://www.sahibinden.com/kategori/otomobil", "http://www.oyunkolu.com/araba-oyunlari/"]}' http://localhost:5000/document_analyzer/get_tfidf_scores
@app.route('/document_analyzer/get_tfidf_scores', methods=['POST'])
def get_tfidf_scores():
    if not request.json or not 'URLs' in request.json:
        abort(400)
    result = document_analyzer.get_tfidf_scores(request.json['URLs'])
    return jsonify(result), 200

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"query": "lol", "count": 5, "length": 4 }' http://localhost:5000/document_analyzer/analyze_search_result
@app.route('/document_analyzer/analyze_search_result', methods=['POST'])
def analyze_search_result():
    if not request.json or not 'query' in request.json or not 'count' in request.json or not 'length' in request.json:
        abort(400)
    result = document_analyzer.analyze_search_result(request.json['query'], request.json['count'], request.json['length'])
    return jsonify(result), 200

### datamuse methods ###

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"ml":"Seasoning on an everything bagel"}' http://localhost:5000/datamuse/search_datamuse_wordenp
@app.route('/datamuse/search_datamuse_wordenp', methods=['POST'])
def search_wordenp():
    if not request.json or not 'ml' in request.json:
        abort(400)
    result = datamuse.search_datamuse_wordenp(request.json['ml'])
    return json.dumps(result) + "\n", 200

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"ml":"Seasoning on an everything bagel", "word_length": 4}' http://localhost:5000/datamuse/wiki_search
@app.route('/datamuse/wiki_search', methods=['POST'])
def wiki_search():
    if not request.json or not 'ml' in request.json or not 'word_length' in request.json:
        abort(400)
    result = datamuse.wiki_search(request.json['ml'], request.json['word_length'])
    return json.dumps(result) + "\n", 200

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"ml":"Seasoning on an everything bagel", "word_length": 4}' http://localhost:5000/datamuse/datamuse_answer_list
@app.route('/datamuse/datamuse_answer_list', methods=['POST'])
def answer_list():
    if not request.json or not 'ml' in request.json or not 'word_length' in request.json:
        abort(400)
    result = datamuse.datamuse_answer_list(request.json['ml'], request.json['word_length'])
    return json.dumps(result) + "\n", 200

### syn_ant methods ###

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"str":"selim", "word_length": 5}' http://localhost:5000/syn_ant/find_all_synonyms
@app.route('/syn_ant/find_all_synonyms', methods=['POST'])
def find_all_synonyms():
    if not request.json or not 'str' in request.json or not 'word_length' in request.json:
        abort(400)
    result = syn_ant.find_all_synonyms(request.json['str'], request.json['word_length'])
    return json.dumps(list(result)) + "\n", 200

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"str":"selim", "word_length": 5}' http://localhost:5000/syn_ant/find_all_antonyms
@app.route('/syn_ant/find_all_antonyms', methods=['POST'])
def find_all_antonyms():
    if not request.json or not 'str' in request.json or not 'word_length' in request.json:
        abort(400)
    result = syn_ant.find_all_antonyms(request.json['str'], request.json['word_length'])
    return json.dumps(list(result)) + "\n", 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)