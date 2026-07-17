from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from services.auth_service import AuthService
from services.report_service import ReportService

# ==========================================
# Blueprint
# ==========================================

auth_bp = Blueprint("auth", __name__)

auth_service = AuthService()
report_service = ReportService()


# ==========================================
# Home Page
# ==========================================

@auth_bp.route("/")
def home():
    return render_template("home.html")


# ==========================================
# Register
# ==========================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        if not full_name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        result = auth_service.register(full_name, email, password)

        if result["success"]:
            flash(result["message"], "success")
            # Log activity
            user = auth_service.login(email, password)
            if user:
                query = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
                report_service.db.execute(query, (user.id, "User Registered"))
            return redirect(url_for("auth.login"))

        flash(result["message"], "danger")

    return render_template("register.html")


# ==========================================
# Login
# ==========================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login an existing user."""
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")

        user = auth_service.login(email, password)

        if user:
            session["user_id"] = user.id
            session["user_name"] = user.full_name
            session["user_role"] = user.role

            # Log activity
            query = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
            report_service.db.execute(query, (user.id, "User Login"))

            flash("Login Successful", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# ==========================================
# Logout
# ==========================================

@auth_bp.route("/logout")
def logout():
    """Logout the current user."""
    if "user_id" in session:
        query = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
        report_service.db.execute(query, (session["user_id"], "User Logout"))

    session.clear()
    flash("Logged Out Successfully", "success")
    return redirect(url_for("auth.login"))


# ==========================================
# Profile
# ==========================================

@auth_bp.route("/profile")
def profile():
    """View user profile."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = auth_service.get_user(session["user_id"])

    # Get user stats
    projects_created = report_service._count_where(
        "projects", "created_by = %s", (session["user_id"],)
    )
    tasks_assigned = report_service._count_where(
        "tasks", "assigned_to = %s", (session["user_id"],)
    )

    return render_template(
        "profile.html",
        user=user,
        projects_created=projects_created,
        tasks_assigned=tasks_assigned
    )


# ==========================================
# Edit Profile
# ==========================================

@auth_bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    """Edit user profile."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = auth_service.get_user(session["user_id"])

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()

        if not full_name or not email:
            flash("Name and email are required.", "danger")
            return render_template("profile_edit.html", user=user)

        query = "UPDATE users SET full_name = %s, email = %s WHERE id = %s"
        report_service.db.execute(query, (full_name, email, session["user_id"]))

        session["user_name"] = full_name
        query2 = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
        report_service.db.execute(query2, (session["user_id"], "Profile Updated"))

        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("profile_edit.html", user=user)


# ==========================================
# Change Password
# ==========================================

@auth_bp.route("/profile/change-password", methods=["GET", "POST"])
def change_password():
    """Change user password."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = auth_service.get_user(session["user_id"])

    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not user.verify_password(current_password):
            flash("Current password is incorrect.", "danger")
            return render_template("change_password.html")

        if len(new_password) < 6:
            flash("New password must be at least 6 characters.", "danger")
            return render_template("change_password.html")

        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("change_password.html")

        from werkzeug.security import generate_password_hash
        hashed = generate_password_hash(new_password)
        query = "UPDATE users SET password = %s WHERE id = %s"
        report_service.db.execute(query, (hashed, session["user_id"]))

        query2 = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
        report_service.db.execute(query2, (session["user_id"], "Password Changed"))

        flash("Password changed successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("change_password.html")
