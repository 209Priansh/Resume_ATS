# add_multiple_candidates.py
from app.config.dbconfig import SessionLocal
from app.models.dbmodels import Candidate, Education, WorkExperience, Skill


def add_candidate_data(session, first_name, last_name, email, contact_number, degree, school, skills, job_title,
                       company, years_of_experience):
    try:
        # Insert data for the candidate
        candidate = Candidate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_number=contact_number
        )
        session.add(candidate)
        session.commit()

        # Fetch the candidate_id for the candidate
        candidate_id = session.query(Candidate.candidate_id).filter_by(email=email).first()[0]

        # Insert education data for the candidate
        education = Education(
            candidate_id=candidate_id,
            degree=degree,
            school=school
        )
        session.add(education)
        session.commit()

        # Insert skills data for the candidate
        skill = Skill(
            candidate_id=candidate_id,
            skill_name=skills
        )
        session.add(skill)
        session.commit()

        # Insert work experience data for the candidate
        experience = WorkExperience(
            candidate_id=candidate_id,
            job_title=job_title,
            company=company,
            years_of_experience=years_of_experience
        )
        session.add(experience)
        session.commit()

        print(f"Data added successfully for {first_name} {last_name}.")

    except Exception as e:
        print(f"Error adding data: {e}")
        session.rollback()


def add_multiple_candidates():
    session = SessionLocal()

    try:
        # Add data for candidate 1
        add_candidate_data(session, 'John', 'Doe', 'john.doe@email.com', '+1 555-1234',
                           'Bachelor of Science in Computer Science', 'University of XYZ | Anytown, USA | May 2022',
                           'Java, Python, C++', 'Software Engineer Intern',
                           'Tech Innovators Pvt. Ltd. | Bangalore, India', 1)

        # Add data for candidate 2
        add_candidate_data(session, 'Amit', 'Patel', 'amit.patel@email.com', '+91 98765 43210',
                           'Master of Technology in Electronics',
                           'Indian Institute of Technology (IIT) | Mumbai, India | May 2022',
                           'Embedded Systems, IoT, C', 'Electronics Engineer', 'ElectroTech Solutions | Mumbai, India',
                           2)

        # Add data for candidate 3
        add_candidate_data(session, 'Priya', 'Sharma', 'priya.sharma@email.com', '+91 87654 32109',
                           'Bachelor of Arts in English Literature',
                           'St. Xavier\'s College | Kolkata, India | May 2021',
                           'Content Writing, Editing, Communication Skills', 'Content Writer',
                           'Creative Words Media | Kolkata, India', 3)

        add_candidate_data(session, 'Vikram', 'Gupta', 'vikram.gupta@email.com', '+91 98765 43210',
                           'Bachelor of Technology in Electrical Engineering',
                           'Indian Institute of Technology (IIT) | Delhi, India | May 2022',
                           'Power Systems, Renewable Energy, Control Systems', 'Electrical Engineer',
                           'PowerTech Solutions | Delhi, India', 4)

        # Add data for candidate 5
        add_candidate_data(session, 'Neha', 'Kapoor', 'neha.kapoor@email.com', '+91 87654 32109',
                           'Master of Business Administration (MBA)', 'XYZ Business School | Mumbai, India | May 2021',
                           'Business Strategy, Marketing, Financial Analysis', 'Business Analyst',
                           'Global Enterprises Ltd. | Mumbai, India', 5)

        # Add data for candidate 6
        add_candidate_data(session, 'Rahul', 'Singh', 'rahul.singh@email.com', '+91 76543 21098',
                           'Bachelor of Science in Computer Engineering', 'ABC University | Pune, India | May 2022',
                           'Java, Spring Boot,angular , Data entry , React', 'Software Developer', 'Tech Wizards Pvt. Ltd. | Pune, India', 6)

        add_candidate_data(session, 'Kamalesh', 'Tripathy', 'kamalesh.tripathy@email.com', '+91 98765 43210',
                           'Bachelor of Technology in Computer Science',
                           'ABC Engineering College | Bangalore, India | May 2021',
                           'Java, Python, Spring Boot , C, VS code', 'Software Developer',
                           'Tech Solutions India Pvt. Ltd. | Bangalore, India', 10)

        add_candidate_data(session, 'Chandana', 'M', 'chandana.m@email.com', '+91 87654 32109',
                           'Bachelor of Commerce', 'XYZ University | Mumbai, India | April 2022',
                           'Data Entry, Microsoft Excel, Typing', 'Data Entry Specialist',
                           'Data Management Services | Mumbai, India', 11)

        add_candidate_data(session, 'Rohit', 'Shetty', 'rohit.shetty@email.com', '+91 76543 21098',
                           'Bachelor of Engineering in Information Technology',
                           'LMN College of Engineering | Pune, India | June 2020',
                           'HTML, CSS, JavaScript, React', 'Web Developer', 'Web Creators Pvt. Ltd. | Pune, India', 12)

        add_candidate_data(session, 'Emily', 'Smith', 'emily.smith@email.com', '+91 87654 32109',
                           'Bachelor of Arts in Business Administration', 'LMN College | London, UK | April 2020',
                           'Data Entry, Microsoft Excel, Typing', 'Data Entry Specialist',
                           'Data Management Ltd. | London, UK', 8)

        add_candidate_data(session, 'Alex', 'Williams', 'alex.williams@email.com', '+91 76543 21098',
                           'Master of Science in Computer Science', 'PQR University | Sydney, Australia | June 2023',
                           'Java, Spring Framework, Hibernate', 'Software Engineer',
                           'Tech Innovators Pty Ltd. | Sydney, Australia', 9)

        # Payal Sharma
        add_candidate_data(session, 'Payal', 'Sharma', 'payal.sharma@email.com', '+91 87654 32101',
                           'Bachelor of Technology in Information Technology',
                           'ABC Institute | Pune, India | April 2022',
                           'Java, Spring Boot, SQL', 'Software Engineer', 'Innovative Tech Solutions | Pune, India', 14)

        # Rajdeep Singh
        add_candidate_data(session, 'Rajdeep', 'Singh', 'rajdeep.singh@email.com', '+91 98765 43219',
                           'Master of Business Administration (MBA)', 'LMN Business School | Delhi, India | June 2023',
                           'Business Analysis, Marketing, Project Management', 'Business Analyst',
                           'Global Enterprises Ltd. | Delhi, India', 15)

        # Neha Verma
        add_candidate_data(session, 'Neha', 'Verma', 'neha.verma@email.com', '+91 87654 32111',
                           'Bachelor of Science in Electrical Engineering',
                           'PQR University | Bangalore, India | May 2022',
                           'C++, Embedded Systems, Electrical Design , react', 'Electrical Engineer',
                           'PowerTech Innovations | Bangalore, India', 16)

        # Priansh Singh
        add_candidate_data(session, 'Priansh', 'Singh', 'priansh.singh@email.com', '+91 76543 21003',
                           'Master of Technology in Mechanical Engineering',
                           'DEF Institute of Technology | Mumbai, India | April 2023',
                           'Java , JSF ,Docker , HTML', 'Software Engineer',
                           'Dynamic Machines Ltd. | Mumbai, India', 17)

        # Saif Khan
        add_candidate_data(session, 'Saif', 'Khan', 'saif.k@email.com', '+91 98765 67892',
                           'Bachelor of Arts in Literature', 'LMN College | Kolkata, India | May 2022',
                           'Content Writing, Editing, Blogging', 'Content Writer',
                           'Creative Words Media | Kolkata, India', 18)

        # Prashant Sharma
        add_candidate_data(session, 'Prashant', 'Sharma', 'prashant.sharma@email.com', '+91 78705 23456',
                           'Bachelor of Commerce', 'XYZ University | Mumbai, India | April 2022',
                           'Accounting, Financial Analysis, Excel', 'Accountant',
                           'Financial Solutions Pvt. Ltd. | Mumbai, India', 19)

        add_candidate_data(session, 'Namrata', 'Sharma', 'namy.sharma@email.com', '+91 87654 32187',
                           'Bachelor of Science in Chemistry', 'ABC College | Delhi, India | May 2021',
                           'Data Entry , MS Word , react', 'Chemist',
                           'Chemical Innovations Ltd. | Delhi, India', 20)

        add_candidate_data(session, 'Rakul', 'Verma', 'rakul.kumar@email.com', '+91 98765 78210',
                           'Master of Computer Applications (MCA)',
                           'MNO Institute of Technology | Bangalore, India | June 2023',
                           'Java, Spring MVC, Hibernate', 'Software Developer',
                           'Innovative Tech Solutions | Bangalore, India', 21)


    finally:
        session.close()


if __name__ == "__main__":
    add_multiple_candidates()
