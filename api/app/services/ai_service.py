from typing import Dict, Any, List
from openai import OpenAI
from langchain.llms import OpenAI as LangChainOpenAI
from langchain.prompts import PromptTemplate
from api.app.core.config import settings
import json
import time
from datetime import datetime


class AIAgentService:
    """Service for managing AI agent interactions and task execution"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.llm = LangChainOpenAI(openai_api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    async def execute_task(self, agent_config: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the specified AI agent configuration"""
        if not self.openai_client:
            # Demo mode - return simulated responses
            return await self._execute_demo_task(agent_config, task_data)
        
        start_time = time.time()
        
        try:
            # Build the prompt based on agent configuration and task
            prompt = self._build_agent_prompt(agent_config, task_data)
            
            # Execute the task using OpenAI
            response = self.openai_client.chat.completions.create(
                model=agent_config.get("model", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": self._get_system_prompt(agent_config)},
                    {"role": "user", "content": prompt}
                ],
                temperature=agent_config.get("temperature", 0.7),
                max_tokens=agent_config.get("max_tokens", 1000)
            )
            
            result = response.choices[0].message.content
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "model_used": agent_config.get("model", "gpt-3.5-turbo")
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "result": None,
                "execution_time": execution_time
            }
    
    def _build_agent_prompt(self, agent_config: Dict[str, Any], task_data: Dict[str, Any]) -> str:
        """Build a prompt for the agent based on task requirements"""
        template = agent_config.get("prompt_template", "")
        if not template:
            template = """
            Task: {task_title}
            Description: {task_description}
            Instructions: {task_instructions}
            Expected Output: {expected_output}
            
            Please complete this task according to the instructions provided.
            """
        
        return template.format(
            task_title=task_data.get("title", ""),
            task_description=task_data.get("description", ""),
            task_instructions=task_data.get("instructions", ""),
            expected_output=task_data.get("expected_output", "")
        )
    
    def _get_system_prompt(self, agent_config: Dict[str, Any]) -> str:
        """Generate system prompt based on agent configuration"""
        personality = agent_config.get("personality_profile", {})
        capabilities = agent_config.get("capabilities", [])
        role_info = agent_config.get("role", {})
        
        system_prompt = f"""
        You are an AI agent with the following characteristics:
        
        Role: {role_info.get('title', 'AI Assistant')}
        Description: {agent_config.get('description', 'A helpful AI assistant')}
        
        Personality Traits: {', '.join([f"{k}: {v}" for k, v in personality.items()])}
        
        Capabilities: {', '.join(capabilities)}
        
        Your goal is to complete tasks efficiently while maintaining the personality and capabilities defined above.
        Always provide clear, actionable responses that align with your role and expertise.
        """
        
        return system_prompt.strip()
    
    async def analyze_agent_performance(self, agent_id: int, recent_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze agent performance based on recent task execution"""
        if not recent_tasks:
            return {
                "performance_score": 0.0,
                "success_rate": 0.0,
                "average_execution_time": 0.0,
                "recommendations": ["No tasks completed yet"]
            }
        
        completed_tasks = [t for t in recent_tasks if t.get("status") == "completed"]
        failed_tasks = [t for t in recent_tasks if t.get("status") == "failed"]
        
        success_rate = len(completed_tasks) / len(recent_tasks) if recent_tasks else 0.0
        avg_execution_time = sum(t.get("execution_time_seconds", 0) for t in completed_tasks) / len(completed_tasks) if completed_tasks else 0.0
        
        # Calculate performance score (0-100)
        performance_score = min(100, success_rate * 100 * (1 - min(0.5, avg_execution_time / 60)))
        
        recommendations = []
        if success_rate < 0.8:
            recommendations.append("Consider reviewing task instructions clarity")
        if avg_execution_time > 30:
            recommendations.append("Optimize prompt templates for faster execution")
        if len(failed_tasks) > 0:
            recommendations.append("Analyze failed task patterns for improvement")
        
        return {
            "performance_score": round(performance_score, 2),
            "success_rate": round(success_rate * 100, 2),
            "average_execution_time": round(avg_execution_time, 2),
            "total_tasks": len(recent_tasks),
            "completed_tasks": len(completed_tasks),
            "failed_tasks": len(failed_tasks),
            "recommendations": recommendations
        }
    
    def generate_agent_suggestions(self, domain: str, role: str) -> Dict[str, Any]:
        """Generate AI agent configuration suggestions based on domain and role"""
        suggestions = {
            "personality_profile": {},
            "capabilities": [],
            "recommended_model": "gpt-3.5-turbo",
            "prompt_template": "",
            "limitations": []
        }
        
        # Domain-specific suggestions
        domain_configs = {
            "software_development": {
                "personality": {"analytical": "high", "detail_oriented": "high", "creative": "medium"},
                "capabilities": ["code_review", "debugging", "architecture_design", "testing"],
                "limitations": ["cannot execute code directly", "limited to text-based outputs"]
            },
            "marketing": {
                "personality": {"creative": "high", "persuasive": "high", "analytical": "medium"},
                "capabilities": ["content_creation", "campaign_analysis", "customer_research"],
                "limitations": ["cannot access real-time market data", "outputs require human review"]
            },
            "data_analysis": {
                "personality": {"analytical": "very_high", "detail_oriented": "very_high", "systematic": "high"},
                "capabilities": ["statistical_analysis", "data_interpretation", "report_generation"],
                "limitations": ["cannot access live databases", "limited to provided datasets"]
            }
        }
        
        if domain.lower() in domain_configs:
            config = domain_configs[domain.lower()]
            suggestions["personality_profile"] = config["personality"]
            suggestions["capabilities"] = config["capabilities"]
            suggestions["limitations"] = config["limitations"]
        
        # Role-specific prompt template
        role_templates = {
            "analyst": "As a {role} in {domain}, analyze the following: {task_description}\n\nProvide detailed insights and actionable recommendations.",
            "manager": "As a {role} in {domain}, coordinate the following: {task_description}\n\nProvide a structured plan with clear next steps.",
            "specialist": "As a {role} specialist in {domain}, execute: {task_description}\n\nProvide expert-level output with detailed explanations."
        }
        
        for role_key, template in role_templates.items():
            if role_key.lower() in role.lower():
                suggestions["prompt_template"] = template
                break
        
        return suggestions
    
    async def _execute_demo_task(self, agent_config: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a demo task with simulated AI responses"""
        start_time = time.time()
        
        # Simulate processing time
        time.sleep(0.5)
        
        role = agent_config.get("role", {}).get("title", "AI Assistant")
        task_title = task_data.get("title", "Demo Task")
        
        # Generate demo responses based on task type
        demo_responses = {
            "analysis": f"As {role}, I've analyzed the request '{task_title}'. In this demo mode, I would typically provide detailed insights, patterns, and recommendations based on the data provided. The analysis would include key findings, visualizations, and actionable next steps.",
            "report": f"Demo Report for '{task_title}':\n\n1. Executive Summary\n2. Key Findings\n3. Detailed Analysis\n4. Recommendations\n5. Next Steps\n\nThis demonstrates how {role} would generate comprehensive reports.",
            "planning": f"Strategic Plan for '{task_title}':\n\n- Phase 1: Initial Assessment\n- Phase 2: Resource Allocation\n- Phase 3: Implementation\n- Phase 4: Monitoring & Optimization\n\nTimeline: 4-6 weeks\nRequired Resources: Listed in detail",
            "default": f"Demo response from {role} for task '{task_title}':\n\nIn a production environment, this AI agent would process your request using advanced language models. The response would be tailored to the specific requirements and would leverage the agent's configured capabilities and personality traits."
        }
        
        # Determine response type
        task_desc = task_data.get("description", "").lower()
        if "analyz" in task_desc or "analysis" in task_desc:
            result = demo_responses["analysis"]
        elif "report" in task_desc:
            result = demo_responses["report"]
        elif "plan" in task_desc:
            result = demo_responses["planning"]
        else:
            result = demo_responses["default"]
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "result": result,
            "execution_time": execution_time,
            "tokens_used": 150,  # Simulated
            "model_used": "demo-mode",
            "demo_mode": True
        }
