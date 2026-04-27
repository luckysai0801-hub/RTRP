from __future__ import annotations

import csv
import json
import os
from copy import deepcopy
from datetime import datetime
from io import StringIO
from pathlib import Path

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    Response,
    session,
    url_for,
)
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "campus-connect-dev-secret")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "students.json"

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")


def create_student(
    name: str,
    roll_number: str,
    email: str,
    password: str,
    department: str,
    semester: str,
    skill_score: int,
    projects: int,
    reels: int,
    mentors: int,
    endorsements: int,
    profile_views: int,
    reel_views: int,
    status: str,
    badges: list[str],
    skills: list[dict],
    recent_activity: list[dict],
    upcoming: list[dict],
    portfolio: list[dict],
) -> dict:
    initials = "".join(part[0] for part in name.split()[:2]).upper()
    now = datetime.utcnow().isoformat()
    return {
        "name": name,
        "roll_number": roll_number.upper(),
        "email": email.lower(),
        "password_hash": generate_password_hash(password),
        "department": department,
        "semester": semester,
        "skill_score": skill_score,
        "projects": projects,
        "reels": reels,
        "mentors": mentors,
        "endorsements": endorsements,
        "profile_views": profile_views,
        "reel_views": reel_views,
        "status": status,
        "institution": "Guru Nanak Institutions Technical Campus",
        "academic_year": "2024-2025",
        "initials": initials,
        "headline": "Building skills, proof-of-work, and campus visibility.",
        "badges": badges,
        "skills": skills,
        "recent_activity": recent_activity,
        "upcoming": upcoming,
        "portfolio": portfolio,
        "created_at": now,
        "updated_at": now,
    }


def seed_students() -> list[dict]:
    return [
        create_student(
            name="K. Asmitha",
            roll_number="24WJ1A6201",
            email="asmitha@gnitc.ac.in",
            password="Asmitha@123",
            department="CSE - Cyber Security",
            semester="Semester IV",
            skill_score=85,
            projects=3,
            reels=5,
            mentors=2,
            endorsements=7,
            profile_views=48,
            reel_views=312,
            status="Active",
            badges=["First Uploader", "Reel Creator", "Mentor Connect", "Score Climber"],
            skills=[
                {"name": "Python", "score": 80, "color": "linear-gradient(90deg, #1E2761, #4a6cf7)"},
                {"name": "Web Development", "score": 75, "color": "linear-gradient(90deg, #7a5af8, #4a6cf7)"},
                {"name": "DSA", "score": 65, "color": "linear-gradient(90deg, #10b981, #4a6cf7)"},
                {"name": "Communication", "score": 70, "color": "linear-gradient(90deg, #f59e0b, #ef4444)"},
                {"name": "Cyber Security", "score": 72, "color": "linear-gradient(90deg, #ef4444, #7a5af8)"},
            ],
            recent_activity=[
                {
                    "icon": "folder",
                    "title": "Uploaded project: Campus Career Platform",
                    "subtitle": "Tech Stack: Python, Flask, MongoDB, HTML/CSS/JS",
                    "time": "Today, 9:30 AM",
                },
                {
                    "icon": "video",
                    "title": "Watched skill reel: Python Basics for Beginners",
                    "subtitle": "Posted by Ravi Teja · 1,200 views",
                    "time": "Yesterday, 7:45 PM",
                },
                {
                    "icon": "mentor",
                    "title": "Connected with mentor: Mr. Chaitanya Kumar",
                    "subtitle": "Assistant Professor, CSE - Cyber Security",
                    "time": "Apr 15, 2026",
                },
                {
                    "icon": "badge",
                    "title": "Earned badge: First Project Uploader",
                    "subtitle": "Recognition for publishing a verified campus project.",
                    "time": "Apr 14, 2026",
                },
            ],
            upcoming=[
                {"title": "Mentor Session", "subtitle": "Mr. Chaitanya Kumar · Apr 26, 4:00 PM"},
                {"title": "Project Submission", "subtitle": "Campus Platform · Apr 29, 11:59 PM"},
            ],
            portfolio=[
                {
                    "title": "Campus Career Networking Platform",
                    "description": "A campus-exclusive networking application with skill tracking, mentor visibility, and analytics-driven reports.",
                    "status": "Completed",
                    "stack": ["Python", "Flask", "MongoDB", "HTML/CSS/JS", "REST API"],
                },
                {
                    "title": "Student Attendance Management System",
                    "description": "An attendance tracker for faculty with low-attendance alerts and downloadable reports.",
                    "status": "In Progress",
                    "stack": ["Python", "Django", "SQLite", "Bootstrap"],
                },
                {
                    "title": "Cyber Security Threat Detection Dashboard",
                    "description": "A lab dashboard that visualizes suspicious activity and firewall events for classroom simulations.",
                    "status": "Completed",
                    "stack": ["Python", "Pandas", "Matplotlib", "Scapy", "HTML/JS"],
                },
            ],
        ),
        create_student(
            name="K. Sri Sai Sharanya",
            roll_number="24WJ1A6202",
            email="srisai@gnitc.ac.in",
            password="Sharanya@123",
            department="CSE - Cyber Security",
            semester="Semester IV",
            skill_score=78,
            projects=2,
            reels=4,
            mentors=1,
            endorsements=5,
            profile_views=34,
            reel_views=208,
            status="Active",
            badges=["Frontend Builder", "Mentor Ready"],
            skills=[
                {"name": "Python", "score": 74, "color": "linear-gradient(90deg, #1E2761, #4a6cf7)"},
                {"name": "Web Development", "score": 81, "color": "linear-gradient(90deg, #7a5af8, #4a6cf7)"},
                {"name": "DSA", "score": 68, "color": "linear-gradient(90deg, #10b981, #4a6cf7)"},
                {"name": "Communication", "score": 72, "color": "linear-gradient(90deg, #f59e0b, #ef4444)"},
            ],
            recent_activity=[
                {
                    "icon": "folder",
                    "title": "Uploaded project: Placement Prep Tracker",
                    "subtitle": "Tracks coding rounds, resume tasks, and mock interviews.",
                    "time": "Today, 8:00 AM",
                },
                {
                    "icon": "video",
                    "title": "Posted reel: HTML Portfolio Tips",
                    "subtitle": "Reached 870 views in two days.",
                    "time": "Apr 22, 2026",
                },
            ],
            upcoming=[
                {"title": "Resume Review", "subtitle": "Faculty panel · Apr 27, 2:00 PM"},
                {"title": "Mock Interview", "subtitle": "Aptitude and HR practice · Apr 30, 10:00 AM"},
            ],
            portfolio=[
                {
                    "title": "Placement Prep Tracker",
                    "description": "Helps students track resume tasks, coding sheets, and interview milestones in one workflow.",
                    "status": "Completed",
                    "stack": ["Flask", "SQLite", "Bootstrap"],
                },
                {
                    "title": "Portfolio Builder",
                    "description": "A responsive builder for personal academic portfolios with project highlights.",
                    "status": "In Progress",
                    "stack": ["HTML", "CSS", "JavaScript"],
                },
            ],
        ),
        create_student(
            name="K. Manideepika",
            roll_number="24WJ1A6203",
            email="manideepika@gnitc.ac.in",
            password="Manideepika@123",
            department="CSE - Cyber Security",
            semester="Semester IV",
            skill_score=91,
            projects=4,
            reels=7,
            mentors=3,
            endorsements=11,
            profile_views=61,
            reel_views=420,
            status="Active",
            badges=["Top Performer", "Reel Creator", "Mentor Connect"],
            skills=[
                {"name": "Python", "score": 89, "color": "linear-gradient(90deg, #1E2761, #4a6cf7)"},
                {"name": "Web Development", "score": 84, "color": "linear-gradient(90deg, #7a5af8, #4a6cf7)"},
                {"name": "DSA", "score": 86, "color": "linear-gradient(90deg, #10b981, #4a6cf7)"},
                {"name": "Communication", "score": 79, "color": "linear-gradient(90deg, #f59e0b, #ef4444)"},
                {"name": "Cyber Security", "score": 88, "color": "linear-gradient(90deg, #ef4444, #7a5af8)"},
            ],
            recent_activity=[
                {
                    "icon": "badge",
                    "title": "Skill score updated: 88 to 91",
                    "subtitle": "Improved after mentor validation and project review.",
                    "time": "Today, 11:10 AM",
                }
            ],
            upcoming=[
                {"title": "Hackathon Demo", "subtitle": "Department innovation cell · Apr 28, 1:00 PM"},
            ],
            portfolio=[
                {
                    "title": "Threat Detection Dashboard",
                    "description": "An analytics dashboard to inspect attack patterns and anomaly spikes.",
                    "status": "Completed",
                    "stack": ["Flask", "Chart.js", "Pandas"],
                }
            ],
        ),
        create_student(
            name="P. Ravi Teja",
            roll_number="24WJ1A6204",
            email="raviteja@gnitc.ac.in",
            password="Raviteja@123",
            department="CSE - Cyber Security",
            semester="Semester IV",
            skill_score=70,
            projects=1,
            reels=2,
            mentors=1,
            endorsements=3,
            profile_views=21,
            reel_views=143,
            status="Inactive",
            badges=["Quick Learner"],
            skills=[
                {"name": "Python", "score": 68, "color": "linear-gradient(90deg, #1E2761, #4a6cf7)"},
                {"name": "Web Development", "score": 62, "color": "linear-gradient(90deg, #7a5af8, #4a6cf7)"},
                {"name": "DSA", "score": 64, "color": "linear-gradient(90deg, #10b981, #4a6cf7)"},
            ],
            recent_activity=[
                {
                    "icon": "video",
                    "title": "Posted reel: Python Basics for Beginners",
                    "subtitle": "Beginner-friendly recap of Python loops and functions.",
                    "time": "Apr 20, 2026",
                }
            ],
            upcoming=[
                {"title": "Skill Review", "subtitle": "Faculty mentor follow-up · May 1, 9:00 AM"},
            ],
            portfolio=[
                {
                    "title": "Python Basics Reel Series",
                    "description": "A short-form reel playlist covering Python basics for first-year students.",
                    "status": "Completed",
                    "stack": ["Python", "Canva", "Video Editing"],
                }
            ],
        ),
        create_student(
            name="S. Lakshmi Priya",
            roll_number="24WJ1A6205",
            email="lakshmi@gnitc.ac.in",
            password="Lakshmi@123",
            department="CSE - Cyber Security",
            semester="Semester IV",
            skill_score=88,
            projects=5,
            reels=6,
            mentors=2,
            endorsements=9,
            profile_views=57,
            reel_views=398,
            status="Active",
            badges=["Project Lead", "Score Climber", "Campus Star"],
            skills=[
                {"name": "Python", "score": 84, "color": "linear-gradient(90deg, #1E2761, #4a6cf7)"},
                {"name": "Web Development", "score": 82, "color": "linear-gradient(90deg, #7a5af8, #4a6cf7)"},
                {"name": "DSA", "score": 76, "color": "linear-gradient(90deg, #10b981, #4a6cf7)"},
                {"name": "Communication", "score": 81, "color": "linear-gradient(90deg, #f59e0b, #ef4444)"},
            ],
            recent_activity=[
                {
                    "icon": "folder",
                    "title": "Uploaded project: Interview Experience Hub",
                    "subtitle": "A platform for juniors to learn from campus placement stories.",
                    "time": "Apr 23, 2026",
                }
            ],
            upcoming=[
                {"title": "Mentor Connect", "subtitle": "Alumni session · Apr 30, 3:30 PM"},
            ],
            portfolio=[
                {
                    "title": "Interview Experience Hub",
                    "description": "Collects and categorizes campus placement experiences with filters by role and company.",
                    "status": "Completed",
                    "stack": ["Flask", "MongoDB", "JavaScript"],
                },
                {
                    "title": "Resume Score Analyzer",
                    "description": "Analyzes resume structure and keyword coverage for student applications.",
                    "status": "Completed",
                    "stack": ["Python", "NLP", "Bootstrap"],
                },
            ],
        ),
    ]


def ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        DATA_FILE.write_text(json.dumps(seed_students(), indent=2), encoding="utf-8")


def load_students() -> list[dict]:
    ensure_data_file()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        DATA_FILE.write_text(json.dumps(seed_students(), indent=2), encoding="utf-8")
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_students(students: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(students, indent=2), encoding="utf-8")


def get_sorted_students() -> list[dict]:
    students = load_students()
    students.sort(key=lambda item: item.get("skill_score", 0), reverse=True)
    return students


def serialize_student(student: dict, include_private: bool = False) -> dict:
    safe_student = deepcopy(student)
    if not include_private:
        safe_student.pop("password_hash", None)
    return safe_student


def get_student_by_roll(roll_number: str | None) -> dict | None:
    if not roll_number:
        return None
    roll_number = roll_number.upper()
    for student in load_students():
        if student["roll_number"] == roll_number:
            return student
    return None


def get_student_by_email(email: str | None) -> dict | None:
    if not email:
        return None
    email = email.lower()
    for student in load_students():
        if student["email"] == email:
            return student
    return None


def current_student() -> dict | None:
    return get_student_by_roll(session.get("student_roll"))


def timestamp_label() -> str:
    return datetime.now().strftime("%b %d, %Y - %I:%M %p")


def add_recent_activity(student: dict, icon: str, title: str, subtitle: str) -> None:
    student.setdefault("recent_activity", [])
    student["recent_activity"].insert(
        0,
        {
            "icon": icon,
            "title": title,
            "subtitle": subtitle,
            "time": timestamp_label(),
        },
    )
    student["recent_activity"] = student["recent_activity"][:6]


def ensure_badge(student: dict, badge_name: str) -> None:
    student.setdefault("badges", [])
    if badge_name not in student["badges"]:
        student["badges"].append(badge_name)


def recalculate_student_metrics(student: dict) -> None:
    projects = len(student.get("portfolio", []))
    reels = max(student.get("reels", 0), min(8, max(0, projects + 2)))
    mentors = max(student.get("mentors", 0), 1 if projects else 0)
    endorsements = max(student.get("endorsements", 0), projects * 2 + mentors)

    skill_items = student.get("skills", [])
    if skill_items:
        average_skill = sum(item.get("score", 0) for item in skill_items) / len(skill_items)
    else:
        average_skill = 50

    score = round(min(98, average_skill * 0.65 + projects * 4 + reels * 1.4 + mentors * 2.2))

    student["projects"] = projects
    student["reels"] = reels
    student["mentors"] = mentors
    student["endorsements"] = endorsements
    student["skill_score"] = max(score, 55)
    student["status"] = "Active" if projects or reels or mentors else "Inactive"
    student["updated_at"] = datetime.utcnow().isoformat()

    if projects >= 1:
        ensure_badge(student, "Project Publisher")
    if projects >= 3:
        ensure_badge(student, "Portfolio Builder")
    if student["skill_score"] >= 85:
        ensure_badge(student, "Score Climber")


def update_student_record(roll_number: str, updater) -> dict | None:
    students = load_students()
    for student in students:
        if student["roll_number"] == roll_number:
            updater(student)
            student["updated_at"] = datetime.utcnow().isoformat()
            save_students(students)
            return student
    return None


def calculate_profile_completion(student: dict) -> int:
    checks = [
        bool(student.get("headline")),
        bool(student.get("skills")),
        bool(student.get("portfolio")),
        bool(student.get("upcoming")),
        bool(student.get("recent_activity")),
        bool(student.get("badges")),
    ]
    return round((sum(checks) / len(checks)) * 100)


def calculate_summary(students: list[dict]) -> dict:
    total_students = len(students)
    active_students = sum(1 for student in students if student.get("status") == "Active")
    total_projects = sum(student.get("projects", 0) for student in students)
    total_reels = sum(student.get("reels", 0) for student in students)
    mentor_sessions = sum(student.get("mentors", 0) for student in students)
    avg_skill_score = round(
        sum(student.get("skill_score", 0) for student in students) / total_students, 1
    ) if total_students else 0
    return {
        "total_students": total_students,
        "active_students": active_students,
        "total_projects": total_projects,
        "total_reels": total_reels,
        "mentor_sessions": mentor_sessions,
        "avg_skill_score": avg_skill_score,
    }


def score_band(score: int) -> str:
    if score >= 85:
        return "high"
    if score >= 70:
        return "mid"
    return "low"


def status_badge(status: str) -> str:
    return "success" if status == "Active" else "warning"


try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.server_info()
    print("[OK] MongoDB connected successfully.")
except ConnectionFailure:
    client = None
    print("[WARN] MongoDB not reachable. Using local JSON data store.")


@app.context_processor
def inject_globals():
    student = current_student()
    return {
        "logged_in_student": serialize_student(student) if student else None,
        "score_band": score_band,
        "status_badge": status_badge,
        "profile_completion": calculate_profile_completion(student) if student else 0,
    }


@app.route("/")
def index():
    students = get_sorted_students()
    summary = calculate_summary(students)
    top_students = [serialize_student(student) for student in students[:3]]
    return render_template("index.html", summary=summary, top_students=top_students)


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login_page():
    if current_student():
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/dashboard")
def dashboard():
    student = current_student()
    if not student:
        return redirect(url_for("login_page"))
    student_data = serialize_student(student)
    student_data["profile_completion"] = calculate_profile_completion(student)
    return render_template("dashboard.html", student=student_data)


@app.route("/reports")
def reports():
    students = [serialize_student(student) for student in get_sorted_students()]
    summary = calculate_summary(students)
    return render_template("reports.html", students=students, summary=summary)


@app.route("/view_reports")
def view_reports():
    requested_roll = request.args.get("student")
    student = get_student_by_roll(requested_roll) if requested_roll else current_student()
    if not student:
        students = get_sorted_students()
        student = students[0] if students else None
    if not student:
        return redirect(url_for("reports"))
    return render_template("view_reports.html", student=serialize_student(student))


@app.route("/login", methods=["POST"])
def login_api():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    student = get_student_by_email(email)
    if not student or not check_password_hash(student["password_hash"], password):
        return jsonify({"status": "error", "message": "Invalid email or password."}), 401

    session["student_roll"] = student["roll_number"]
    return jsonify(
        {
            "status": "success",
            "message": "Login successful.",
            "redirect": url_for("dashboard"),
        }
    )


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    roll_number = data.get("roll_number", "").strip().upper()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not all([name, roll_number, email, password]):
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    if not email.endswith("@gnitc.ac.in"):
        return jsonify(
            {"status": "error", "message": "Use your institutional email address."}
        ), 400

    if len(password) < 8:
        return jsonify(
            {"status": "error", "message": "Password must be at least 8 characters long."}
        ), 400

    students = load_students()
    if any(student["email"] == email for student in students):
        return jsonify({"status": "error", "message": "An account already exists for this email."}), 409

    if any(student["roll_number"] == roll_number for student in students):
        return jsonify({"status": "error", "message": "Roll number is already registered."}), 409

    new_student = create_student(
        name=name,
        roll_number=roll_number,
        email=email,
        password=password,
        department="CSE - Cyber Security",
        semester="Semester IV",
        skill_score=60,
        projects=0,
        reels=0,
        mentors=0,
        endorsements=0,
        profile_views=0,
        reel_views=0,
        status="Active",
        badges=["New Joiner"],
        skills=[
            {"name": "Python", "score": 55, "color": "linear-gradient(90deg, #1E2761, #4a6cf7)"},
            {"name": "Web Development", "score": 50, "color": "linear-gradient(90deg, #7a5af8, #4a6cf7)"},
            {"name": "Communication", "score": 62, "color": "linear-gradient(90deg, #f59e0b, #ef4444)"},
        ],
        recent_activity=[
            {
                "icon": "badge",
                "title": "Joined CampusConnect",
                "subtitle": "Profile created successfully. Start uploading your work.",
                "time": "Today",
            }
        ],
        upcoming=[
            {"title": "Profile Setup", "subtitle": "Add projects and reels to improve visibility."},
        ],
        portfolio=[],
    )

    students.append(new_student)
    save_students(students)
    return jsonify(
        {
            "status": "success",
            "message": "Account created successfully.",
            "redirect": url_for("login_page"),
        }
    )


@app.route("/api/profile", methods=["POST"])
def update_profile():
    student = current_student()
    if not student:
        return jsonify({"status": "error", "message": "Login required."}), 401

    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    headline = data.get("headline", "").strip()
    department = data.get("department", "").strip()
    semester = data.get("semester", "").strip()
    skills_input = data.get("skills", "")

    if not all([name, headline, department, semester]):
        return jsonify({"status": "error", "message": "All profile fields are required."}), 400

    skill_names = [item.strip() for item in skills_input.split(",") if item.strip()]
    if not skill_names:
        return jsonify({"status": "error", "message": "Add at least one skill."}), 400

    def updater(record: dict) -> None:
        record["name"] = name
        record["headline"] = headline
        record["department"] = department
        record["semester"] = semester
        record["initials"] = "".join(part[0] for part in name.split()[:2]).upper()
        palette = [
            "linear-gradient(90deg, #1E2761, #4a6cf7)",
            "linear-gradient(90deg, #7a5af8, #4a6cf7)",
            "linear-gradient(90deg, #10b981, #4a6cf7)",
            "linear-gradient(90deg, #f59e0b, #ef4444)",
            "linear-gradient(90deg, #ef4444, #7a5af8)",
        ]
        existing_scores = {item["name"].lower(): item.get("score", 60) for item in record.get("skills", [])}
        record["skills"] = [
            {
                "name": skill_name,
                "score": existing_scores.get(skill_name.lower(), min(92, 58 + index * 6)),
                "color": palette[index % len(palette)],
            }
            for index, skill_name in enumerate(skill_names)
        ]
        ensure_badge(record, "Profile Optimized")
        add_recent_activity(record, "badge", "Updated profile details", "Refreshed headline, department, semester, and skills.")
        recalculate_student_metrics(record)

    updated = update_student_record(student["roll_number"], updater)
    if not updated:
        return jsonify({"status": "error", "message": "Student profile not found."}), 404

    return jsonify(
        {
            "status": "success",
            "message": "Profile updated successfully.",
            "student": serialize_student(updated),
        }
    )


@app.route("/api/projects", methods=["POST"])
def add_project():
    student = current_student()
    if not student:
        return jsonify({"status": "error", "message": "Login required."}), 401

    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    stack_raw = data.get("stack", "").strip()
    status = data.get("status", "").strip() or "In Progress"

    if not all([title, description, stack_raw]):
        return jsonify({"status": "error", "message": "Project title, description, and stack are required."}), 400

    stack = [item.strip() for item in stack_raw.split(",") if item.strip()]
    if not stack:
        return jsonify({"status": "error", "message": "Add at least one technology in the stack."}), 400

    def updater(record: dict) -> None:
        record.setdefault("portfolio", [])
        record["portfolio"].insert(
            0,
            {
                "title": title,
                "description": description,
                "status": status,
                "stack": stack,
            },
        )
        add_recent_activity(record, "folder", f"Uploaded project: {title}", f"Stack: {', '.join(stack[:4])}")
        ensure_badge(record, "Project Publisher")
        record["profile_views"] = record.get("profile_views", 0) + 8
        record["reel_views"] = record.get("reel_views", 0) + 25
        recalculate_student_metrics(record)

    updated = update_student_record(student["roll_number"], updater)
    if not updated:
        return jsonify({"status": "error", "message": "Student profile not found."}), 404

    return jsonify(
        {
            "status": "success",
            "message": "Project added successfully.",
            "student": serialize_student(updated),
        }
    )


@app.route("/get_reports")
def get_reports():
    full_students = get_sorted_students()
    students = [
        {
            "name": student["name"],
            "roll_number": student["roll_number"],
            "department": student["department"],
            "skill_score": student["skill_score"],
            "projects": student["projects"],
            "reels": student["reels"],
            "status": student["status"],
            "view_url": url_for("view_reports", student=student["roll_number"]),
        }
        for student in full_students
    ]
    return jsonify({"status": "success", "data": students, "summary": calculate_summary(full_students)})


@app.route("/export/reports.csv")
def export_reports():
    students = get_sorted_students()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["Rank", "Name", "Roll Number", "Department", "Skill Score", "Projects", "Reels", "Status"]
    )
    for index, student in enumerate(students, start=1):
        writer.writerow(
            [
                index,
                student["name"],
                student["roll_number"],
                student["department"],
                student["skill_score"],
                student["projects"],
                student["reels"],
                student["status"],
            ]
        )
    csv_content = output.getvalue()
    output.close()
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=campusconnect_reports.csv"},
    )


if __name__ == "__main__":
    ensure_data_file()
    app.run(debug=True, port=5000)
