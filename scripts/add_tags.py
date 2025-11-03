from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.posts.model.model import Base, TagModel

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/challenge_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

TAGS = [
    "tecnología", "programación", "web", "mobile", "datos", "ai", "cloud", "tutorial", "noticias", "opinión"
]


def main():
    db = Session()

    for tag_name in TAGS:
        if not db.query(TagModel).filter_by(name=tag_name).first():
            db.add(TagModel(name=tag_name))
            print(f"➕ {tag_name}")

    db.commit()
    db.close()
    print("✅ Tags creados exitosamente!")


if __name__ == "__main__":
    main()