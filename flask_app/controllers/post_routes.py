from flask_app import app
from flask_app.models import user_model, post_model
from flask import render_template,redirect,request,session,flash


@app.route('/post/message')
def message_form():
    if 'user_id' in session:
        return render_template('msg_form.html')
    return redirect('/home')

@app.route('/post/message', methods = ['POST'])
def submit_post():
    
    if not post_model.Post.validate_post(request.form):
        return redirect('/post/message')
    
    post_data = {
        'user_id':session['user_id'],
        'post_title':request.form['post_title'],
        'post_content':request.form['post_content'],
        'date_posted':request.form['date_posted']
    }
    
    post_model.Post.save(post_data)
    return redirect('/dashboard')

@app.route('/view/post/<int:id>')
def view_post(id):
    return render_template('view_post.html', post = post_model.Post.get_post_by_id(id))

@app.route('/edit/post/<int:id>')
def edit_form(id):
    if 'user_id' in session:
        post = post_model.Post.get_post_by_id(id)
        
        if session['user_id'] == post.created_by.id:
            return render_template('edit_post.html', post = post_model.Post.get_post_by_id(id))
        return redirect('/dashboard')
    return redirect('/home')
    
@app.route('/edit/post', methods = ['POST'])
def edit_post():
    post_id = request.form['id']
    if not post_model.Post.validate_post(request.form):
        return redirect(f'/edit/post/{post_id}')
    
    post_model.Post.edit(request.form)
    
    return redirect('/dashboard')

@app.route('/delete/post/<int:id>')
def delete_post(id):
    post_model.Post.delete(id)
    return redirect('/dashboard')