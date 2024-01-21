from app.models.dbmodels import Candidate, Education, WorkExperience, Skill
from app.config.dbconfig import SessionLocal
import requests
import logging

logging.basicConfig(level=logging.DEBUG)


def fetch_txt_resume_data(resume_url):
    response = requests.get(resume_url)
    if response.status_code == 200:
        return response.text
    else:
        logging.error(f"Failed to fetch resume data from: {resume_url}")
        return None


def parse_resume_txt(session, resume_text):
    try:
        # Split the resume text into sections based on new lines
        lines = resume_text.split('\n')

        # Ensure there is at least one line in the resume
        if not lines:
            logging.warning("Empty resume text. Skipping.")
            return

        # Extract candidate information
        candidate_info = {'name': '', 'contact': '', 'email': ''}
        for line in lines:
            if line.startswith('Name:'):
                candidate_info['name'] = line[len('Name:'):].strip()
            elif line.startswith('Address:'):
                # Assume the contact information follows the 'Address' line
                contact_info = line[len('Address:'):].strip().split('|')
                for info in contact_info:
                    if 'contact' in info.lower():
                        candidate_info['contact'] = info.split(':')[1].strip()
                    elif 'email' in info.lower():
                        candidate_info['email'] = info.split(':')[1].strip()

        # Check if essential information is present
        if not all(candidate_info.values()):
            logging.warning(f"Invalid candidate information format. Skipping. Candidate info: {candidate_info}")
            return

        # Print candidate information
        print(f"Candidate Info: {candidate_info}")

        # Create a Candidate object and save it to get the candidate_id
        candidate = Candidate(
            first_name=candidate_info['name'].split()[0],
            last_name=candidate_info['name'].split()[1] if len(candidate_info['name'].split()) > 1 else '',
            email=candidate_info['email'],
            contact_number=candidate_info['contact']
        )
        session.add(candidate)
        session.commit()

        # Extract and print other sections (objective, education, skills, work experience, etc.)
        for section in ['Objective', 'Education', 'Skills', 'Work Experience', 'Projects', 'Certifications']:
            try:
                section_start = lines.index(section + ':') + 1
                section_end = lines.index('', section_start) if '' in lines[section_start:] else len(lines)
                section_content = ' '.join(lines[section_start:section_end]).strip()

                # Create corresponding objects and save to the database
                if section == 'Education':
                    education = Education(candidate_id=candidate.candidate_id, degree=section_content)
                    session.add(education)
                elif section == 'Work Experience':
                    experience = WorkExperience(candidate_id=candidate.candidate_id, job_title=section_content)
                    session.add(experience)
                elif section == 'Skills':
                    skill = Skill(candidate_id=candidate.candidate_id, skill_name=section_content)
                    session.add(skill)

                print(f"{section}: {section_content}")

            except ValueError:
                # Ignore section not found errors
                logging.warning(f"Section '{section}' not found. Skipping.")

        # Commit the session after processing all sections
        session.commit()

    except Exception as e:
        logging.error(f"Error during parsing: {e}")


def scrape_resume_from_github(username, repository, folder_path, resume_files):
    github_raw_url = f'https://raw.githubusercontent.com/{username}/{repository}/main/{folder_path}/'
    logging.info(f"Fetching resumes from GitHub folder: {folder_path}")

    session = SessionLocal()

    try:
        for resume_file in resume_files:
            resume_url = f'{github_raw_url}{resume_file}'
            resume_data = fetch_txt_resume_data(resume_url)
            if resume_data:
                parse_resume_txt(session, resume_data)

        logging.info("Scraping completed.")
        session.commit()

    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        session.rollback()  # Rollback changes if an error occurs

    finally:
        session.close()


resume_files_to_scrape = [
    'Amit_resume.txt',
    'Neha_resume.txt',
    'Priya_resume.txt',
    'Rajesh_resume.txt',
    'Swati_resume.txt',
    'Vikram_resume.txt'
]

scrape_resume_from_github('209Priansh', 'ATS_Group9', 'Resume', resume_files_to_scrape)
