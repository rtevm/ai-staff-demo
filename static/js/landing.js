// Landing Page JavaScript

// Show More Examples
function showMoreExamples() {
    const moreExamples = document.getElementById('moreExamples');
    const button = event.target;
    
    if (moreExamples.style.display === 'none' || !moreExamples.style.display) {
        moreExamples.style.display = 'block';
        button.textContent = 'Show Less Examples';
        
        // Animate the cards
        const cards = moreExamples.querySelectorAll('.example-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in', 'visible');
            }, index * 100);
        });
    } else {
        moreExamples.style.display = 'none';
        button.textContent = 'See More Examples';
    }
}

// Configure Role
function configureRole(roleType) {
    const modal = new bootstrap.Modal(document.getElementById('roleBuilderModal'));
    
    // Load role configuration based on type
    const modalBody = document.querySelector('#roleBuilderModal .modal-body');
    modalBody.innerHTML = `
        <div class="role-configuration">
            <h4>Configure ${roleType.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())} Role</h4>
            <form id="roleConfigForm">
                <div class="mb-3">
                    <label for="roleName" class="form-label">Role Name</label>
                    <input type="text" class="form-control" id="roleName" value="${roleType.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}" required>
                </div>
                <div class="mb-3">
                    <label for="rolePurpose" class="form-label">Purpose</label>
                    <textarea class="form-control" id="rolePurpose" rows="3" placeholder="Define the primary purpose of this role..." required></textarea>
                </div>
                <div class="mb-3">
                    <label for="accountabilities" class="form-label">Accountabilities</label>
                    <div id="accountabilitiesList">
                        <div class="input-group mb-2">
                            <input type="text" class="form-control" placeholder="Add accountability...">
                            <button class="btn btn-outline-secondary" type="button" onclick="addAccountability()">+</button>
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <label for="domains" class="form-label">Domains</label>
                    <input type="text" class="form-control" id="domains" placeholder="e.g., Marketing, Finance, Operations">
                </div>
                <div class="mb-3">
                    <label for="policies" class="form-label">Policies</label>
                    <textarea class="form-control" id="policies" rows="2" placeholder="Operating guidelines and constraints..."></textarea>
                </div>
                <div class="mb-3">
                    <label for="metrics" class="form-label">Success Metrics</label>
                    <input type="text" class="form-control" id="metrics" placeholder="e.g., ROI, Engagement Rate, Completion Time">
                </div>
                <button type="submit" class="btn btn-primary">Create Agent</button>
            </form>
        </div>
    `;
    
    modal.show();
    
    // Handle form submission
    document.getElementById('roleConfigForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('roleName').value,
            purpose: document.getElementById('rolePurpose').value,
            accountabilities: Array.from(document.querySelectorAll('#accountabilitiesList input')).map(input => input.value).filter(v => v),
            domains: document.getElementById('domains').value,
            policies: document.getElementById('policies').value,
            metrics: document.getElementById('metrics').value
        };
        
        // Show loading state
        const submitButton = e.target.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating Agent...';
        
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Show success message
            modalBody.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-check-circle text-success" style="font-size: 4rem;"></i>
                    <h4 class="mt-3">Agent Created Successfully!</h4>
                    <p class="text-muted">Your ${formData.name} agent is now ready to start working.</p>
                    <button class="btn btn-primary" onclick="window.location.href='/dashboard'">Go to Dashboard</button>
                </div>
            `;
        } catch (error) {
            console.error('Error creating agent:', error);
            submitButton.disabled = false;
            submitButton.innerHTML = 'Create Agent';
        }
    });
}

// Create Custom Role
function createCustomRole() {
    configureRole('custom');
}

// Add Accountability
function addAccountability() {
    const accountabilitiesList = document.getElementById('accountabilitiesList');
    const newInput = document.createElement('div');
    newInput.className = 'input-group mb-2';
    newInput.innerHTML = `
        <input type="text" class="form-control" placeholder="Add accountability...">
        <button class="btn btn-outline-danger" type="button" onclick="removeAccountability(this)">-</button>
    `;
    accountabilitiesList.appendChild(newInput);
}

// Remove Accountability
function removeAccountability(button) {
    button.parentElement.remove();
}

// Open Role Builder
function openRoleBuilder() {
    const modal = new bootstrap.Modal(document.getElementById('roleBuilderModal'));
    
    const modalBody = document.querySelector('#roleBuilderModal .modal-body');
    modalBody.innerHTML = `
        <div class="role-builder-interface">
            <h4>Interactive Role Builder</h4>
            <p class="text-muted">Build your perfect AI agent by defining its role and capabilities.</p>
            
            <div class="builder-steps">
                <div class="step active" data-step="1">
                    <h5>Step 1: Choose Base Template</h5>
                    <div class="row g-3 mt-2">
                        <div class="col-md-4">
                            <div class="template-option" onclick="selectTemplate('executive')">
                                <i class="bi bi-briefcase"></i>
                                <span>Executive</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="template-option" onclick="selectTemplate('specialist')">
                                <i class="bi bi-person-badge"></i>
                                <span>Specialist</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="template-option" onclick="selectTemplate('coordinator')">
                                <i class="bi bi-diagram-3"></i>
                                <span>Coordinator</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="step" data-step="2" style="display: none;">
                    <h5>Step 2: Define Core Attributes</h5>
                    <!-- Attributes form will be loaded here -->
                </div>
                
                <div class="step" data-step="3" style="display: none;">
                    <h5>Step 3: Set Performance Metrics</h5>
                    <!-- Metrics configuration will be loaded here -->
                </div>
            </div>
        </div>
    `;
    
    modal.show();
}

// Select Template
function selectTemplate(templateType) {
    // Move to next step
    const steps = document.querySelectorAll('.builder-steps .step');
    steps[0].style.display = 'none';
    steps[0].classList.remove('active');
    steps[1].style.display = 'block';
    steps[1].classList.add('active');
    
    // Load attributes form
    steps[1].innerHTML = `
        <h5>Step 2: Define Core Attributes</h5>
        <form class="mt-3">
            <div class="mb-3">
                <label class="form-label">Primary Function</label>
                <select class="form-select">
                    <option>Strategic Planning</option>
                    <option>Execution & Operations</option>
                    <option>Analysis & Reporting</option>
                    <option>Communication & Coordination</option>
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Autonomy Level</label>
                <input type="range" class="form-range" min="1" max="5" value="3">
                <div class="d-flex justify-content-between">
                    <small>Supervised</small>
                    <small>Fully Autonomous</small>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Collaboration Style</label>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="collab" id="collab1">
                    <label class="form-check-label" for="collab1">Independent Worker</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="collab" id="collab2" checked>
                    <label class="form-check-label" for="collab2">Team Player</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="collab" id="collab3">
                    <label class="form-check-label" for="collab3">Team Leader</label>
                </div>
            </div>
            <button type="button" class="btn btn-primary" onclick="moveToMetrics()">Next: Set Metrics</button>
        </form>
    `;
}

// Move to Metrics Step
function moveToMetrics() {
    const steps = document.querySelectorAll('.builder-steps .step');
    steps[1].style.display = 'none';
    steps[1].classList.remove('active');
    steps[2].style.display = 'block';
    steps[2].classList.add('active');
    
    steps[2].innerHTML = `
        <h5>Step 3: Set Performance Metrics</h5>
        <div class="mt-3">
            <div class="metric-config mb-3">
                <label class="form-label">Success Rate Target</label>
                <div class="input-group">
                    <input type="number" class="form-control" value="90" min="0" max="100">
                    <span class="input-group-text">%</span>
                </div>
            </div>
            <div class="metric-config mb-3">
                <label class="form-label">Response Time</label>
                <select class="form-select">
                    <option>< 1 minute</option>
                    <option selected>< 5 minutes</option>
                    <option>< 30 minutes</option>
                    <option>< 1 hour</option>
                </select>
            </div>
            <div class="metric-config mb-3">
                <label class="form-label">Quality Score Threshold</label>
                <input type="range" class="form-range" min="1" max="10" value="8">
                <div class="text-center">8/10</div>
            </div>
            <button type="button" class="btn btn-success" onclick="completeRoleBuilder()">Create Agent</button>
        </div>
    `;
}

// Complete Role Builder
function completeRoleBuilder() {
    const modalBody = document.querySelector('#roleBuilderModal .modal-body');
    modalBody.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p>Creating your custom agent...</p>
        </div>
    `;
    
    setTimeout(() => {
        modalBody.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-check-circle text-success" style="font-size: 4rem;"></i>
                <h4 class="mt-3">Agent Created!</h4>
                <p class="text-muted">Your custom agent is ready to start working.</p>
                <button class="btn btn-primary" onclick="window.location.href='/dashboard'">View in Dashboard</button>
            </div>
        `;
    }, 2000);
}

// Open ROI Calculator
function openROICalculator() {
    const modal = new bootstrap.Modal(document.getElementById('roiCalculatorModal'));
    
    const modalBody = document.querySelector('#roiCalculatorModal .modal-body');
    modalBody.innerHTML = `
        <form id="roiForm">
            <div class="mb-3">
                <label for="teamSize" class="form-label">Current Team Size</label>
                <input type="number" class="form-control" id="teamSize" value="5" min="1">
            </div>
            <div class="mb-3">
                <label for="avgSalary" class="form-label">Average Annual Salary</label>
                <div class="input-group">
                    <span class="input-group-text">$</span>
                    <input type="number" class="form-control" id="avgSalary" value="75000" min="0">
                </div>
            </div>
            <div class="mb-3">
                <label for="taskHours" class="form-label">Hours/Week on Repetitive Tasks</label>
                <input type="number" class="form-control" id="taskHours" value="20" min="0" max="40">
            </div>
            <div class="mb-3">
                <label for="errorRate" class="form-label">Current Error Rate (%)</label>
                <input type="number" class="form-control" id="errorRate" value="5" min="0" max="100">
            </div>
            <button type="button" class="btn btn-primary w-100" onclick="calculateROI()">Calculate ROI</button>
        </form>
        <div id="roiResults" class="mt-4" style="display: none;">
            <!-- Results will be displayed here -->
        </div>
    `;
    
    modal.show();
}

// Calculate ROI
function calculateROI() {
    const teamSize = parseInt(document.getElementById('teamSize').value);
    const avgSalary = parseInt(document.getElementById('avgSalary').value);
    const taskHours = parseInt(document.getElementById('taskHours').value);
    const errorRate = parseInt(document.getElementById('errorRate').value);
    
    // Calculate savings
    const hourlyRate = avgSalary / 2080; // Annual hours
    const weeklyTaskCost = teamSize * taskHours * hourlyRate;
    const annualTaskCost = weeklyTaskCost * 52;
    
    // Assume 80% automation efficiency
    const automationSavings = annualTaskCost * 0.8;
    
    // Error reduction savings (assume $1000 per error)
    const errorsPerYear = teamSize * 52 * 40 * (errorRate / 100);
    const errorReductionSavings = errorsPerYear * 0.7 * 1000; // 70% reduction
    
    const totalSavings = automationSavings + errorReductionSavings;
    const platformCost = teamSize * 2000 * 12; // $2000/month per agent
    const netSavings = totalSavings - platformCost;
    const roi = ((netSavings / platformCost) * 100).toFixed(0);
    
    // Display results
    const resultsDiv = document.getElementById('roiResults');
    resultsDiv.style.display = 'block';
    resultsDiv.innerHTML = `
        <div class="roi-breakdown">
            <h5 class="mb-3">Your Estimated ROI</h5>
            <div class="metric-row">
                <span>Annual Task Automation Savings:</span>
                <strong class="text-success">$${automationSavings.toLocaleString()}</strong>
            </div>
            <div class="metric-row">
                <span>Error Reduction Savings:</span>
                <strong class="text-success">$${errorReductionSavings.toLocaleString()}</strong>
            </div>
            <div class="metric-row">
                <span>Total Annual Savings:</span>
                <strong class="text-success">$${totalSavings.toLocaleString()}</strong>
            </div>
            <div class="metric-row">
                <span>Platform Investment:</span>
                <strong class="text-danger">-$${platformCost.toLocaleString()}</strong>
            </div>
            <hr>
            <div class="metric-row">
                <span>Net Annual Savings:</span>
                <strong class="text-primary">$${netSavings.toLocaleString()}</strong>
            </div>
            <div class="text-center mt-4">
                <h3 class="text-primary">${roi}% ROI</h3>
                <p class="text-muted">First Year Return on Investment</p>
            </div>
        </div>
        <style>
        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
        }
        </style>
    `;
}

// Open Complexity Analyzer
function openComplexityAnalyzer() {
    alert('Complexity Analyzer - Coming Soon!');
}

// Smooth Scrolling for Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Navbar background on scroll
    const navbar = document.getElementById('mainNav');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in', 'visible');
            }
        });
    }, observerOptions);
    
    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('fade-in');
        observer.observe(section);
    });
});

// Add navbar scrolled styles
const style = document.createElement('style');
style.textContent = `
    .navbar-scrolled {
        background-color: rgba(33, 37, 41, 0.95) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .template-option {
        padding: 2rem;
        text-align: center;
        border: 2px solid #e0e0e0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .template-option:hover {
        border-color: var(--primary-color);
        background: var(--light-color);
        transform: translateY(-2px);
    }
    .template-option i {
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }
`;
document.head.appendChild(style);
