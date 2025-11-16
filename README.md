# SkillCreatorAgency – Agency Swarm Starter

A production-ready starter for running a single-agent Agency Swarm setup that uses a standalone
Claude Skills MCP backend and a `skill_creator` agent for managing skills and tools.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Add any additional API keys your agents need
# EXAMPLE_API_KEY=your_api_key_here
```

### 3. Run the standalone Claude Skills MCP backend

In one terminal:

```bash
source venv/bin/activate
python scripts/start_claude_skills_mcp.py
```

This starts the `claude-skills-mcp-backend` HTTP MCP server (vector search, sentence-transformers,
PyTorch, etc.) using `claude-skills-mcp-config.json` and loading skills from `mnt/skills`.

Leave this terminal running.

### 4. Run the SkillCreatorAgency

In another terminal:

```bash
source venv/bin/activate
python agency.py
```

`agency.py` only connects to the already-running MCP backend; it will not attempt to start it.
If the backend is not detected, it prints instructions on how to start it and exits.

---

## 🧩 Using the SkillCreatorAgency to Build New Skills

Once both the Claude Skills backend and the agency are running, you can use the terminal UI to create
and iterate on skills.

### 1. Inspect existing skills

In the interactive terminal started by `python agency.py`, you can simply ask:

- `What skills are available?`

The `skill_creator` agent will:

- Call `Claude_Skills.find_helpful_skills` to semantically search for relevant skills.
- Call `Claude_Skills.list_skills` to show the full inventory, including:
  - Skill names
  - Short descriptions
  - Source paths under `mnt/skills`.

### 2. Create a new skill (e.g. reporting-skill)

Example conversation:

- You: `I want to create a new reporting skill.`
- Agent:
  - Uses the `skill-creator` skill to plan the new skill.
  - Asks a short set of questions (name, description, data sources, outputs, delivery, etc.).
  - You can answer in detail or say: `use defaults`.

Under the hood, the agent will:

- Run `python3 ./mnt/skills/skill-creator/scripts/init_skill.py <skill-name> --path ./mnt/skills/<folder>`
  via the `PersistentShellTool`.
- Initialize a new skill folder like:

  - `mnt/skills/reporting-skill/`
    - `SKILL.md`
    - `scripts/`
    - `references/`
    - `assets/`

- Optionally overwrite `SKILL.md` and add starter scripts such as:

  - `scripts/generate_report.py` – data in (CSV/SQLite), reports out (CSV/XLSX/PDF), optional email.

### 3. Iterate on the new skill

From there you can:

- Ask the agent to:
  - Open or modify `SKILL.md`.
  - Edit or add scripts under `scripts/`.
  - Add reference docs or assets.
- Use the built-in validation and packaging scripts from the `skill-creator` skill:

  ```bash
  python3 ./mnt/skills/skill-creator/scripts/quick_validate.py ./mnt/skills/<folder>/<skill-name>
  python3 ./mnt/skills/skill-creator/scripts/package_skill.py ./mnt/skills/<folder>/<skill-name> ./dist
  ```

This pattern works for any new skill you want to build (reporting, PDF processing, dashboards, etc.):
you describe the skill conversationally, and the `skill_creator` agent orchestrates `init_skill.py`,
file edits, validation, and packaging for you.

---

## 🏗️ Project Structure

```
agency-starter-template/
├── agency.py                 # Main entry point (SkillCreatorAgency)
├── main.py                   # FastAPI integration entrypoint (do not modify)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container configuration
├── .env                      # Environment variables (create this)
├── AGENTS.md                 # Agent-creation workflow and instructions
├── shared_instructions.md    # Shared instructions for the agency
├── claude-skills-mcp-config.json   # Backend config (skills, embeddings, etc.)
├── scripts/
│   └── start_claude_skills_mcp.py  # Script to start standalone MCP backend
├── skill_creator/
│   ├── __init__.py
│   ├── skill_creator.py      # `skill_creator` Agent definition
│   ├── instructions.md       # Agent-specific instructions
│   ├── files/                # Local files accessible to the agent
│   └── tools/
│       └── __init__.py
├── servers/
│   └── claude_skills/        # Thin Python wrappers around Claude Skills MCP tools
│       ├── __init__.py
│       ├── find_helpful_skills.py
│       ├── list_skills.py
│       ├── read_skill_document.py
│       └── server.py
├── mnt/
│   └── skills/
│       └── skill-creator/    # Local skill for this repo
│           ├── SKILL.md
│           ├── LICENSE.txt
│           └── scripts/
│               ├── init_skill.py
│               ├── package_skill.py
│               └── quick_validate.py
├── tests/
│   ├── test_agency.py
│   └── test_claude_skills.py
└── venv/                     # Local virtualenv (not committed)
```

---

## 🔧 Creating Your Own Agency

### 🤖 **AI-Assisted Agency Creation with Cursor**

This template includes **AI-powered agency creation** using Cursor IDE:

1. **Open this project in Cursor IDE**

2. **Use the AI Assistant** to create your agency by referencing:
   ```
   📁 .cursor/rules/workflow.mdc
   ```
3. **Simply ask the AI:**

   > "Create a new agency using the .cursor workflow"

   The AI will guide you through the complete 7-step process:

   - ✅ PRD Creation
   - ✅ Folder Structure Setup
   - ✅ Tool Development
   - ✅ Agent Creation
   - ✅ Agency Configuration
   - ✅ Testing & Validation
   - ✅ Iteration & Refinement

### 📋 **What the AI Will Do For You**

The AI assistant will automatically:

- Create proper folder structures
- Generate agent classes and instructions
- Build custom tools with full functionality
- Set up communication flows
- Create the main agency file
- Test everything to ensure it works

### 🚀 **Manual Alternative (Advanced Users)**

If you prefer manual setup, replace the `ExampleAgency/` folder with your own agency structure following the Agency Swarm conventions.

### Agency Structure Requirements

Your agency must follow this structure:

- **Agency Folder**: Contains all agents and manifesto
- **Agent Folders**: Each agent has its own folder with:
  - `AgentName.py` - Agent class definition
  - `instructions.md` - Agent-specific instructions
  - `tools/` - Folder containing agent tools
- **agency_manifesto.md** - Shared instructions for all agents

---

## 🚀 Production Deployment

This repo is compatible with the Agencii platform and standard Agency Swarm deployment patterns,
but it is first and foremost a local-first SkillCreatorAgency starter. You can adapt the existing
`Dockerfile` and `main.py` for your preferred hosting environment.

---

## 🔨 Development Workflow

### **🎯 Recommended: AI-Assisted Development**

1. **Open Cursor IDE** with this template
2. **Ask the AI**: _"Create a new agency using the .cursor workflow"_
3. **Follow the guided process** - the AI handles everything automatically
4. **Test your agency**: `python agency.py`
5. **Deploy to production**: Install [Agencii GitHub App](https://github.com/apps/agencii) and push to main

### **⚙️ Manual Development (Advanced)**

If you prefer hands-on development:

1. **Create Tools**: Build agent tools in `tools/` folders
2. **Configure Agents**: Write `instructions.md` and agent classes
3. **Test Locally**: Run `python agency.py`
4. **Deploy**: Push to your preferred platform

The `.cursor/rules/workflow.mdc` file contains the complete development specifications for manual implementation.

---

## 📚 Key Features

- **🌐 Agencii Cloud Deploy**: One-click deployment to [Agencii platform](https://agencii.ai/)
- **🤖 AI-Assisted Creation**: Built-in Cursor IDE workflow for automated agency development
- **🔄 Auto-Deploy**: Automatic deployment on push to main branch
- **🚀 Ready-to-Deploy**: Dockerfile and requirements included
- **🔧 Modular Structure**: Easy to customize and extend
- **🛠️ Example Implementation**: Complete working example
- **📦 Container Ready**: Docker configuration for any platform
- **🔒 Environment Management**: Secure API key handling via Agencii dashboard
- **🧪 Local Testing**: Terminal demo for development
- **📋 Guided Workflow**: 7-step process with AI assistance

---

## 📖 Learn More

- **[Agency Swarm Documentation](https://agency-swarm.ai/)**
- **[Agency Swarm GitHub](https://github.com/VRSEN/agency-swarm)**

---

## Credits & Licenses

- This project is licensed under the MIT License (see `LICENSE`).
- It is based on and inspired by:
  - [agency-ai-solutions/agency-starter-template](https://github.com/agency-ai-solutions/agency-starter-template/blob/main/README.md)
  - [K-Dense-AI/claude-skills-mcp](https://github.com/K-Dense-AI/claude-skills-mcp/blob/main/README.md)
- The `skill-creator` skill under `mnt/skills/skill-creator/` is distributed under the Apache 2.0 License (see its `LICENSE.txt`).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## ⚡ Quick Tips

- **Start Small**: Begin with 1-2 agents and expand
- **Test Tools**: Each tool should work independently
- **Clear Instructions**: Write detailed agent instructions
- **Environment Setup**: Always use `.env` for API keys
- **Documentation**: Update instructions as you develop

---

**Ready to build your AI agency?** 🤖✨

### 🌐 **Production Route (Recommended)**

1. **Sign up** at [agencii.ai](https://agencii.ai/)
2. **Use this template** to create your repository
3. **Install** [Agencii GitHub App](https://github.com/apps/agencii)
4. **Push to main** → Automatic deployment!

### 🛠️ **Development Route**

Open this template in **Cursor IDE** and ask the AI to create your agency using the `.cursor` workflow. The AI will handle everything from setup to testing automatically!