from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/graph/')
def graph_html():
  return render_template('generatedgraph.html')

if __name__ == '__main__':
  app.run()
