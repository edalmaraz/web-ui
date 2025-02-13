# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Git
- Windows OS (for Windows-specific functions)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/edalmaraz/web-ui.git
cd web-ui
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for development
```

4. Configure Git:
```bash
git config user.email "terry.wagner@example.com"
git config user.name "Terry Wagner"
```

## Running the Application

1. Start the Web UI Launcher:
```bash
python launcher.py
```

2. Configure the System:
   - Enable "Hierarchical Management" for agent system
   - Enable "Double-Check Mode" for result verification
   - Configure task parameters in the Task Configuration tab

3. Monitor and Control:
   - Use the Control tab for system settings
   - Monitor agent activities in the Activity Log tab
   - View agent hierarchy in the Visualization tab
   - Track result reconciliation in the Reconciliation tab

## Key Features

### Agent System
- Hierarchical management with Director → Sub-Directors → Managers → Agents
- Specialized agents for different task types
- Double-check mode for result verification
- Real-time activity monitoring

### Task Configuration
- Basic parameters: Complexity, Scope, Urgency
- Advanced parameters: Task Type, Priority, Timeout
- Resource allocation preview

### Safety Features
- Emergency stop (Ctrl+Shift+X or GUI button)
- Function control system
- Activity logging and monitoring

## Common Operations

### Adding New Tasks
1. Go to Task Configuration tab
2. Set task parameters
3. Update preview to see resource allocation
4. Submit task through the system

### Monitoring Activities
1. Open Activity Log tab
2. Use filters to find specific activities
3. Export logs if needed

### Emergency Stop
- Press Ctrl+Shift+X
- Click the red Emergency Stop button
- All operations will halt immediately

## Troubleshooting

### Common Issues
1. **Agent System Not Starting**
   - Check if Hierarchical Management is enabled
   - Verify Python dependencies are installed

2. **Visualization Not Updating**
   - Refresh the view using Update Preview
   - Restart the application if persists

3. **Emergency Stop Not Working**
   - Check if the overlay window is running
   - Verify keyboard shortcuts are not conflicting

### Getting Help
- Check the logs in the `logs` directory
- Refer to documentation in the `docs` folder:
  - HELP.md for common issues
  - USER_MANUAL.md for detailed usage
  - ADVANCED_FEATURES.md for complex features

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Create feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and test thoroughly
3. Commit changes:
```bash
git add .
git commit -m "Description of changes"
```

4. Create pull request for review

## Security Notes
- Keep API keys in environment variables
- Regularly update dependencies
- Review function control settings
- Monitor agent activities for unusual patterns
