from sqlalchemy import create_engine, Column, String, Integer, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# JobPosting 모델 정의
class JobPosting(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    date_posted = Column(Date, nullable=True)
    location = Column(String(255), nullable=True)
    job_type = Column(String(255), nullable=True)
    __table_args__ = (UniqueConstraint('title', 'company', name='_title_company_uc'),)

# MySQL 연결 설정
DATABASE_URL = "mysql+pymysql://saramin_user:password@localhost/saramin"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# 테이블 생성
Base.metadata.create_all(engine)
