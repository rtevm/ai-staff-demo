from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Domain Schemas
class DomainBase(BaseModel):
    name: str
    description: Optional[str] = None
    expertise_areas: Optional[List[str]] = []


class DomainCreate(DomainBase):
    pass


class Domain(DomainBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Role Schemas
class RoleBase(BaseModel):
    title: str
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = []
    authority_level: int = 1
    required_skills: Optional[List[str]] = []


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Team Schemas
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    purpose: Optional[str] = None
    governance_structure: Optional[Dict[str, Any]] = {}
    is_active: bool = True


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# AI Agent Schemas
class AIAgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    personality_profile: Optional[Dict[str, Any]] = {}
    capabilities: Optional[List[str]] = []
    limitations: Optional[List[str]] = []
    model_config: Optional[Dict[str, Any]] = {}
    prompt_template: Optional[str] = None
    is_active: bool = True


class AIAgentCreate(AIAgentBase):
    role_id: int
    domain_id: int
    team_id: int


class AIAgentUpdate(AIAgentBase):
    role_id: Optional[int] = None
    domain_id: Optional[int] = None
    team_id: Optional[int] = None


class AIAgent(AIAgentBase):
    id: int
    role_id: int
    domain_id: int
    team_id: int
    performance_score: float
    total_tasks_completed: int
    success_rate: float
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Related objects
    role: Optional[Role] = None
    domain: Optional[Domain] = None
    team: Optional[Team] = None
    
    class Config:
        from_attributes = True


# Policy Schemas
class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    policy_text: str
    enforcement_level: str = "advisory"
    version: str = "1.0"
    is_active: bool = True


class PolicyCreate(PolicyBase):
    domain_id: int


class Policy(PolicyBase):
    id: int
    domain_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    objectives: Optional[List[str]] = []
    status: str = "planning"
    priority: str = "medium"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    team_id: int


class Project(ProjectBase):
    id: int
    team_id: int
    creator_id: int
    completion_percentage: float
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    expected_output: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    difficulty_level: int = 1
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: int
    assigned_agent_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    result: Optional[str] = None
    execution_time_seconds: Optional[float] = None


class Task(TaskBase):
    id: int
    project_id: int
    assigned_agent_id: int
    execution_log: Optional[Dict[str, Any]] = {}
    result: Optional[str] = None
    execution_time_seconds: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Related objects
    assigned_agent: Optional[AIAgent] = None
    
    class Config:
        from_attributes = True


# Metric Schemas
class MetricBase(BaseModel):
    name: str
    description: Optional[str] = None
    metric_type: str
    value: float
    unit: Optional[str] = None
    target_value: Optional[float] = None
    notes: Optional[str] = None


class MetricCreate(MetricBase):
    agent_id: int


class Metric(MetricBase):
    id: int
    agent_id: int
    measurement_date: datetime
    
    class Config:
        from_attributes = True


# Accountability Schemas
class AccountabilityBase(BaseModel):
    accountability_type: str
    description: str
    measurement_criteria: Optional[Dict[str, Any]] = {}
    review_frequency: str = "weekly"
    is_active: bool = True


class AccountabilityCreate(AccountabilityBase):
    agent_id: int


class Accountability(AccountabilityBase):
    id: int
    agent_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard/Analytics Schemas
class DashboardStats(BaseModel):
    total_agents: int
    active_agents: int
    total_teams: int
    active_projects: int
    completed_tasks: int
    pending_tasks: int
    average_success_rate: float
    top_performing_agents: List[Dict[str, Any]]


class AgentPerformanceReport(BaseModel):
    agent_id: int
    agent_name: str
    total_tasks: int
    completed_tasks: int
    success_rate: float
    average_execution_time: float
    performance_score: float
    recent_metrics: List[Metric]


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
