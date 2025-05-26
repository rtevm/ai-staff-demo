from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.app.db.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    teams = relationship("Team", back_populates="owner")
    projects = relationship("Project", back_populates="creator")


class Domain(Base):
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    expertise_areas = Column(JSON)  # List of expertise areas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    agents = relationship("AIAgent", back_populates="domain")
    policies = relationship("Policy", back_populates="domain")


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    responsibilities = Column(JSON)  # List of responsibilities
    authority_level = Column(Integer, default=1)  # 1-10 scale
    required_skills = Column(JSON)  # List of required skills
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    agents = relationship("AIAgent", back_populates="role")


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    purpose = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    governance_structure = Column(JSON)  # Self-management structure
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="teams")
    agents = relationship("AIAgent", back_populates="team")
    projects = relationship("Project", back_populates="team")


class AIAgent(Base):
    __tablename__ = "ai_agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    personality_profile = Column(JSON)  # AI personality traits
    capabilities = Column(JSON)  # List of capabilities
    limitations = Column(JSON)  # Known limitations
    
    # Relationships
    role_id = Column(Integer, ForeignKey("roles.id"))
    domain_id = Column(Integer, ForeignKey("domains.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    
    # Configuration
    model_config = Column(JSON)  # AI model configuration
    prompt_template = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Performance tracking
    performance_score = Column(Float, default=0.0)
    total_tasks_completed = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    role = relationship("Role", back_populates="agents")
    domain = relationship("Domain", back_populates="agents")
    team = relationship("Team", back_populates="agents")
    tasks = relationship("Task", back_populates="assigned_agent")
    metrics = relationship("Metric", back_populates="agent")


class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    policy_text = Column(Text, nullable=False)
    domain_id = Column(Integer, ForeignKey("domains.id"))
    enforcement_level = Column(String, default="advisory")  # advisory, mandatory, critical
    version = Column(String, default="1.0")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    domain = relationship("Domain", back_populates="policies")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    objectives = Column(JSON)  # List of project objectives
    status = Column(String, default="planning")  # planning, active, paused, completed, cancelled
    priority = Column(String, default="medium")  # low, medium, high, critical
    
    # Relationships
    team_id = Column(Integer, ForeignKey("teams.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))
    
    # Timeline
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Progress tracking
    completion_percentage = Column(Float, default=0.0)
    
    # Relationships
    team = relationship("Team", back_populates="projects")
    creator = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    instructions = Column(Text)
    expected_output = Column(Text)
    
    # Relationships
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_agent_id = Column(Integer, ForeignKey("ai_agents.id"))
    
    # Status and progress
    status = Column(String, default="pending")  # pending, in_progress, completed, failed, cancelled
    priority = Column(String, default="medium")  # low, medium, high, critical
    difficulty_level = Column(Integer, default=1)  # 1-10 scale
    
    # Execution details
    execution_log = Column(JSON)  # Detailed execution history
    result = Column(Text)
    execution_time_seconds = Column(Float)
    
    # Timeline
    due_date = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assigned_agent = relationship("AIAgent", back_populates="tasks")


class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    metric_type = Column(String, nullable=False)  # performance, efficiency, quality, etc.
    
    # Measurement
    value = Column(Float, nullable=False)
    unit = Column(String)  # percentage, count, time, etc.
    target_value = Column(Float)
    
    # Relationships
    agent_id = Column(Integer, ForeignKey("ai_agents.id"))
    
    # Context
    measurement_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    # Relationships
    agent = relationship("AIAgent", back_populates="metrics")


class Accountability(Base):
    __tablename__ = "accountabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("ai_agents.id"))
    accountability_type = Column(String, nullable=False)  # outcome, process, compliance
    description = Column(Text, nullable=False)
    measurement_criteria = Column(JSON)  # How accountability is measured
    review_frequency = Column(String, default="weekly")  # daily, weekly, monthly, quarterly
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    agent = relationship("AIAgent")
