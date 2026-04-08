"""
Initialize database and create admin user.
Run: python init_db.py
"""
from app import app
from models import db, User, Article, Experience, ResumeSection
from config import Config
import json


def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Create admin user if not exists
        admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
        if not admin:
            admin = User(username=Config.ADMIN_USERNAME)
            admin.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin)
            print(f"Admin user created: {Config.ADMIN_USERNAME}")
        else:
            print(f"Admin user already exists: {Config.ADMIN_USERNAME}")

        # Create sample article if none exist
        if Article.query.count() == 0:
            sample = Article(
                title="Добро пожаловать в блог!",
                date="2024-01-01",
                excerpt="Это ваш первый пост. Отредактируйте или удалите его.",
                content="# Добро пожаловать\n\nЭто ваш первый пост в блоге.",
                tags="блог, пример"
            )
            db.session.add(sample)
            print("Sample article created")
        else:
            print("Articles already exist, skipping sample")

        # Create resume sections if not exist
        if ResumeSection.query.filter_by(section_type='hero').count() == 0:
            hero = ResumeSection(
                section_type='hero',
                content=json.dumps({
                    'name': 'Галкин Александр',
                    'position': 'Senior AQA / LeadAQA Python',
                    'age': '39 лет, родился 5 мая 1986',
                    'experience': '12+ лет опыта'
                })
            )
            db.session.add(hero)

        if ResumeSection.query.filter_by(section_type='about').count() == 0:
            about = ResumeSection(
                section_type='about',
                content=json.dumps({
                    'description': 'Моя главная цель как QA — помогать развитию компании, повышая качество программного обеспечения.',
                    'highlight1': {'value': '6+ лет', 'label': 'в QA Automation'},
                    'highlight2': {'value': 'E2E фреймворки', 'label': 'с нуля'},
                    'highlight3': {'value': 'CI/CD', 'label': 'pipeline'}
                })
            )
            db.session.add(about)

        if ResumeSection.query.filter_by(section_type='contacts').count() == 0:
            contacts = ResumeSection(
                section_type='contacts',
                content=json.dumps({
                    'phone': '+7 (995) 590-16-58',
                    'email': 'qa_engineer86@vk.com',
                    'github': 'github.com/qasdet',
                    'location': 'Санкт-Петербург'
                })
            )
            db.session.add(contacts)

        if ResumeSection.query.filter_by(section_type='skills').count() == 0:
            skills = ResumeSection(
                section_type='skills',
                content=json.dumps({
                    'items': ['Python', 'PostgreSQL', 'Docker', 'SQL', 'Pytest', 'Linux', 'Selenium', 'Bash', 'API', 'GraphQL', 'gRPC', 'CI/CD', 'GitLab CI', 'Ansible', 'Git', 'Playwright', 'Appium', 'Allure']
                })
            )
            db.session.add(skills)

        if ResumeSection.query.filter_by(section_type='education').count() == 0:
            education = ResumeSection(
                section_type='education',
                content=json.dumps({
                    'year': '2027',
                    'degree': 'Среднее специальное',
                    'school': 'Московский финансово-промышленный университет «Синергия»',
                    'faculty': 'Информационных технологий и программирования'
                })
            )
            db.session.add(education)

        if ResumeSection.query.filter_by(section_type='certificates').count() == 0:
            certs = ResumeSection(
                section_type='certificates',
                content=json.dumps([
                    {'name': 'Linux: File Management for Devops', 'year': '2021'}
                ])
            )
            db.session.add(certs)

        # Create sample experiences if none exist
        if Experience.query.count() == 0:
            experiences = [
                Experience(
                    company='Банк ВТБ (ПАО)',
                    role='Ведущий инженер по тестированию',
                    period='Июнь 2025 — Октябрь 2025',
                    duration='5 месяцев',
                    description=json.dumps([
                        {'type': 'p', 'content': 'Проектная работа в рамках Т1, переводили в ВТБ на 1/100ую'},
                        {'type': 'ul', 'items': [
                            'Проводил комплексное тестирование критически важного модуля аутентификации в мобильном приложении (100+ млн пользователей)',
                            'Выявил и задокументировал 15+ нетривиальных дефектов на стыке систем, предотвратив потенциальные риски для безопасности',
                            'Разработал методику подготовки тестовых данных, которая сократила время на подготовку к регрессу'
                        ]}
                    ]),
                    sort_order=70
                ),
                Experience(
                    company='Т1',
                    role='Lead QA инженер',
                    period='Июнь 2024 — Октябрь 2025',
                    duration='1 год 5 месяцев',
                    description=json.dumps([
                        {'type': 'ul', 'items': [
                            'Разработал с нуля стратегию и фреймворк автоматизации (Python, Pytest) для продукта-аналога импортозамещения Active Directory, достигнув 70% покрытия критических сценариев за 8 месяцев',
                            'Тестировал протоколы LDAP, Kerberos, NTLM для интеграционного тестирования с разными ОС в гетерогенной среде',
                            'Сократил полный цикл регрессионного тестирования с 3 дней до 4 часов, внедрив параллельный запуск E2E-тестов в CI',
                            'Автоматизировал развертывание тестовых окружений (Ansible, Vagrant), уменьшив время подготовки стенда с 90 до 30 минут'
                        ]}
                    ]),
                    sort_order=60
                ),
                Experience(
                    company='МТС',
                    role='Senior QA инженер',
                    period='Июнь 2022 — Июнь 2024',
                    duration='2 года 1 месяц',
                    description=json.dumps([
                        {'type': 'p', 'content': 'Тестировал проект по рекламным интеграциям медиа-планирования mediapush.mts.ru'},
                        {'type': 'ul', 'items': [
                            'Спроектировал и внедрил E2E-фреймворк (Python, Playwright) с нуля, увеличив тестовое покрытие с 0 до 85% за 9 месяцев',
                            'Настроил CI/CD пайплайн (GitLab CI) для ежедневного запуска 50+ тестовых наборов с отчетностью в Allure',
                            'Разработал инструмент на Python для генерации ORM-моделей из схемы PostgreSQL',
                            'Менторил 3-х Junior QA по паттернам автоматизации (Page Object, Factory)'
                        ]}
                    ]),
                    sort_order=50
                ),
                Experience(
                    company='Проектная работа',
                    role='QA Automation Consultant',
                    period='Август 2020 — Июнь 2022',
                    duration='1 год 11 месяцев',
                    description=json.dumps([
                        {'type': 'p', 'content': 'Special Technology Center (4 мес.): Автоматизировал API-тестирование для сервиса парсинга почты.'},
                        {'type': 'p', 'content': 'Лаборатория Касперского (4 мес.): Автоматизировал регресс для продуктов на macOS и проводил исследовательское тестирование KIS/SAAS.'},
                        {'type': 'p', 'content': 'Лига Цифровой Экономики (4 мес.):'},
                        {'type': 'ul', 'items': [
                            'Запустил релиз мобильного приложения Эльдорадо',
                            'Проводил нагрузочное тестирование для М.Видео/Эльдорадо (JMeter, Gatling, Kubernetes, Docker, Prometheus, Grafana)',
                            'Координировал работу SRE-инженеров по настройке мониторинга'
                        ]}
                    ]),
                    sort_order=40
                ),
                Experience(
                    company='Нмаркет.ПРО',
                    role='Lead QA Automation Engineer',
                    period='Март 2021 — Март 2022',
                    duration='1 год 1 месяц',
                    description=json.dumps([
                        {'type': 'ul', 'items': [
                            'Тестировал портал и мобильные приложения для Android и iOS, доводил фичи до релиза в прод',
                            'Управлял командой тестирования из 9 человек, отвечал за планирование спринтов и полный цикл выпуска',
                            'Предложил бизнесовую идею конструктора сайтов, реализованную на проектах Сайт.Плюс и Каталог.ПРО',
                            'Разработал E2E-тесты для SPA (CodeceptJS/TypeScript, PyTest/Playwright)',
                            'Автоматизация тестирования: Appium + Pytest'
                        ]}
                    ]),
                    sort_order=30
                ),
                Experience(
                    company='Конфидент',
                    role='Специалист по тестированию и сопровождению',
                    period='Июнь 2018 — Февраль 2020',
                    duration='1 год 9 месяцев',
                    description=json.dumps([
                        {'type': 'p', 'content': 'Проекты: Тестирование и внедрение продуктов информационной безопасности (Web Application Firewall, Dallas Lock). Сертификация ФСТЭК и ФСБ.'},
                        {'type': 'ul', 'items': [
                            'Настраивал HyperV, SQL, кластера для тестирования Firewall',
                            'Автоматизировал тестирование UI (Python/Selenium)',
                            'Тестирование в гетерогенной среде: Астра Linux, Рэд ОС, Ubuntu, Unix',
                            'Работа с PKI — Rutoken, NFC ридерами'
                        ]}
                    ]),
                    sort_order=20
                ),
                Experience(
                    company='ООО УК ЖКС',
                    role='Системный администратор (Ведущий)',
                    period='Июнь 2013 — Июль 2017',
                    duration='4 года 2 месяца',
                    description=json.dumps([
                        {'type': 'p', 'content': 'Администрировал гетерогенную IT-инфраструктуру (Windows/Linux) для 50+ пользователей.'}
                    ]),
                    sort_order=10
                )
            ]
            for exp in experiences:
                db.session.add(exp)
            print(f"Created {len(experiences)} sample experiences")

        db.session.commit()
        print("Database initialized successfully!")


if __name__ == '__main__':
    init_database()
