
import tkinter as tk
from tkinter import messagebox
import secrets
import time
import os
from datetime import datetime

# ---------------- SECURITY SETTINGS ----------------

USERNAME = "admin"
PASSWORD = "1234"

MAX_LOGIN_ATTEMPTS = 5
MAX_OTP_ATTEMPTS = 3
OTP_VALIDITY = 120

otp = ""
otp_time = 0
login_attempts = 0
otp_attempts = 0
total_failed_logins = 0
unauthorized_attempts = 0
account_locked = False

LOG_FILE = "security_log.txt"


# ---------------- SECURITY LOGGING ----------------

def log_event(event):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"[{current_time}] {event}\n")


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Two Factor Authentication System")
root.geometry("420x430")
root.resizable(False, False)
root.configure(bg="#202A44")


# ---------------- LOGIN FUNCTION ----------------

def login():

    global login_attempts
    global total_failed_logins
    global unauthorized_attempts
    global account_locked

    if account_locked:
        messagebox.showerror("Account Locked",
                             "Account is locked!")
        return

    username = username_entry.get()
    password = password_entry.get()

    if username == USERNAME and password == PASSWORD:

        log_event("Successful password verification")

        messagebox.showinfo(
            "Login",
            "Login Successful!\nOTP will be generated."
        )

        root.withdraw()
        generate_otp()

    else:

        login_attempts += 1
        total_failed_logins += 1
        unauthorized_attempts += 1

        log_event(
            f"Unauthorized login attempt #{login_attempts}"
        )

        remaining = MAX_LOGIN_ATTEMPTS - login_attempts

        if login_attempts >= MAX_LOGIN_ATTEMPTS:

            account_locked = True

            log_event("Account locked after 5 failed login attempts")

            messagebox.showerror(
                "Account Locked",
                "Maximum failed login attempts reached.\n"
                "Account has been locked."
            )

            login_button.config(state="disabled")

        else:

            messagebox.showerror(
                "Login Failed",
                f"Invalid Username or Password\n"
                f"Attempts remaining: {remaining}"
            )


# ---------------- OTP GENERATION ----------------

def generate_otp():

    global otp, otp_time, otp_attempts

    otp = str(secrets.randbelow(900000) + 100000)
    otp_time = time.time()
    otp_attempts = 0

    log_event("New OTP generated")

    messagebox.showinfo(
        "OTP Generated",
        f"Your Demo OTP is: {otp}\n\n"
        "OTP is valid for 2 minutes."
    )

    open_otp_window()


# ---------------- OTP WINDOW ----------------

def open_otp_window():

    otp_window = tk.Toplevel(root)
    otp_window.title("OTP Verification")
    otp_window.geometry("420x350")
    otp_window.resizable(False, False)
    otp_window.configure(bg="#202A44")

    tk.Label(
        otp_window,
        text="TWO FACTOR AUTHENTICATION",
        font=("Arial", 15, "bold"),
        bg="#202A44",
        fg="white"
    ).pack(pady=20)

    tk.Label(
        otp_window,
        text="Enter Your 6 Digit OTP",
        font=("Arial", 12),
        bg="#202A44",
        fg="white"
    ).pack(pady=10)

    otp_entry = tk.Entry(
        otp_window,
        font=("Arial", 16),
        justify="center",
        width=15
    )
    otp_entry.pack(pady=10)

    def verify_otp():

        global otp_attempts

        entered_otp = otp_entry.get()

        if time.time() - otp_time > OTP_VALIDITY:

            log_event("OTP verification failed: OTP expired")

            messagebox.showerror(
                "Expired",
                "OTP Expired! Please resend OTP."
            )
            return

        if otp_attempts >= MAX_OTP_ATTEMPTS:

            messagebox.showerror(
                "Blocked",
                "Maximum OTP attempts reached."
            )

            log_event("OTP verification blocked")

            otp_window.destroy()
            root.deiconify()
            return

        if entered_otp == otp:

            log_event("OTP verified successfully")

            messagebox.showinfo(
                "Success",
                "OTP Verified Successfully!\n"
                "Welcome to the Secure System."
            )

            otp_window.destroy()
            open_dashboard()

        else:

            otp_attempts += 1

            log_event(
                f"Incorrect OTP attempt #{otp_attempts}"
            )

            remaining = MAX_OTP_ATTEMPTS - otp_attempts

            messagebox.showerror(
                "Invalid OTP",
                f"Wrong OTP!\n"
                f"Attempts remaining: {remaining}"
            )

            if otp_attempts >= MAX_OTP_ATTEMPTS:

                log_event("Maximum OTP attempts reached")

                messagebox.showwarning(
                    "OTP Blocked",
                    "Maximum OTP attempts reached.\n"
                    "Please login again."
                )

                otp_window.destroy()
                root.deiconify()

    tk.Button(
        otp_window,
        text="VERIFY OTP",
        font=("Arial", 12, "bold"),
        bg="#00C853",
        fg="white",
        width=18,
        command=verify_otp
    ).pack(pady=15)

    tk.Button(
        otp_window,
        text="RESEND OTP",
        font=("Arial", 10, "bold"),
        bg="#2196F3",
        fg="white",
        width=18,
        command=lambda: resend_otp(otp_window)
    ).pack(pady=5)

    otp_entry.focus_set()


# ---------------- RESEND OTP ----------------

def resend_otp(window):

    window.destroy()
    generate_otp()


# ---------------- ADMIN DASHBOARD ----------------

def open_dashboard():

    dashboard = tk.Toplevel(root)
    dashboard.title("Admin Security Dashboard")
    dashboard.geometry("550x520")
    dashboard.resizable(False, False)
    dashboard.configure(bg="#202A44")

    tk.Label(
        dashboard,
        text="ADMIN SECURITY DASHBOARD",
        font=("Arial", 18, "bold"),
        bg="#202A44",
        fg="white"
    ).pack(pady=20)

    stats_frame = tk.Frame(
        dashboard,
        bg="#2D3B5B"
    )
    stats_frame.pack(padx=20, pady=10, fill="x")

    failed_label = tk.Label(
        stats_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#2D3B5B",
        fg="white"
    )
    failed_label.pack(pady=10)

    unauthorized_label = tk.Label(
        stats_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#2D3B5B",
        fg="white"
    )
    unauthorized_label.pack(pady=10)

    lock_label = tk.Label(
        stats_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#2D3B5B",
        fg="white"
    )
    lock_label.pack(pady=10)

    otp_label = tk.Label(
        stats_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#2D3B5B",
        fg="white"
    )
    otp_label.pack(pady=10)

    def refresh_dashboard():

        failed_label.config(
            text=f"Total Failed Login Attempts: {total_failed_logins}"
        )

        unauthorized_label.config(
            text=f"Unauthorized Access Attempts: {unauthorized_attempts}"
        )

        lock_status = "LOCKED" if account_locked else "ACTIVE"

        lock_label.config(
            text=f"Account Status: {lock_status}"
        )

        otp_label.config(
            text=f"OTP Attempts (Current Session): {otp_attempts}"
        )

    def view_logs():

        log_window = tk.Toplevel(dashboard)
        log_window.title("Security Event Logs")
        log_window.geometry("500x350")
        log_window.configure(bg="#202A44")

        tk.Label(
            log_window,
            text="SECURITY EVENT LOGS",
            font=("Arial", 14, "bold"),
            bg="#202A44",
            fg="white"
        ).pack(pady=10)

        log_text = tk.Text(
            log_window,
            width=58,
            height=16,
            font=("Consolas", 9)
        )
        log_text.pack(padx=10, pady=10)

        if os.path.exists(LOG_FILE):

            with open(LOG_FILE, "r") as file:
                log_text.insert("1.0", file.read())

        else:
            log_text.insert("1.0", "No security events recorded.")

        log_text.config(state="disabled")

    tk.Button(
        dashboard,
        text="REFRESH DASHBOARD",
        font=("Arial", 11, "bold"),
        bg="#00C853",
        fg="white",
        width=23,
        command=refresh_dashboard
    ).pack(pady=12)

    tk.Button(
        dashboard,
        text="VIEW SECURITY LOGS",
        font=("Arial", 11, "bold"),
        bg="#2196F3",
        fg="white",
        width=23,
        command=view_logs
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="EXIT SYSTEM",
        font=("Arial", 11, "bold"),
        bg="#E53935",
        fg="white",
        width=23,
        command=root.destroy
    ).pack(pady=8)

    refresh_dashboard()


# ---------------- LOGIN GUI DESIGN ----------------

tk.Label(
    root,
    text="SECURE LOGIN SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#202A44",
    fg="white"
).pack(pady=30)

tk.Label(
    root,
    text="Username",
    font=("Arial", 12),
    bg="#202A44",
    fg="white"
).pack()

username_entry = tk.Entry(
    root,
    font=("Arial", 12),
    width=25
)
username_entry.pack(pady=8)

tk.Label(
    root,
    text="Password",
    font=("Arial", 12),
    bg="#202A44",
    fg="white"
).pack()

password_entry = tk.Entry(
    root,
    font=("Arial", 12),
    width=25,
    show="*"
)
password_entry.pack(pady=8)

login_button = tk.Button(
    root,
    text="LOGIN",
    font=("Arial", 12, "bold"),
    bg="#00C853",
    fg="white",
    width=18,
    command=login
)
login_button.pack(pady=25)

root.mainloop()
