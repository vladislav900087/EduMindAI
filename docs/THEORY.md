
1. **API:** An API is a set of rules that lets programs talk to each other. In EduMindAI, the React frontend asks the FastAPI backend for data, and the backend returns an answer.
2. **REST API:** REST is a common way to organize an API around resources, such as users, courses, and quizzes. For example, `GET /courses` asks for courses, while `POST /courses` creates one.
3. **Endpoint:** An endpoint is one specific API address and action. `POST /auth/login` is an endpoint that accepts credentials and returns an access token.
4. **Server:** A server is a computer hardware system or software program that processes requests and delivers data, resources, services, or applications to other devices (called clients) over a network or the internet.
5. **Client:** A device, program, or browser that asks for a service, data, or resource.
6. **HTTP (Hypertext Transfer Protocol):** HTTP is the set of rules that web browsers (clients) and web servers use to talk to each other.
7. **HTTPS (Hypertext Transfer Protocol Secure):** HTTPS is the safe, encrypted version of regular HTTP.
8. **JSON (JavaScript Object Notation):** JSON is a lightweight, text-based data format used to store and exchange information between a server and a web application.
9. **JWT:** A JWT is a signed digital pass proving that a user has logged in. The frontend sends it with protected requests, and the backend checks it before allowing access.
10. **Repository:** A repository is the part of the code that reads and writes database data. It keeps SQLAlchemy queries out of the rest of the application.
11. **Service:** A service contains business rules. For example, the purchase service checks balance, creates ledger transactions, enrolls the student, and prevents duplicate purchases.
12. **Celery:** Celery runs slow work outside the web request, so the user does not wait while the browser is frozen. EduMindAI uses it for emails and notifications.
13. **Celery Beat:** Celery Beat is a scheduler for repeated background jobs. In this project, it periodically checks upcoming assignment deadlines.
14. **Docker:** Docker packages an application with its dependencies into a container. This makes the project run similarly on macOS, a Linux server, or another developer's computer.
15. **Docker Compose:** Docker compose starts several containers as one system. Here it starts PostgreSQL, Redis, FastAPI, Celery worker, Celery Beat, and Nginx frontend together.
16. **Deployment:** Deployment means preparing and running the application outside the development environment. The project is deployed locally through Docker Compose and can be demonstrated publicly through Cloudflare Tunnel.
17. **Redis:** Redis (Remote Dictionary Server) is a super-fast data storage tool that keeps information directly in one's computer's short-term memory, instead of saving it on a slow hard drive.
18. **FastAPI:** FastAPI is a modern, high-performance Python web framework used to build APIs quickly and easily.