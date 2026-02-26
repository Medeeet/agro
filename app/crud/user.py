from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import UserProfile
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> UserProfile:
    db_user = UserProfile(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.id == user_id).first()


def get_users(db: Session, skip=0, limit=20, search=None):
    query = db.query(UserProfile)

    if search:
        query = query.filter(
            or_(
                UserProfile.first_name.ilike(f"%{search}%"),
                UserProfile.last_name.ilike(f"%{search}%"),
                UserProfile.email.ilike(f"%{search}%")
            )
        )

    return query.offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    db_user = get_user(db, user_id)

    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user

