from app.db.database import SessionLocal
from app.models.portfolio_models import Project, Skill, Experience
import json


def seed_data():
    db = SessionLocal()
    try:
        # Only seed if tables are empty
        if db.query(Project).count() == 0:
            projects = [
                Project(
                    title="UPEXCISE – State Excise Management System",
                    description="State-level excise management platform digitalizing liquor manufacturing and distribution supply chains across Uttar Pradesh.",
                    tech_stack=json.dumps(["Angular 8", "TypeScript", "RxJS", "Spring Boot", "REST APIs", "Git"]),
                    duration="~956 days",
                    highlights=json.dumps([
                        "Led frontend development for 500+ government stakeholders",
                        "Real-time inventory tracking dashboards",
                        "~25% reduction in system response time"
                    ]),
                    category="government",
                    live_url=None,
                    github_url=None,
                ),
                Project(
                    title="TNPDS – Tamil Nadu Public Distribution System",
                    description="Large-scale PDS portal serving millions of Tamil Nadu beneficiaries with responsive, accessible UI components.",
                    tech_stack=json.dumps(["Angular 14–20", "Angular Material", "TypeScript", "MySQL", "REST APIs"]),
                    duration="Ongoing",
                    highlights=json.dumps([
                        "Serves millions of beneficiaries",
                        "WCAG-accessible UI across mobile & desktop",
                        "99%+ system uptime"
                    ]),
                    category="government",
                ),
                Project(
                    title="UPPDS & MHPDS – Public Distribution Portals",
                    description="Developing and maintaining PDS portals for Uttar Pradesh and Maharashtra with seamless API integration.",
                    tech_stack=json.dumps(["Angular 14–20", "Angular Material", "TypeScript", "REST APIs", "Git"]),
                    duration="Ongoing",
                    highlights=json.dumps([
                        "Multi-state portal management",
                        "JWT Auth & RBAC implementation",
                        "Cross-functional Agile delivery"
                    ]),
                    category="government",
                ),
            ]
            db.add_all(projects)

        if db.query(Skill).count() == 0:
            skills = [
                Skill(category="Frontend",  name="Angular",           proficiency=95, icon="⚡"),
                Skill(category="Frontend",  name="TypeScript",         proficiency=90, icon="🔷"),
                Skill(category="Frontend",  name="RxJS",               proficiency=85, icon="🔁"),
                Skill(category="Frontend",  name="Angular Material",   proficiency=90, icon="🎨"),
                Skill(category="Frontend",  name="HTML5 / CSS3",       proficiency=92, icon="🌐"),
                Skill(category="Backend",   name="Spring Boot",        proficiency=30, icon="🌿"),
                Skill(category="Backend",   name="REST APIs",          proficiency=88, icon="🔗"),
                Skill(category="Database",  name="MySQL",              proficiency=50, icon="🗄️"),
                Skill(category="Tools",     name="Git",                proficiency=95, icon="🛠"),
                Skill(category="Tools",     name="Agile/Scrum",        proficiency=88, icon="♟"),
            ]
            db.add_all(skills)

        if db.query(Experience).count() == 0:
            experiences = [
                Experience(
                    role="Angular Developer",
                    company="OASYS Cybernetics",
                    location="Tiruchirappalli, India",
                    start_date="June 2022",
                    end_date=None,
                    current=True,
                    bullets=json.dumps([
                        "Architected SPAs using Angular 12–20 serving 1M+ users across 4 state government portals.",
                        "Improved application performance by ~35% via lazy loading & OnPush change detection.",
                        "Integrated 20+ REST APIs with RxJS pipelines, reducing frontend bugs by ~30%.",
                        "Built reusable Angular Material component library — cut feature delivery time by 25%.",
                        "Implemented JWT authentication and RBAC for multi-stakeholder government systems.",
                        "Mentored 2 junior developers; refactored legacy codebases, reducing complexity by 40%."
                    ]),
                ),
                Experience(
                    role="Shift Supervisor",
                    company="SCM Textile & Processing Mills",
                    location="Erode, India",
                    start_date="November 2021",
                    end_date="April 2022",
                    current=False,
                    bullets=json.dumps([
                        "Supervised daily production ensuring safety and consistent workflow targets.",
                        "Trained new staff and reduced material waste by 15% via stock rotation."
                    ]),
                ),
            ]
            db.add_all(experiences)

        db.commit()
    finally:
        db.close()
