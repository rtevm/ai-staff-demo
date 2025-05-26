# AI Staff Platform Demo

This is a demo version of the AI Staff Platform configured for easy deployment on Render.

## What's Been Done

✅ **Repository Structure** - Reorganized for Render deployment:
- `/api` - Contains the FastAPI application
- `/static` - Frontend assets (CSS, JS, images)
- `/templates` - HTML templates
- `/demo` - Demo data and examples
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration

✅ **Demo Mode** - Modified to work without API keys:
- AI service returns simulated responses in demo mode
- No OpenAI API key required
- Fully functional UI/UX demonstration

✅ **Environment Configuration** - Set up for Render:
- SQLite database for demo (no external DB needed)
- Auto-generated secret key
- CORS configured for public access

## What You Need to Do

### 1. Create a Public GitHub Repository

```bash
# Navigate to the demo directory
cd ai-staff-platform-demo

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial demo commit"

# Create a new PUBLIC repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ai-staff-platform-demo.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Render

1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Blueprint"
3. Connect your GitHub account
4. Select your `ai-staff-platform-demo` repository
5. Render will detect the `render.yaml` file
6. Click "Apply" to create the service
7. Wait 5-10 minutes for the build to complete

### 3. Access Your Demo

Once deployed, Render will provide a URL like:
```
https://ai-staff-platform-demo.onrender.com
```

Share this link for others to test your demo!

## Features Available in Demo

- ✅ Landing page with product overview
- ✅ Interactive dashboard
- ✅ CEO delegation interface
- ✅ Architecture diagrams
- ✅ Agent management (simulated)
- ✅ Task execution (demo responses)
- ✅ Performance analytics
- ✅ Team collaboration features

## Important Notes

- This is a demo version with simulated AI responses
- No real API calls are made in demo mode
- Database is SQLite (resets on redeploy)
- Perfect for showcasing UI/UX and concept

## Troubleshooting

If the deployment fails:
1. Check the Render logs for errors
2. Ensure all files were committed to GitHub
3. Verify the repository is public
4. Check that Python version is compatible

## Next Steps

After your demo is live, you can:
- Share the link in your application
- Monitor usage in Render dashboard
- Update by pushing to GitHub (auto-deploys)
- Upgrade to paid tier for private repos

---

**Demo URL:** [Your URL will appear here after deployment]
