from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)

class Todo_N(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    completed=db.Column(db.Boolean,default=False)

    def __repr__(self):
        return f"<Task {self.content}>"
@app.route("/",methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo_N(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding your task'
    else:
        tasks=Todo_N.query.order_by(Todo_N.timestamp).all()
        return render_template("index.html",tasks=tasks)


@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    
    task=Todo_N.query.get_or_404(id)

    if request.method=='POST':  
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was some issue updating your task"
    else:
        return render_template('update.html',task=task)

@app.route('/delete/<int:id>',methods=['POST','GET'])
def delete(id):
    
    delete_task=Todo_N.query.get_or_404(id)

    try :
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem in delete route'



    return render_template('update.html',rewrite_task=rewrite_task)




if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)