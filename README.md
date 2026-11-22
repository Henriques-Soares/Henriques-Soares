<h1 align="center">Hi, I'm Henriques 👋</h1>

<p align="center">
  <b>IT Risk & Governance Analyst @ Bradesco</b> · <b>Computer Engineering @ FIAP</b><br>
  I work where technology meets risk, and I build systems that are secure by design.
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/henriques-soares"><img src="https://img.shields.io/badge/LinkedIn-henriques--soares-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:henriquessoareshs@gmail.com"><img src="https://img.shields.io/badge/Email-Get%20in%20touch-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>

---

### 🧭 About me

- 🏦 I work in **IT Governance & IT Risk Advisory** at Bradesco, one of Brazil's largest banks.
- 🎓 **Computer Engineering** student at FIAP.
- 🔐 I like the full picture: understanding the risk, designing the control and writing the code that enforces it.
- 🌍 Based in São Paulo 🇧🇷, with Angolan roots 🇦🇴.

### 🔐 What I focus on

| Area | Topics |
|---|---|
| **Security engineering** | PKI & mTLS, network segmentation, WireGuard VPN, SIEM detection & response, MITRE ATT&CK |
| **Governance, Risk & Compliance** | Risk assessment, security controls, least privilege, audit trails |
| **Defensive AI** | Anomaly detection, LLM guardrails (OWASP Top 10 for LLM, MITRE ATLAS) |
| **Software development** | Java & Spring Boot, Python, TypeScript & React Native |

### 🚀 Featured project

#### [Vila Aurora: Secure & Resilient Community Infrastructure](https://github.com/Henriques-Soares/gs-vila-aurora)

A working lab of a secure IoT network for five community spaces (a school, a health unit, a shelter and more), designed to keep running even when the internet goes down.

- **No shared secrets:** every device has its own X.509 certificate issued by the project CA, with revocation (CRL) and rotation.
- **Defense in depth:** MQTT broker with mTLS and per-device ACLs, a WireGuard tunnel between edge and cloud, and segmented networks.
- **Detection & response:** a custom SIEM with 4 rules mapped to MITRE ATT&CK. Low-risk threats are contained automatically; high-impact actions require human approval.
- **Access control:** password + TOTP MFA, role-based access, CSRF protection and a full audit trail.
- **Defensive AI:** Isolation Forest anomaly detection and guardrails against prompt injection and data leakage.
- **Resilience:** edge nodes keep operating offline and reconcile with the cloud without losing data.

`Python` `Docker` `PostgreSQL` `MQTT` `WireGuard` `OpenSSL` `Flask`

### 🧩 More projects

| Project | What it does | Stack |
|---|---|---|
| [medical-appointments-api](https://github.com/Henriques-Soares/medical-appointments-api) | Appointment scheduling REST API with JWT authentication and BCrypt password hashing | Java 17 · Spring Boot · Spring Security · H2 |
| [medical-appointments-app](https://github.com/Henriques-Soares/medical-appointments-app) | Mobile app to book and manage medical appointments | React Native · TypeScript |
| [digital-twin-sensors-app](https://github.com/Henriques-Soares/digital-twin-sensors-app) | Mobile app to monitor Digital Twin sensors, using a live API or mock data | React Native · Expo |
| [digital-twin-sensors-api](https://github.com/Henriques-Soares/digital-twin-sensors-api) | REST API that stores the sensor readings used by the app above | Java · Spring Boot · H2 |
| [landslide-risk-monitor](https://github.com/Henriques-Soares/landslide-risk-monitor) | Early-warning simulation that scores landslide risk from soil moisture and slope | React Native |
| [datawork-app](https://github.com/Henriques-Soares/datawork-app) | Productivity analytics with task tracking, KPIs and charts | React Native · Expo |

### 🛠️ Tech stack

<p>
  <img src="https://skillicons.dev/icons?i=java,spring,python,ts,react,docker,postgres,mysql,linux,git&perline=10" alt="Java, Spring, Python, TypeScript, React Native, Docker, PostgreSQL, MySQL, Linux, Git">
</p>

---

<p align="center"><i>Always happy to talk about security engineering, GRC and building technology for Africa.</i></p>
