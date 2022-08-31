from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import current_user,login_required
from . import db
from .models import Questions
from matplotlib.figure import Figure
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

sub = ['LIN','I-M','SP','B-K','MU','NTER','NTRA','NAT']

views = Blueprint('views',__name__)

@views.route('/',methods = ['POST','GET'])
@login_required
def home():
    if request.method == 'POST':
        print(request.form.get('username'))
    return render_template('index.html',user=current_user)

@views.route('/subscribe')
@login_required
def subscription():
    return render_template('subscribe.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('myprofile.html',user=current_user)

@views.route('/forms',methods=['POST','GET'])
@login_required
def forms():
    if len(current_user.qs):
        for i in current_user.qs:
            db.session.delete(i)
            db.session.commit()

    if request.method == "POST":

        for i in range(1,31):
            question = int(i)
            choice = int(request.form.get(f'q{i}'))
            print(question,choice if choice else 1)
            db.session.add(Questions(question = question,choice=choice if choice else 1,student = current_user.id))
            db.session.commit()
        return redirect(url_for('views.home'))

    return render_template('form.html')

@views.route('/analysis')
@login_required
def analysis():
    learn = learning_set()
    return render_template('analysis.html',sub=sub,learn=learn)

@views.route('/contactUs')
@login_required
def contactUs():
    return render_template('contact.html',user=current_user)

@views.route('/education')
@login_required
def education():
    return render_template('Education.html',user=current_user)

@views.route('/career_selection')
def career():
    return render_template('career_selection.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/ask_expert')
def ask_expert():
    return render_template('ask_expert.html')

@views.route('/career_counselling')
def career_counselling():
    return render_template('career_counselling.html')

@views.route('/course')
def course():
    return render_template('course.html')

@views.route('/workshops')
def workshops():
    return render_template('workshops.html')

@views.route('/video')
def video():
    return render_template('video.html')

@views.route('/agora')
def agora():
    return render_template('agora.html')

@views.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(1,31)
    ys = learning()
    axis.plot(xs, ys)
    return fig


class Analysis:
    def ___init__(self):
        qs = current_user.qs
        result = [0 for _ in range(8)]
        for i in qs:
            result[(i.question - 1)%8] += 5*i.choice
        print(result)
        return {i:j for i,j in zip(sub,result)}

def learning():
    qs = current_user.qs
    result = [i.choice for i in qs]
    return result

def learning_set():
    qs = current_user.qs
    learn = [0 for _ in range(8)]
    for i in qs:
        learn[(i.question-1)%8] += 5*i.choice
    return learn