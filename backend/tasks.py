from celery import shared_task
from datetime import datetime, timedelta
from models import Appointment, Patient
from extensions import db

@shared_task
def send_daily_reminders():
    today = datetime.utcnow().date()
    print(f"Checking for appointments on {today}...")
    
    appointments = Appointment.query.filter_by(date=today, status="Booked").all()
    
    if not appointments:
        print("No appointments found for today.")
        return

    for appt in appointments:
        patient = appt.patient
        if patient and patient.user:
            message = (
                f"Reminder: Dear {patient.user.name}, you have an appointment scheduled "
                f"with Dr. {appt.doctor.user.name} today at {appt.time}. "
                f"Please visit LifeSync Hospital."
            )
            # In a real app, you would send SMS or Email here.
            # For now, we simulate it by printing to the console/logs.
            print(f"[ALERT] Sending to {patient.user.email}: {message}")

@shared_task
def send_monthly_reports():
    # Calculate previous month range
    today = datetime.utcnow().date()
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)
    
    print(f"Generating monthly reports for {first_day_prev_month} to {last_day_prev_month}...")
    
    from models import Doctor, Treatment # Import here to avoid circular imports if any
    
    doctors = Doctor.query.all()
    
    for doctor in doctors:
        # Find completed appointments for this doctor in the date range
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status == "Completed",
            Appointment.date >= first_day_prev_month,
            Appointment.date <= last_day_prev_month
        ).all()
        
        if not appointments:
            print(f"No completed appointments for Dr. {doctor.user.name} last month.")
            continue
            
        # Generate HTML Report
        html_content = f"""
        <html>
        <body>
            <h1>Monthly Activity Report</h1>
            <p><strong>Doctor:</strong> Dr. {doctor.user.name}</p>
            <p><strong>Month:</strong> {first_day_prev_month.strftime('%B %Y')}</p>
            <p><strong>Total Completed Appointments:</strong> {len(appointments)}</p>
            
            <table border="1" cellpadding="5" cellspacing="0">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Patient Name</th>
                        <th>Diagnosis</th>
                        <th>Treatment/Medicines</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for appt in appointments:
            # Fetch treatment details if available
            treatment = Treatment.query.filter_by(appointment_id=appt.id).first()
            diagnosis = treatment.diagnosis if treatment else "N/A"
            medicines = treatment.medicines if treatment else "N/A"
            
            html_content += f"""
                    <tr>
                        <td>{appt.date}</td>
                        <td>{appt.patient.user.name}</td>
                        <td>{diagnosis}</td>
                        <td>{medicines}</td>
                    </tr>
            """
            
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """
        
        # Simulate sending email
        print(f"==================================================")
        print(f"[EMAIL] Sending Monthly Report to {doctor.user.email}")
        print(f"Subject: Monthly Activity Report - {first_day_prev_month.strftime('%B %Y')}")
        print(f"Content (HTML snippet):")
        print(html_content[:500] + "...") # Print first 500 chars
        print(f"==================================================")
