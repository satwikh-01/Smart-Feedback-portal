from sqlalchemy.orm import Session
from app.models.team import Team
from app.models.user import User
from app.schemas.team import TeamCreate

def get_team(db: Session, team_id: int):
    """
    Fetches a team by its ID.
    """
    return db.query(Team).filter(Team.id == team_id).first()

def get_team_by_manager(db: Session, manager_id: int):
    """
    Fetches the team managed by a specific manager.
    """
    return db.query(Team).filter(Team.manager_id == manager_id).first()

def create_team(db: Session, team: TeamCreate, manager_id: int):
    """
    Creates a new team for a manager.
    """
    db_team = Team(name=team.name, manager_id=manager_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def add_employee_to_team(db: Session, team: Team, user: User):
    """
    Assigns an employee to a team.
    """
    user.team_id = team.id
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
