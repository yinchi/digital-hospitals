# Todo list

- [ ] Add documentation for Simulation module
    - Description of job orchestrator (Rohit?)
    - Description of simulation config
    - How are configs injected into each new job instance?
- Simulation module &mdash; implementation
    - [ ] Initial: base simulation with no module connections
    - [ ] Switch to new method of defining resource schedules
    - [ ] BIM integration assuming lift is always working
        - As in BIM-DES paper (submitted to Automation in Construction)
    - [ ] Add lift status check
- Simulation module &mdash; API and job orchestrator
    - [ ] FastAPI endpoints
    - [ ] Kubernetes? (Rohit)
        - [Python hook](https://github.com/kubernetes-client/python)
        - How will the FastAPI service communicate with the Kubernetes host?
        - Integration with existing Docker Compose setup in this project?
    - Versioning?
        - We will need to have a good versioning system as we incorporate more of the other modules into the simulation setup (see "Implementaton" section above)
- [ ] Asset status module
- [ ] BIM module
    - BackgroundTask implementation currently not working, and impossible to get error messages from background task
    - Use Kubernetes to run background task? (Rohit)
    - If error does occur, need way to get error message into MongoDB
- [ ] Stock management module
- [ ] Resource scheduling module
- Deployment
    - [ ] Set up server &mdash; which machine/URLs?
    - [ ] Git hooks? Whenever a "git push" event is triggered:
        - Build container images
        - Restart certain containers (e.g. front-ends)
        - Kubernetes host will use new versions of containers when launching new jobs
