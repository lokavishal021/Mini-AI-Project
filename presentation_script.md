# OmniBot-AI DevOps Presentation Script

**Goal:** Presenting OmniBot-AI with full Cloud Automation & DevOps Lifecycle.
**Time:** ~5-7 minutes

---

### 1. The Introduction (Setting the Stage)

*(Open VS Code so the teacher can see your project folders on the left side)*

**You say:** 
> "Good morning/afternoon! Today I will be presenting my project, OmniBot-AI. While the core of the project is an AI Chatbot, my primary focus for this presentation is on the **DevOps and Cloud Automation** infrastructure that I built around it. I have implemented a complete, enterprise-grade DevOps lifecycle, covering everything from Infrastructure as Code to Container Orchestration."

---

### 2. Cloud Automation - Infrastructure (Terraform)

*(Click and open the `terraform` folder, then open `main.tf`)*

**You say:**
> "I started by automating the cloud infrastructure. Instead of manually creating servers on AWS, I used **Terraform**. As you can see in this `main.tf` file, I have defined my infrastructure as code. This specific block automatically provisions an Amazon EC2 cloud server (`t2.micro`) to host the bot. This guarantees our infrastructure is reproducible and version-controlled."

---

### 3. Cloud Automation - Configuration (Ansible)

*(Click and open the `ansible` folder, then open `setup.yml`)*

**You say:**
> "Once the server is created, it needs to be configured. Instead of logging into the server manually, I used **Ansible** for Configuration Management. If you look at this `setup.yml` file, this playbook automatically connects to the new server and installs necessary dependencies, like Docker, ensuring the environment is perfectly prepared for our application without any human intervention."

---

### 4. Containerization (Docker)

*(Click and open the `Dockerfile` at the root of the project)*

**You say:**
> "Next, to ensure the OmniBot runs exactly the same way on my laptop as it does in the cloud, I containerized the application using **Docker**. This `Dockerfile` packages the Python environment, installs the `requirements.txt`, and isolates the application."

*(Optional: Open Terminal and run this command)*
**Action:** Type `docker-compose up -d` in the terminal.
**You say:**
> "I also added a `docker-compose.yml` file for local automation. By just running `docker-compose up`, the entire stack spins up locally in seconds."
*(Expected Output: The terminal will show `Creating omnibot ... done`)*

---

### 5. Orchestration & Scaling (Kubernetes)

*(Click and open the `k8s` folder. Open `hpa.yaml` and `deployment.yaml`)*

**You say:**
> "For production deployment, running a single Docker container isn't enough. So, I orchestrated the application using **Kubernetes**. I wrote several manifests, but the most important for Cloud Automation is this `hpa.yaml` file."

*(Point to the code in `hpa.yaml`)*

**You say:**
> "This is the **Horizontal Pod Autoscaler**. I configured it so that if the CPU utilization of the chatbot goes over 70%, Kubernetes will automatically scale the application up to 5 replicas. When traffic drops, it scales back down to 1. This is true elastic cloud automation."

---

### 6. Continuous Integration (GitHub Actions)

*(Click and open the `.github/workflows` folder)*

**You say:**
> "To tie the development process together, I implemented Continuous Integration. Whenever I push new AI code to GitHub, this workflow automatically triggers. It tests the code and builds a fresh Docker image, ensuring that buggy code never reaches the production server."

---

### 7. Observability & Monitoring (Prometheus/Grafana)

*(Click and open the `monitoring` folder, then open `prometheus.yml`)*

**You say:**
> "Finally, you can't have DevOps without Observability. I integrated **Prometheus** to constantly scrape metrics from the chatbot, such as memory usage and response times. This allows us to visualize the health of the application on a Grafana dashboard and get automated alerts if the server goes down."

---

### 8. Conclusion

**You say:**
> "In conclusion, I didn't just build an AI Chatbot; I built a fully automated software delivery pipeline. From provisioning the cloud (Terraform), to configuring it (Ansible), packaging the app (Docker), scaling it (Kubernetes), and monitoring it (Prometheus), the entire lifecycle is automated."
> "Are there any specific files or configurations you would like me to explain further?"
