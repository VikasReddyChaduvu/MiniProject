from flask import Flask, render_template, request, redirect
from models import db, Exam, Room, Allocation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_exam", methods=["GET", "POST"])
def add_exam():
    if request.method == "POST":
        subject = request.form["subject"]
        date = request.form["date"]
        time = request.form["time"]
        exam = Exam(subject=subject, date=date, time=time)
        db.session.add(exam)
        db.session.commit()
        return redirect("/")
    return render_template("add_exam.html")

@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        room_number = request.form["room_number"]
        capacity = request.form["capacity"]
        room = Room(room_number=room_number, capacity=capacity)
        db.session.add(room)
        db.session.commit()
        return redirect("/")
    return render_template("add_room.html")

@app.route("/allocate", methods=["GET", "POST"])
def allocate():
    exams = Exam.query.all()
    rooms = Room.query.all()
    if request.method == "POST":
        exam_id = request.form["exam_id"]
        room_id = request.form["room_id"]
        allocation = Allocation(exam_id=exam_id, room_id=room_id)
        db.session.add(allocation)
        db.session.commit()
        return redirect("/schedule")
    return render_template("allocate.html", exams=exams, rooms=rooms)

@app.route("/schedule")
def schedule():
    allocations = Allocation.query.all()
    return render_template("schedule.html", allocations=allocations)

if __name__ == "__main__":
    app.run(debug=True)
