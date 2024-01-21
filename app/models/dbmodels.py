# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.config.dbconfig import Base


class Candidate(Base):
    __tablename__ = 'candidates'
    candidate_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    contact_number = Column(String)

    education = relationship('Education', back_populates='candidate')
    work_experience = relationship('WorkExperience', back_populates='candidate')
    skills = relationship('Skill', back_populates='candidate')


class Education(Base):
    __tablename__ = 'education'
    education_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    degree = Column(String)
    school = Column(String)
    candidate = relationship('Candidate', back_populates='education')


class WorkExperience(Base):
    __tablename__ = 'work_experience'
    experience_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    job_title = Column(String)
    company = Column(String)
    years_of_experience = Column(Integer)
    candidate = relationship('Candidate', back_populates='work_experience')


class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    skill_name = Column(String)
    candidate = relationship('Candidate', back_populates='skills')


class Job_Details(Base):
    __tablename__ = 'job_details'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    ratings = Column(Float)
    job_description = Column(String)
    salary = Column(String)
    location = Column(String)

