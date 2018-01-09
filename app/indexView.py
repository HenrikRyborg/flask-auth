from flask import render_template, Blueprint

indexBP = Blueprint('indexBP', __name__)

# indexView
@indexBP.route('/', methods=['GET','POST'])
def indexView():
    
    return render_template('index.html')