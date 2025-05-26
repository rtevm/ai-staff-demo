from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.app.db.database import get_db
from api.app.models.models import AIAgent, Role, Domain, Team
from api.app.schemas.schemas import AIAgent as AIAgentSchema, AIAgentCreate, AIAgentUpdate
from api.app.services.ai_service import AIAgentService

router = APIRouter()
ai_service = AIAgentService()


@router.get("/", response_model=List[AIAgentSchema])
def get_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of AI agents"""
    agents = db.query(AIAgent).offset(skip).limit(limit).all()
    return agents


@router.get("/{agent_id}", response_model=AIAgentSchema)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get specific AI agent by ID"""
    agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/", response_model=AIAgentSchema)
def create_agent(agent: AIAgentCreate, db: Session = Depends(get_db)):
    """Create a new AI agent"""
    # Validate foreign keys exist
    role = db.query(Role).filter(Role.id == agent.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")
    
    domain = db.query(Domain).filter(Domain.id == agent.domain_id).first()
    if not domain:
        raise HTTPException(status_code=400, detail="Domain not found")
    
    team = db.query(Team).filter(Team.id == agent.team_id).first()
    if not team:
        raise HTTPException(status_code=400, detail="Team not found")
    
    # Generate AI suggestions for the agent
    suggestions = ai_service.generate_agent_suggestions(domain.name, role.title)
    
    # Create agent with suggestions if not provided
    agent_data = agent.dict()
    if not agent_data.get("personality_profile"):
        agent_data["personality_profile"] = suggestions["personality_profile"]
    if not agent_data.get("capabilities"):
        agent_data["capabilities"] = suggestions["capabilities"]
    if not agent_data.get("prompt_template"):
        agent_data["prompt_template"] = suggestions["prompt_template"]
    
    db_agent = AIAgent(**agent_data)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.put("/{agent_id}", response_model=AIAgentSchema)
def update_agent(agent_id: int, agent_update: AIAgentUpdate, db: Session = Depends(get_db)):
    """Update an AI agent"""
    db_agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent, field, value)
    
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an AI agent"""
    db_agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(db_agent)
    db.commit()
    return {"message": "Agent deleted successfully"}


@router.get("/{agent_id}/performance")
async def get_agent_performance(agent_id: int, db: Session = Depends(get_db)):
    """Get agent performance metrics"""
    agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get recent tasks for performance analysis
    recent_tasks = [
        {
            "status": task.status,
            "execution_time_seconds": task.execution_time_seconds or 0
        }
        for task in agent.tasks[-20:]  # Last 20 tasks
    ]
    
    performance = await ai_service.analyze_agent_performance(agent_id, recent_tasks)
    return performance


@router.post("/{agent_id}/execute-task")
async def execute_task(agent_id: int, task_data: dict, db: Session = Depends(get_db)):
    """Execute a task using the specified agent"""
    agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if not agent.is_active:
        raise HTTPException(status_code=400, detail="Agent is not active")
    
    # Prepare agent configuration
    agent_config = {
        "model": agent.model_config.get("model", "gpt-3.5-turbo") if agent.model_config else "gpt-3.5-turbo",
        "temperature": agent.model_config.get("temperature", 0.7) if agent.model_config else 0.7,
        "max_tokens": agent.model_config.get("max_tokens", 1000) if agent.model_config else 1000,
        "prompt_template": agent.prompt_template,
        "personality_profile": agent.personality_profile or {},
        "capabilities": agent.capabilities or [],
        "description": agent.description,
        "role": {
            "title": agent.role.title if agent.role else "AI Assistant"
        }
    }
    
    # Execute the task
    result = await ai_service.execute_task(agent_config, task_data)
    
    # Update agent performance metrics
    if result["success"]:
        agent.total_tasks_completed += 1
        agent.success_rate = (agent.success_rate * (agent.total_tasks_completed - 1) + 1) / agent.total_tasks_completed
    else:
        total_attempts = agent.total_tasks_completed + 1
        agent.success_rate = (agent.success_rate * agent.total_tasks_completed) / total_attempts
    
    db.commit()
    
    return result
