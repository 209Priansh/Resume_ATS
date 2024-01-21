from sqlalchemy.orm import sessionmaker

from app.models.dbmodels import Candidate
from app.config.dbconfig import SessionLocal

# Create the database engine and session
engine = SessionLocal().bind
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Query all candidate profiles and extract their IDs
all_profiles = session.query(Candidate.candidate_id).all()
print(all_profiles)

# Create the your_profile_id_list
your_profile_id_list = [profile.candidate_id for profile in all_profiles]

# Close the session
session.close()

# Print the resulting profile ID list
print(your_profile_id_list)
