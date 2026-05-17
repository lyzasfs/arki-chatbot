"""
app.py — Arki Chatbot Backend
SmartHireArch: Web-Based Hub Client Acquisition System
St. John Paul II College of Davao · May 2027

Run:
    pip install flask flask-cors
    python app.py

Then open index.html in a browser or at http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


# =============================================================================
#  KNOWLEDGE BASE — sourced directly from the SmartHireArch Capstone Paper
# =============================================================================
KNOWLEDGE = {

    # ── GENERAL / OVERVIEW ────────────────────────────────────────────────────

    "what_is_smarthirearch": """
**SmartHireArch** is a Web-Based Hub Client Acquisition System developed for architectural companies in Davao City.

It was built as a capstone project by **Phil P. Amper** and **Reymark V. Butad**, under the guidance of adviser **Gilbert D. Carnice, LPT**, submitted to the College of Information and Communications Technology at St. John Paul II College of Davao (May 2027).

**Why it exists:**
Most architectural firms still rely on email, spreadsheets, and paper-based records — causing delayed responses, data duplication, inconsistent information, and poor tracking of client inquiries and job applications.

**What it does:**
- Centralizes client inquiry submission and tracking
- Provides a web-based recruitment and applicant tracking system
- Gives administrators full oversight through a central dashboard
- Secures all data through role-based access control and password encryption

The system uses a **client-server architecture**: the frontend handles user interaction, the backend (PHP + MySQL) processes data securely.
""",

    "purpose": """
The purpose of SmartHireArch is to **modernize client acquisition and staff recruitment** for architectural firms in Davao City.

It replaces the outdated manual methods (email, spreadsheets, paper records) with a secure, centralized digital platform. This addresses key problems like:
- Slow response times to client inquiries
- Difficulty tracking application status
- Data duplication and human errors
- Lack of role-based access and data security
- No centralized place to manage both clients and applicants
""",

    "objectives": """
SmartHireArch has **three core objectives**:

1. **Centralized Client Inquiry System** — Develop a system for efficient submission and tracking of project requests from clients.

2. **Web-Based Recruitment & Applicant Tracking** — Integrate a recruitment module for streamlined application management, letting architects submit applications and track their progress.

3. **Secure, Role-Based Web Platform** — Implement password encryption, secure authentication, and role-based access control (RBAC) to improve data organization, communication, and decision-making.
""",

    "problem": """
SmartHireArch was developed to solve real problems faced by architectural firms in Davao City:

- **Slow response times** — Manual methods like email and spreadsheets delay responses to client inquiries and job applicants.
- **Data duplication and errors** — Traditional data management causes companies to duplicate data, lose information, and make human errors (Gulomkodirova, 2023).
- **Lack of system integration** — Firms without integrated digital systems lose the ability to share information efficiently and assess operations (Marín-Vinuesa et al., 2021).
- **Client confidence drops** — Digital delays and poor tracking reduce client trust (McLean & McLean, 2022).
- **Security risks** — Without role-based access control and secure storage, systems face greater risks of unauthorized access and data breaches (Kaur & Singh, 2021).
""",

    "scope": """
**Scope of SmartHireArch:**

- Operates through the **internet** via standard web browsers — no installation needed
- Supports **client inquiry submission** and tracking
- Supports **architect job applications** and recruitment management
- Includes **user authentication** and role-based access control
- Features **inquiry tracking** and basic reporting functions
- Designed specifically for **architectural firms in Davao City**
- Responsive design for both **desktop and mobile**

**Limitations:**
- Requires a **stable internet connection** — poor connectivity reduces functionality
- Communication is limited to the **built-in messaging system** only
- Does NOT include: automated analytics, AI applicant screening, or full project and financial management
""",

    # ── USER ROLES ────────────────────────────────────────────────────────────

    "roles": """
SmartHireArch has **three user roles**, each with specific access levels:

**1. Client**
- Submits project inquiries online
- Tracks the status of their project requests in real time
- Views architect profiles, specializations, years of experience, and portfolios
- Communicates with architects via the messaging system
- Receives automatic email notifications when their request is approved or rejected

**2. Architect**
- Creates and manages a professional profile
- Uploads portfolio and resume
- Browses and applies for job openings posted by the admin
- Tracks application status
- Maintains records of achievements

**3. Admin**
- Has full control of the entire platform via a 6-tab dashboard
- Reviews and approves/rejects client project requests
- Reviews and approves/rejects architect applications
- Manages all registered users
- Posts and manages job openings
- Communicates with clients and architects
- Toggles the hiring status (open or closed) on the landing page
""",

    # ── REGISTRATION & LOGIN ──────────────────────────────────────────────────

    "register": """
**How to Register on SmartHireArch:**

1. Visit the **Registration Page**
2. **Choose your role:**
   - **Client** — if you are looking to hire an architect
   - **Architect** — if you are seeking employment opportunities
3. Fill in your details: name, email, and password
4. The system uses **input validation** — error messages are shown in real time to help you correct mistakes
5. Submit the form to create your account

The registration is a **two-step process**: role selection first, then personal information entry.
""",

    "login": """
**How to Log In to SmartHireArch:**

1. Go to the **Login Page**
2. Enter your registered **email and password**
3. You will be redirected to your role-specific dashboard

Other features on the Login Page:
- **Redirect to Register** — for new users who don't have an account yet
- **Back to Home** button — returns to the public landing page

The page uses a **dark stone background and amber accent colors** for a clean, professional design.
""",

    # ── CLIENT FEATURES ───────────────────────────────────────────────────────

    "client": """
**Client Features in SmartHireArch:**

As a client, you can:
- **Submit project inquiries** through the online form
- **Track the status** of your project requests in real time
- **View architect profiles** — including specializations, years of experience, and project portfolios
- **Communicate** with architects via the built-in messaging system
- **Receive email notifications** when your request is approved or rejected by the admin

The client module is designed around the architectural service workflow — inquiry submission → consultation documentation → project requirement assessment → proposal preparation → status tracking → client onboarding.
""",

    "inquiry": """
**How Client Inquiries Work:**

1. A client logs in and submits a **project inquiry** through the system's online form
2. The inquiry enters the system and the client can **track its status** in real time
3. The **Admin** reviews the inquiry from the Projects tab of the dashboard
4. The admin either **approves or rejects** the project request
5. An **automatic email notification** is sent to the client informing them of the decision

This replaces the old manual process of sending emails and waiting for replies with no clear tracking.
""",

    # ── ARCHITECT FEATURES ────────────────────────────────────────────────────

    "architect": """
**Architect Features in SmartHireArch:**

As an architect, you can:
- **Create and manage** your professional profile
- **Upload your portfolio and resume** to showcase your work
- **Browse job openings** posted by the admin
- **Apply for jobs** directly through the system
- **Track your application status** in real time
- **Maintain records** of your professional achievements

Your profile is publicly visible on the **Landing Page** under the "Meet the Team" section, where clients can see your specializations and years of experience.
""",

    "portfolio": """
**Architect Portfolio & Profile:**

Architects can upload their **portfolio and resume** directly on their profile page within SmartHireArch.

On the **Landing Page**, clients and visitors can view:
- Architect profiles with specialization areas
- Years of experience
- Project galleries under "Our Works and Achievements"

This is a key differentiator from HubSpot and Zoho CRM — those systems do not support architect-specific profile pages or project galleries. Portfolio presentation directly influences a client's decision to hire, making this a critical feature for architectural firms.
""",

    # ── ADMIN FEATURES ────────────────────────────────────────────────────────

    "admin": """
**Admin Dashboard — SmartHireArch:**

The Admin Dashboard has **6 tabs**:

**1. Overview**
- Displays platform statistics and indicators
- Includes a **hiring status switch** — toggle applications open or closed
- Hiring status is reflected on the public Landing Page as a banner

**2. Users**
- View and manage all registered clients and architects
- Full user oversight from one screen

**3. Applications**
- Review architect applications including resumes and portfolios
- **Approve or reject** applications
- Automatic **email notification** is sent to the applicant upon decision

**4. Projects**
- View client project requests
- **Approve or reject** project inquiries
- Automatic **email notification** is sent to the client upon decision

**5. Jobs**
- Post new job openings
- Manage existing job postings for architect recruitment

**6. Messages**
- Communicate directly with clients and architects
- Centralized messaging system for all platform communication

The admin has **complete oversight and control** of the entire SmartHireArch platform.
""",

    "hiring_status": """
**Hiring Status Toggle (Admin Feature):**

The admin can **open or close architect applications** from the Overview tab of the dashboard using a hiring status switch.

- When **ON (Open):** A hiring status banner appears on the public-facing Landing Page, informing visitors that the firm is currently hiring architects.
- When **OFF (Closed):** The banner disappears and no new architect applications are accepted.

This gives the admin full control over the recruitment cycle without needing to modify any code.
""",

    # ── SYSTEM FEATURES ───────────────────────────────────────────────────────

    "features": """
**SmartHireArch Core Features:**

1. **Client Inquiry Tracking**
   - Clients submit project requests online
   - Real-time status tracking from submission to approval/rejection
   - Automatic email notifications

2. **Web-Based Recruitment & Applicant Tracking**
   - Architects apply for jobs through the platform
   - Admin reviews resumes and portfolios
   - Application status is tracked in real time

3. **Role-Based Access Control (RBAC)**
   - Three roles: Client, Architect, Admin
   - Each role has specific access rights — unauthorized access is blocked

4. **Admin Dashboard (6 tabs)**
   - Overview, Users, Applications, Projects, Jobs, Messages
   - Full platform control from one interface

5. **Built-In Messaging System**
   - Direct communication between clients, architects, and admin
   - No need for external email for in-platform communication

6. **Automatic Email Notifications**
   - Sent to applicants when their application is approved or rejected
   - Sent to clients when their project request is approved or rejected

7. **Architect Profile Pages**
   - Publicly visible on the Landing Page
   - Includes specializations, experience, portfolio/project gallery

8. **Hiring Status Banner**
   - Admin toggles whether the firm is currently hiring
   - Displayed dynamically on the Landing Page
""",

    # ── LANDING PAGE ──────────────────────────────────────────────────────────

    "landing_page": """
**SmartHireArch Landing Page:**

The Landing Page is the **public-facing homepage**, accessible to all visitors without requiring login.

It includes:
- **Dynamic Navigation Bar** — shows Login/Register for guests; shows dashboard link for logged-in users
- **Hero Section** — with a call-to-action encouraging visitors to explore the platform
- **About Us Section** — describes the architectural firm and its mission
- **Meet the Team** — showcases registered architects with their specializations and years of experience
- **Our Works and Achievements** — a gallery of completed architectural projects
- **Hiring Status Banner** — dynamically toggled by the admin (visible when hiring is open)
- **Contact Section** — for visitors to reach out to the firm

**Design:** Uses a professional **dark stone and amber color palette** to convey trust, elegance, and professionalism.
""",

    # ── SECURITY ──────────────────────────────────────────────────────────────

    "security": """
**SmartHireArch Security Features:**

SmartHireArch implements multiple layers of security:

**1. Password Encryption**
- All user passwords are stored encrypted — never in plain text
- Protects against unauthorized access even in the event of data exposure

**2. Secure Authentication**
- Users must be verified and authenticated before accessing any system feature
- Prevents unauthorized entry into client, architect, or admin areas

**3. Role-Based Access Control (RBAC)**
- Clients can only access their own inquiries and public architect profiles
- Architects can only manage their own profile and applications
- Admins have full access to all data and controls
- Prevents accidental or intentional cross-role data exposure

**4. Access Control Mechanisms**
- Adaptive security that blocks unauthorized activities
- Reduces the risk of data breaches (Soomro et al., 2021)

**References:** Almorsy et al. (2021); Rani et al. (2023); Kaur & Singh (2021); Zhang et al. (2022)
""",

    "rbac": """
**Role-Based Access Control (RBAC) in SmartHireArch:**

RBAC ensures each user only accesses what they are authorized to see:

- **Client** — can only view their own inquiries and public architect profiles
- **Architect** — can only manage their own profile, resume, portfolio, and applications
- **Admin** — has full access to all users, inquiries, applications, jobs, and messages

**Why RBAC matters:**
- Reduces the risk of unauthorized access and data breaches (Kaur & Singh, 2021)
- Improves operational efficiency by simplifying system management (Soomro et al., 2021)
- Ensures regulatory compliance with privacy standards (Fernandes et al., 2020)
- Rani et al. (2023) showed RBAC combined with encryption secures confidentiality, integrity, and availability of data
""",

    

    "technology": """
**SmartHireArch Technology Stack:**

| Software | Role | Requirements |
|---|---|---|
| **PHP 7.4+** | Server-side scripting — handles backend logic and data processing | Windows 10/11 (64-bit), XAMPP/WAMP/LAMP |
| **MySQL 5.7+** | Relational database — stores all client, architect, inquiry, and admin data | 2 GB RAM minimum (4 GB recommended) |
| **CSS** | Styling — layout, colors, responsive design | Modern web browser |
| **JavaScript** | Frontend interactivity — dynamic behavior, real-time updates | Modern browser with JS support |
| **Bootstrap** | Front-end framework — responsive, mobile-friendly components | Modern browser, internet connection |
| **Draw.io** | Diagramming tool used during system design | Web browser, cloud storage |

**Architecture:** Client-server model
- **Frontend** (HTML, CSS, JS, Bootstrap) — user interaction layer
- **Backend** (PHP) — business logic and data processing
- **Database** (MySQL) — secure, structured data storage
""",

    "hardware": """
**SmartHireArch Hardware Requirements:**

| Hardware | Minimum | Recommended |
|---|---|---|
| **Processor** | Intel Core i3 | Intel Core i5 (10th Gen) or i7 (11th Gen) |
| **RAM** | 4 GB | 8 GB or 16 GB |
| **OS** | Windows 10 (64-bit) | Windows 11 (64-bit) |
| **Web Server** | XAMPP, WAMP, or LAMP | XAMPP with PHP 7.4+ and MySQL 5.7+ |

A **laptop or desktop PC** is sufficient to run and develop SmartHireArch locally.
""",

    # ── SYSTEM ARCHITECTURE / IPO ─────────────────────────────────────────────

    "architecture": """
**SmartHireArch System Architecture:**

SmartHireArch uses a **client-server architecture**:

- **Frontend** — HTML, CSS, JavaScript, Bootstrap handle the user interface and interactions
- **Backend** — PHP processes all business logic (form submissions, approvals, notifications)
- **Database** — MySQL stores all structured data (users, inquiries, applications, job posts)

**Data flow:**
1. User interacts with the frontend (browser)
2. Request is sent to the PHP backend
3. Backend queries or writes to MySQL database
4. Response is returned and displayed to the user

This design **separates concerns** — the user interface is decoupled from data storage, and all sensitive processing happens on the server side.
""",

    "ipo": """
**SmartHireArch Conceptual Framework (IPO Model):**

SmartHireArch follows an **Input → Process → Output** framework:

---
**INPUT**
- Users (clients, architects, admins) register and log in via role-based access
- The system authenticates and identifies each user by role
- A centralized database receives: client info, project inquiries, applicant data, and admin actions

---
**PROCESS** — Three simultaneous workflows:

*Clients:*
- Submit project requests
- Track inquiry status
- View architect profiles, ratings, and achievements
- Communicate via the messaging system

*Architects:*
- Manage professional profiles
- Upload portfolios and resumes
- Submit job applications
- Track application status and achievements

*Admins:*
- Oversee all client inquiries and architect applications
- Approve or reject requests/applications
- Post job openings
- Monitor the entire platform via the dashboard

---
**OUTPUT**
- Client ratings and satisfaction data
- Recruitment analytics
- Profile view statistics
- System-generated reports
- These outputs support **transparency, better decisions, and ongoing improvements**
""",

    # ── RELATED SYSTEMS COMPARISON ────────────────────────────────────────────

    "comparison": """
**SmartHireArch vs. Related Systems:**

| Feature | HubSpot CRM | Zoho CRM | Upwork | SmartHireArch |
|---|---|---|---|---|
| Client Registration / Login | ✓ | ✓ | ✓ | ✓ |
| Client Inquiry Management | ✓ | ✓ | ✗ | ✓ |
| Request Status Tracking | ✓ | ✓ | ✗ | ✓ |
| Admin Dashboard | ✓ | ✓ | ✗ | ✓ |
| Recruitment / Applicant Tracking | ✗ | ✗ | ✓ | ✓ |
| Architect Profile Page | ✗ | ✗ | ✓ | ✓ |
| Centralized Firm-Based System | ✓ | ✓ | ✗ | ✓ |

**Key insight:**
- HubSpot and Zoho cover CRM well but lack architect profiles and recruitment features
- Upwork supports profiles and portfolios but is an open marketplace — not a firm-based internal system
- **SmartHireArch is the only system that combines all features in one platform tailored to architectural firms in Davao City**
""",

    "hubspot": """
**HubSpot CRM vs. SmartHireArch:**

HubSpot CRM is an enterprise-grade solution for managing customer interactions and sales pipelines. It supports:
- Client inquiry collection
- Customer interaction tracking
- Automated follow-up messages
- Analytical reports
- AI-powered analytics and marketing automation

**Limitations for architectural firms:**
- Built for general use across many industries (retail, healthcare, finance, marketing)
- Advanced features increase complexity and cost — problematic for small architectural firms
- Requires heavy customization to match architectural service workflows
- Does NOT support architect profile pages, project galleries, or recruitment tracking

**SmartHireArch advantage:** Designed specifically for architectural companies with structured client acquisition steps, architect profiles, and firm-specific admin workflows.
""",

    "zoho": """
**Zoho CRM vs. SmartHireArch:**

Zoho CRM is a cloud-based customer relationship management system with:
- Lead management and assignment
- Workflow automation
- Customizable reporting dashboards

**Limitations for architectural firms:**
- General-purpose system — requires customization for architectural-specific needs
- Does not natively support architect profile pages or project portfolios
- No built-in recruitment module

**SmartHireArch advantage:** Natively integrates client consultation tracking, service requirement documentation, project proposal management, and architect recruitment — purpose-built, no customization required.
""",

    "upwork": """
**Upwork vs. SmartHireArch:**

Upwork is a global freelance marketplace that allows clients to post projects and receive bids from service providers. It features:
- Freelancer profiles and portfolio display
- Proposal submission system
- Client-provider communication

**Limitations for architectural firms:**
- Open marketplace — not firm-specific or internal
- No centralized admin dashboard for one organization
- No structured client onboarding or inquiry management
- No internal recruitment workflow

**SmartHireArch advantage:** Serves as a **dedicated internal platform** for one architectural firm — managing long-term client relationships, structured inquiry workflows, and internal recruitment with admin control — not open marketplace bidding.
""",

    # ── PROTOTYPE / UI ────────────────────────────────────────────────────────

    "ui": """
**SmartHireArch Interface Overview:**

**Login Page (Figure 5)**
- Clean, minimalist layout with dark stone background and amber accents
- Users enter their registered email and password
- Redirects new users to the registration page
- Includes a "Back to Home" button

**Registration Page (Figure 6)**
- Two-step process: choose role first (Client or Architect), then fill in details
- Real-time input validation with clear error messages

**Landing Page (Figure 7)**
- Public-facing homepage accessible without login
- Dynamic nav bar (adapts based on login status)
- Sections: Hero, About Us, Meet the Team, Our Works, Hiring Banner, Contact

**Admin Dashboard (Figure 8)**
- 6 tabs: Overview, Users, Applications, Projects, Jobs, Messages
- Complete platform management from one interface
- Hiring status switch, automatic notifications, user management

**Design language:** Professional dark stone and amber color palette — conveys trust, elegance, and professionalism appropriate for an architectural firm.
""",

    # ── RESEARCH BACKGROUND ───────────────────────────────────────────────────

    "research": """
**Research Background for SmartHireArch:**

SmartHireArch is grounded in academic literature:

- **Digital transformation** improves decision-making and performance (Verhoef et al., 2021)
- **CRM systems** improve service delivery through client data management (Buttle & Maklan, 2022)
- **Web-based client acquisition systems** lead to higher customer satisfaction and trust (Chatterjee et al., 2021)
- **E-recruitment systems** accelerate hiring and improve communication (Allden et al., 2021)
- **Digital platforms** enable real-time access to organizational data (Sari et al., 2022)
- **RBAC + encryption** secures confidentiality, integrity, and availability (Rani et al., 2023)
- **Architectural firms** benefit from technology-based recruitment to verify qualified labor (Oesterreich & Teuteberg, 2020)
""",

    "team": """
**SmartHireArch Development Team:**

- **Phil P. Amper** — Developer
- **Reymark V. Butad** — Developer
- **Gilbert D. Carnice, LPT** — Adviser

Submitted to the **College of Information and Communications Technology**
**St. John Paul II College of Davao** — May 2027

Degree: **Bachelor of Science in Information Technology**
""",
}


# =============================================================================
#  INTENT MAP — keywords mapped to knowledge keys
#  More entries = smarter and more accurate matching
# =============================================================================
INTENT_MAP = [
    # General
    (["what is smarthirearch", "smarthirearch about", "about smarthirearch",
      "tell me about", "overview", "explain smarthirearch", "what does smarthirearch do",
      "introduce", "describe the system"],
     "what_is_smarthirearch"),

    (["purpose", "goal", "aim", "why was it made", "why was smarthirearch",
      "reason for", "what is the purpose"],
     "purpose"),

    (["objective", "objectives", "what does it aim", "aims of"],
     "objectives"),

    (["problem", "issue", "challenge", "what problem", "problems solved",
      "statement of the problem", "why was it needed"],
     "problem"),

    (["scope", "limitation", "coverage", "what it cannot", "not supported",
      "what is not included", "disadvantage", "does not support"],
     "scope"),

    # Roles
    (["role", "roles", "user type", "user roles", "types of user",
      "who can use", "who uses smarthirearch"],
     "roles"),

    # Registration & Login
    (["register", "sign up", "create account", "new account", "how to register",
      "registration page", "create a user"],
     "register"),

    (["login", "log in", "sign in", "how to login", "access the system",
      "how do i access", "enter the system"],
     "login"),

    # Client
    (["client feature", "client can", "what can a client",
      "client role", "what does a client do", "as a client"],
     "client"),

    (["inquiry", "inquiries", "submit project", "project request",
      "how to submit", "project inquiry", "send a request"],
     "inquiry"),

    # Architect
    (["architect feature", "architect can", "what can an architect",
      "architect role", "what does an architect do", "as an architect",
      "apply as architect", "how do i apply"],
     "architect"),

    (["portfolio", "resume", "upload resume", "upload portfolio",
      "showcase work", "architect profile"],
     "portfolio"),

    # Admin
    (["admin feature", "admin can", "what can the admin",
      "admin role", "what does an admin do", "administrator"],
     "admin"),

    (["dashboard", "admin dashboard", "control panel",
      "6 tabs", "six tabs", "tabs in the dashboard"],
     "admin"),

    (["hiring status", "toggle hiring", "open hiring",
      "close hiring", "hiring banner", "hiring switch"],
     "hiring_status"),

    # Features
    (["feature", "features", "what can it do", "capabilities",
      "functions", "main function", "core features", "system features",
      "what features", "list of features"],
     "features"),

    # Landing Page
    (["landing page", "homepage", "home page", "public page",
      "main page", "front page"],
     "landing_page"),

    # Security
    (["security", "secure", "protection", "data safety",
      "how is data protected", "encryption", "password", "safe"],
     "security"),

    (["rbac", "role based access", "role-based access",
      "access control", "authorization", "permissions"],
     "rbac"),

    # Technology
    (["technology", "tech stack", "built with", "programming language",
      "php", "mysql", "bootstrap", "javascript", "what language",
      "tools used", "software used"],
     "technology"),

    (["hardware", "computer", "specs", "specifications",
      "hardware requirements", "what computer", "system requirements"],
     "hardware"),

    # Architecture / IPO
    (["system architecture", "client server", "how is it designed",
      "technical design", "architecture of the system"],
     "architecture"),

    (["ipo", "input process output", "conceptual framework",
      "framework", "ipo model", "how the system works overall"],
     "ipo"),

    # Comparisons
    (["hubspot", "hub spot", "compare hubspot", "hubspot vs"],
     "hubspot"),

    (["zoho", "zoho crm", "compare zoho", "zoho vs"],
     "zoho"),

    (["upwork", "compare upwork", "upwork vs"],
     "upwork"),

    (["comparison", "compare", "vs", "difference", "similar system",
      "related system", "comparison matrix", "other systems"],
     "comparison"),

    # UI / Prototype
    (["interface", "ui", "design", "prototype", "what does it look like",
      "screen", "page design", "login page", "registration page", "how it looks"],
     "ui"),

    # Research
    (["research", "literature", "study", "references", "related literature",
      "theoretical", "based on", "authors cited"],
     "research"),

    # Team
    (["team", "developers", "who made", "who built",
      "creator", "authors", "who created", "who developed",
      "developer", "adviser"],
     "team"),
]

GREETINGS = {"hi", "hello", "hey", "good morning", "good afternoon",
             "good evening", "howdy", "greetings", "sup", "what's up"}

THANKS = {"thank", "thanks", "thank you", "ty", "appreciate", "helpful"}
FAREWELL = {"bye", "goodbye", "see you", "take care", "later", "ciao"}

FALLBACK = """I'm **Arki** 👋 — your SmartHireArch assistant!

I can answer questions about:
- **System overview** — what SmartHireArch is and why it was built
- **User roles** — client, architect, and admin
- **Client features** — inquiry submission, tracking, messaging
- **Architect features** — profile, portfolio, job applications
- **Admin dashboard** — all 6 tabs and what each one does
- **Security** — RBAC, encryption, authentication
- **Technology stack** — PHP, MySQL, Bootstrap, JavaScript
- **System comparison** — vs HubSpot, Zoho CRM, and Upwork
- **IPO framework** — how the system works conceptually
- **Team & background** — who built it and why

Try asking: *"What does the admin dashboard do?"* or *"How do I register as an architect?"*"""




def normalize(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def get_reply(user_msg: str) -> str:
    clean = normalize(user_msg)

    
    if any(g == clean or clean.startswith(g + " ") for g in GREETINGS):
        return (
            "**Hello! 👋** I'm Arki, your SmartHireArch assistant.\n\n"
            "SmartHireArch is a web-based hub client acquisition system for architectural "
            "firms in Davao City. I know everything about it!\n\n"
            "What would you like to know? You can ask about registration, features, "
            "user roles, the admin dashboard, security, or how it compares to other systems."
        )

    
    if any(t in clean for t in THANKS):
        return "You're welcome! 😊 Feel free to ask anything else about SmartHireArch anytime."

    # ── Farewell ─────────────────────────────────────────────────────────────
    if any(f in clean for f in FAREWELL):
        return "Goodbye! 👋 Come back anytime you have questions about SmartHireArch."

    # ── Score-based intent matching ──────────────────────────────────────────
    # Count how many keywords from each intent match the user's message.
    # Pick the intent with the highest score.
    best_key = None
    best_score = 0

    for keywords, key in INTENT_MAP:
        score = sum(1 for kw in keywords if kw in clean)
        if score > best_score:
            best_score = score
            best_key = key

    if best_key and best_score >= 1:
        return KNOWLEDGE.get(best_key, FALLBACK).strip()

    return FALLBACK


# =============================================================================
#  ROUTES
# =============================================================================

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type a message!"})

    reply = get_reply(user_msg)
    return jsonify({"reply": reply})


# =============================================================================
#  ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  Arki — SmartHireArch Chatbot Backend")
    print("  Running at: http://localhost:5000")
    print("  Press CTRL+C to stop")
    print("=" * 55)
    app.run(debug=True, port=5000)