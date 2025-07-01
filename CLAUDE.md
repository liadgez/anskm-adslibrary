##Standard Workflow
1. First think through the problem, read the codebase for relevant files, and write a plan to projectplan.md.
2. The plan should have a list of todo items that you can check off as you complete them
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the projectplan.md file with a summary of the changes you made and any other relevant information.

!!Don't forget to chec-off tasks you have already completed.

!!! when trying to run the project after it's done - Don't reinstall anything - dependencies are already installed.
   If there's a .venv folder, use .venv/bin/python (not system python/python3) to run
  scripts. If there's a package.json, use npm commands directly. Check if the app is
  already running with lsof -i :[PORT] or ps aux | grep [APP_NAME] - if found, it's
  already live. For port conflicts, increment the port number. Virtual environments and
  dependencies exist and work - use the project's specific executables, not system-wide
  ones.