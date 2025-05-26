// AI Staff Platform Dashboard JavaScript

// API base URL
const API_BASE = '/api/v1';

// Global variables
let agents = [];
let currentUser = null;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

// Initialize the dashboard
async function initializeDashboard() {
    try {
        showLoading();
        await loadDashboardData();
        setupEventListeners();
        hideLoading();
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showNotification('Error loading dashboard', 'error');
        hideLoading();
    }
}

// Load all dashboard data
async function loadDashboardData() {
    try {
        // Load agents data
        await loadAgents();
        
        // Update overview stats
        updateOverviewStats();
        
        // Load recent activity
        loadRecentActivity();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        throw error;
    }
}

// Load agents from API
async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE}/agents/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        agents = await response.json();
        renderAgentsTable();
        return agents;
    } catch (error) {
        console.error('Error loading agents:', error);
        // Show demo data if API is not available
        agents = getDemoAgents();
        renderAgentsTable();
        return agents;
    }
}

// Get demo agents data for showcase
function getDemoAgents() {
    return [
        {
            id: 1,
            name: "Sarah Analytics",
            description: "Data analysis specialist focused on business intelligence",
            role: { title: "Data Analyst" },
            domain: { name: "Data Science" },
            team: { name: "Analytics Team" },
            is_active: true,
            performance_score: 92.5,
            total_tasks_completed: 47,
            success_rate: 94.0
        },
        {
            id: 2,
            name: "Marcus CodeReview",
            description: "Software development expert specializing in code quality",
            role: { title: "Senior Developer" },
            domain: { name: "Software Engineering" },
            team: { name: "Development Team" },
            is_active: true,
            performance_score: 88.3,
            total_tasks_completed: 62,
            success_rate: 91.2
        },
        {
            id: 3,
            name: "Elena Strategy",
            description: "Strategic planning and project management specialist",
            role: { title: "Project Manager" },
            domain: { name: "Business Strategy" },
            team: { name: "Strategy Team" },
            is_active: true,
            performance_score: 95.7,
            total_tasks_completed: 34,
            success_rate: 97.1
        }
    ];
}

// Render agents table
function renderAgentsTable() {
    const tableBody = document.getElementById('agents-table-body');
    
    if (!agents || agents.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No agents found</td></tr>';
        return;
    }
    
    tableBody.innerHTML = agents.map(agent => `
        <tr class="fade-in">
            <td>
                <div class="d-flex align-items-center">
                    <div class="me-3">
                        <i class="fas fa-robot text-primary"></i>
                    </div>
                    <div>
                        <div class="fw-bold">${agent.name}</div>
                        <div class="text-muted small">${agent.description || 'No description'}</div>
                    </div>
                </div>
            </td>
            <td>
                <span class="badge bg-secondary">${agent.role?.title || 'Unknown'}</span>
            </td>
            <td>
                <span class="badge bg-info">${agent.domain?.name || 'Unknown'}</span>
            </td>
            <td>
                <span class="badge bg-warning text-dark">${agent.team?.name || 'Unknown'}</span>
            </td>
            <td>
                <span class="status-badge ${agent.is_active ? 'status-active' : 'status-inactive'}">
                    ${agent.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td>
                <div class="performance-indicator ${getPerformanceClass(agent.performance_score)}">
                    ${agent.performance_score?.toFixed(1) || '0.0'}%
                </div>
                <div class="text-muted small">
                    ${agent.total_tasks_completed || 0} tasks completed
                </div>
            </td>
            <td>
                <div class="btn-group btn-group-sm" role="group">
                    <button type="button" class="btn btn-outline-primary" onclick="viewAgent(${agent.id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button type="button" class="btn btn-outline-secondary" onclick="editAgent(${agent.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="btn btn-outline-danger" onclick="deleteAgent(${agent.id})" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Get performance CSS class based on score
function getPerformanceClass(score) {
    if (score >= 90) return 'performance-excellent';
    if (score >= 75) return 'performance-good';
    if (score >= 60) return 'performance-average';
    return 'performance-poor';
}

// Update overview statistics
function updateOverviewStats() {
    const activeAgents = agents.filter(agent => agent.is_active).length;
    const totalTasks = agents.reduce((sum, agent) => sum + (agent.total_tasks_completed || 0), 0);
    const avgSuccessRate = agents.length > 0 
        ? agents.reduce((sum, agent) => sum + (agent.success_rate || 0), 0) / agents.length 
        : 0;
    
    // Update DOM elements
    document.getElementById('total-agents').textContent = activeAgents;
    document.getElementById('completed-tasks').textContent = totalTasks;
    document.getElementById('success-rate').textContent = `${avgSuccessRate.toFixed(1)}%`;
    document.getElementById('active-teams').textContent = getUniqueTeamsCount();
}

// Get unique teams count
function getUniqueTeamsCount() {
    const teams = new Set(agents.map(agent => agent.team?.name).filter(Boolean));
    return teams.size;
}

// Load recent activity
function loadRecentActivity() {
    const recentActivityDiv = document.getElementById('recent-activity');
    
    // Demo recent activity data
    const activities = [
        {
            type: 'agent_created',
            message: 'New agent "Sarah Analytics" was created',
            time: '2 minutes ago',
            icon: 'fas fa-robot text-primary'
        },
        {
            type: 'task_completed',
            message: 'Task "Market Analysis Q4" completed successfully',
            time: '15 minutes ago',
            icon: 'fas fa-check-circle text-success'
        },
        {
            type: 'team_updated',
            message: 'Analytics Team governance structure updated',
            time: '1 hour ago',
            icon: 'fas fa-users text-info'
        },
        {
            type: 'performance_alert',
            message: 'Agent performance review scheduled',
            time: '2 hours ago',
            icon: 'fas fa-chart-line text-warning'
        }
    ];
    
    recentActivityDiv.innerHTML = activities.map(activity => `
        <div class="d-flex align-items-center mb-3">
            <div class="me-3">
                <i class="${activity.icon}"></i>
            </div>
            <div class="flex-grow-1">
                <div class="text-sm">${activity.message}</div>
                <div class="text-muted small">${activity.time}</div>
            </div>
        </div>
    `).join('');
}

// Setup event listeners
function setupEventListeners() {
    // Create agent modal form submission
    const createAgentForm = document.getElementById('createAgentForm');
    if (createAgentForm) {
        createAgentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            createAgent();
        });
    }
    
    // Setup navigation
    setupNavigation();
}

// Setup navigation
function setupNavigation() {
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Handle navigation based on href
            const target = this.getAttribute('href');
            navigateToSection(target);
        });
    });
}

// Navigate to different sections
function navigateToSection(target) {
    switch(target) {
        case '#overview':
            // Already shown by default
            break;
        case '#agent-management':
            // Scroll to agent management section
            document.getElementById('agent-management').scrollIntoView({ behavior: 'smooth' });
            break;
        default:
            // Future sections
            showNotification(`Navigation to ${target} - Coming soon!`, 'info');
    }
}

// Show create agent modal
function showCreateAgentModal() {
    const modal = new bootstrap.Modal(document.getElementById('createAgentModal'));
    
    // Load dropdown options
    loadDropdownOptions();
    
    // Reset form
    document.getElementById('createAgentForm').reset();
    
    modal.show();
}

// Load dropdown options for the create agent form
async function loadDropdownOptions() {
    // Demo data - in a real app, these would come from the API
    const roles = [
        { id: 1, title: 'Data Analyst' },
        { id: 2, title: 'Senior Developer' },
        { id: 3, title: 'Project Manager' },
        { id: 4, title: 'Business Analyst' },
        { id: 5, title: 'Quality Assurance' }
    ];
    
    const domains = [
        { id: 1, name: 'Data Science' },
        { id: 2, name: 'Software Engineering' },
        { id: 3, name: 'Business Strategy' },
        { id: 4, name: 'Marketing' },
        { id: 5, name: 'Operations' }
    ];
    
    const teams = [
        { id: 1, name: 'Analytics Team' },
        { id: 2, name: 'Development Team' },
        { id: 3, name: 'Strategy Team' },
        { id: 4, name: 'Marketing Team' },
        { id: 5, name: 'Operations Team' }
    ];
    
    // Populate dropdowns
    populateDropdown('agentRole', roles, 'id', 'title');
    populateDropdown('agentDomain', domains, 'id', 'name');
    populateDropdown('agentTeam', teams, 'id', 'name');
}

// Populate dropdown with options
function populateDropdown(selectId, options, valueField, textField) {
    const select = document.getElementById(selectId);
    
    // Clear existing options (except the first placeholder)
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }
    
    // Add new options
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option[valueField];
        optionElement.textContent = option[textField];
        select.appendChild(optionElement);
    });
}

// Create new agent
async function createAgent() {
    const form = document.getElementById('createAgentForm');
    const formData = new FormData(form);
    
    const agentData = {
        name: document.getElementById('agentName').value,
        description: document.getElementById('agentDescription').value,
        role_id: parseInt(document.getElementById('agentRole').value),
        domain_id: parseInt(document.getElementById('agentDomain').value),
        team_id: parseInt(document.getElementById('agentTeam').value)
    };
    
    // Validate required fields
    if (!agentData.name || !agentData.role_id || !agentData.domain_id || !agentData.team_id) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    try {
        showLoading();
        
        // For demo purposes, simulate API call
        await simulateCreateAgent(agentData);
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createAgentModal'));
        modal.hide();
        
        // Refresh agents data
        await loadAgents();
        updateOverviewStats();
        
        showNotification('Agent created successfully!', 'success');
        hideLoading();
        
    } catch (error) {
        console.error('Error creating agent:', error);
        showNotification('Error creating agent', 'error');
        hideLoading();
    }
}

// Simulate agent creation for demo
async function simulateCreateAgent(agentData) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const newAgent = {
                id: agents.length + 1,
                ...agentData,
                role: { title: getDropdownText('agentRole') },
                domain: { name: getDropdownText('agentDomain') },
                team: { name: getDropdownText('agentTeam') },
                is_active: true,
                performance_score: 85.0,
                total_tasks_completed: 0,
                success_rate: 0.0
            };
            
            agents.unshift(newAgent);
            resolve(newAgent);
        }, 500);
    });
}

// Get text from dropdown option
function getDropdownText(selectId) {
    const select = document.getElementById(selectId);
    return select.options[select.selectedIndex].text;
}

// View agent details
function viewAgent(agentId) {
    const agent = agents.find(a => a.id === agentId);
    if (agent) {
        showNotification(`Viewing details for ${agent.name} - Feature coming soon!`, 'info');
    }
}

// Edit agent
function editAgent(agentId) {
    const agent = agents.find(a => a.id === agentId);
    if (agent) {
        showNotification(`Editing ${agent.name} - Feature coming soon!`, 'info');
    }
}

// Delete agent
function deleteAgent(agentId) {
    const agent = agents.find(a => a.id === agentId);
    if (agent && confirm(`Are you sure you want to delete ${agent.name}?`)) {
        agents = agents.filter(a => a.id !== agentId);
        renderAgentsTable();
        updateOverviewStats();
        showNotification(`${agent.name} deleted successfully`, 'success');
    }
}

// Refresh dashboard
async function refreshDashboard() {
    showNotification('Refreshing dashboard...', 'info');
    await loadDashboardData();
    showNotification('Dashboard refreshed!', 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast ${bgClass} text-white" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Show loading state
function showLoading() {
    const loadingSpinner = document.createElement('div');
    loadingSpinner.id = 'loading-overlay';
    loadingSpinner.innerHTML = `
        <div class="d-flex justify-content-center align-items-center position-fixed top-0 start-0 w-100 h-100" 
             style="background-color: rgba(0,0,0,0.1); z-index: 9999;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    document.body.appendChild(loadingSpinner);
}

// Hide loading state
function hideLoading() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.remove();
    }
}

// Placeholder functions for future features
function showCreateTeamModal() {
    showNotification('Create Team feature coming soon!', 'info');
}

function showCreateProjectModal() {
    showNotification('Create Project feature coming soon!', 'info');
}

function viewAnalytics() {
    showNotification('Analytics Dashboard coming soon!', 'info');
}

// Export functions for global access
window.refreshDashboard = refreshDashboard;
window.showCreateAgentModal = showCreateAgentModal;
window.createAgent = createAgent;
window.viewAgent = viewAgent;
window.editAgent = editAgent;
window.deleteAgent = deleteAgent;
window.showCreateTeamModal = showCreateTeamModal;
window.showCreateProjectModal = showCreateProjectModal;
window.viewAnalytics = viewAnalytics;
