from flask import Flask, render_template, request, jsonify
import re
import html

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match_regex():
    data = request.get_json()
    text = data.get('text', '')
    pattern = data.get('pattern', '')
    
    if not pattern:
        return jsonify({'highlighted_text': html.escape(text), 'matches': 0})
    
    try:
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
        matches = list(regex.finditer(text))
        
        if not matches:
            return jsonify({'highlighted_text': html.escape(text), 'matches': 0})
        
        highlighted_text = ""
        last_end = 0
        
        for match in matches:
            start, end = match.span()
            highlighted_text += html.escape(text[last_end:start])
            highlighted_text += f'<mark>{html.escape(text[start:end])}</mark>'
            last_end = end
        
        highlighted_text += html.escape(text[last_end:])
        
        return jsonify({
            'highlighted_text': highlighted_text,
            'matches': len(matches)
        })
    
    except re.error as e:
        return jsonify({
            'highlighted_text': html.escape(text),
            'matches': 0,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
