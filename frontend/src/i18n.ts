import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            brand: {
                portal: 'Learning Portal',
            },
            role: {
                student: 'Student',
                teacher: 'Teacher',
                admin: 'Administrator',
            },
            auth: {
                signIn: 'Sign in',
                signingIn: 'Signing in...',
                createAccount: 'Create account',
                creatingAccount: 'Creating account...',
                email: 'Email',
                password: 'Password',
                fullName: 'Full name',
                loginDescription:
                    'Access your courses, lessons, quizzes, and assignments.',
                registerDescription:
                    'Join EduMindAI as a student or teacher.',
                noAccount: 'Do not have an account?',
                haveAccount: 'Already have an account?',
                createOne: 'Create one',
                invalidCredentials: 'Invalid email or password.',
                registerError: 'Could not create account. Try another email.',
            },
            nav: {
                dashboard: 'Dashboard',
                courses: 'Courses',
                assignments: 'Assignments',
                quizHistory: 'Quiz history',
                settings: 'Settings',
                logout: 'Log out',
            },
            settings: {
                title: 'Preferences',
                region: 'Region',
                language: 'Interface language',
                save: 'Save preferences',
                saving: 'Saving...',
                saved: 'Preferences saved.',
                error: 'Could not save preferences.',
            },
            region: {
                kazakhstan: 'Kazakhstan',
                europe: 'Europe',
            },
            language: {
                en: 'English',
                ru: 'Russian',
                kk: 'Kazakh',
                de: 'German',
            },
            common: { loading: 'Loading...', backToCourse: 'Back to course', noDescription: 'No description provided.', open: 'Open', publish: 'Publish', error: 'Something went wrong.' },
            dashboard: {
                overview: 'Overview', welcome: 'Welcome, {{name}}', studentDescription: 'Track your learning and recent results.',
                teacherDescription: 'Manage your courses and student work.', loadError: 'Could not load dashboard information.',
                enrolledCourses: 'Enrolled courses', submittedAssignments: 'Submitted assignments', gradedAssignments: 'Graded assignments',
                averageQuizScore: 'Average quiz score', continueLearning: 'Continue learning', viewAssignments: 'View assignments',
                myCourses: 'My courses', assignments: 'Assignments', awaitingGrading: 'Awaiting grading', manageCourses: 'Manage courses', reviewAssignments: 'Review assignments',
            },
            courses: { title: 'Courses', catalog: 'Course catalog', description: 'Explore available courses and continue learning.', loadError: 'Could not load courses.', loading: 'Loading courses...', mine: 'My courses', noneMine: 'You have not created any courses yet.', all: 'All courses', none: 'No courses yet', publishedHere: 'Published courses will appear here.', openCourse: 'Open course' },
            learning: { backToCourses: 'Back to courses', courseNotFound: 'Course not found.', lessonNotFound: 'Lesson not found.', courseIdMissing: 'Course id is missing.', lessonIdMissing: 'Lesson id is missing.', invalidLessonId: 'Invalid lesson id.', loadCourse: 'Loading course...', loadLesson: 'Loading lesson...', loadCourseError: 'Could not load course content.', loadLessonError: 'Could not load lesson.', progress: 'Progress', lessons: 'lessons', enroll: 'Enroll in course', enrollError: 'Could not enroll in this course.', completed: 'Completed', complete: 'Complete', completeLesson: 'Complete lesson', completing: 'Completing...', completeError: 'Could not mark this lesson complete.', deleteLesson: 'Delete lesson', deleting: 'Deleting...', deleteLessonError: 'Could not delete this lesson.', noContent: 'No content provided.', due: 'Due', lessonsTitle: 'Lessons', quizzes: 'Quizzes', assignments: 'Assignments', noLessons: 'No lessons yet.', noQuizzes: 'No quizzes yet.', noAssignments: 'No assignments yet.', addLesson: 'Add lesson', addQuiz: 'Add quiz', addAssignment: 'Add assignment', lessonTitle: 'Lesson title', lessonContent: 'Lesson content', quizTitle: 'Quiz title', quizDescription: 'Quiz description', assignmentTitle: 'Assignment title', assignmentDescription: 'Assignment description', createLesson: 'Create lesson', createQuiz: 'Create quiz', createAssignment: 'Create assignment', createLessonError: 'Could not create lesson.', createQuizError: 'Could not create quiz.', createAssignmentError: 'Could not create assignment.' },
            work: { assignment: 'Assignment', loadAssignments: 'Loading assignments...', loadAssignment: 'Loading assignment...', noDeadline: 'No deadline', submission: 'Your submission', submissions: 'Submissions', noSubmissions: 'No submissions yet.', submit: 'Submit assignment', update: 'Update submission', saving: 'Saving...', grade: 'Grade', feedback: 'Feedback', noFeedback: 'No feedback provided.', quizHistory: 'Quiz history', loadHistory: 'Loading quiz history...', noHistory: 'No completed quizzes yet.', completed: 'Completed', quizManagement: 'Quiz management', questions: 'Questions', addQuestion: 'Add question', loadingQuestions: 'Loading questions...', noQuestions: 'No questions added yet.', correct: 'Correct', question: 'Question', option: 'Option', adding: 'Adding...', createCourse: 'Create course', creating: 'Creating...', title: 'Title', description: 'Description' },
        },
    },
    ru: {
        translation: {
            brand: {
                portal: 'Учебный портал',
            },
            role: {
                student: 'Студент',
                teacher: 'Преподаватель',
                admin: 'Администратор',
            },
            auth: {
                signIn: 'Войти',
                signingIn: 'Вход...',
                createAccount: 'Создать аккаунт',
                creatingAccount: 'Создание аккаунта...',
                email: 'Электронная почта',
                password: 'Пароль',
                fullName: 'Полное имя',
                loginDescription:
                    'Получите доступ к вашим курсам, урокам, тестам и заданиям.',
                registerDescription:
                    'Присоединяйтесь к EduMindAI в качестве студента или преподавателя.',
                noAccount: 'Нет аккаунта?',
                haveAccount: 'Уже есть аккаунт?',
                createOne: 'Создать',
                invalidCredentials: 'Неверный email или пароль.',
                registerError: 'Не удалось создать аккаунт. Попробуйте другой email.',
            },
            nav: {
                dashboard: 'Главная',
                courses: 'Курсы',
                assignments: 'Задания',
                quizHistory: 'История тестов',
                settings: 'Настройки',
                logout: 'Выйти',
            },
            settings: {
                title: 'Настройки',
                region: 'Регион',
                language: 'Язык интерфейса',
                save: 'Сохранить настройки',
                saving: 'Сохранение...',
                saved: 'Настройки сохранены.',
                error: 'Не удалось сохранить настройки.',
            },
            region: {
                kazakhstan: 'Казахстан',
                europe: 'Европа',
            },
            language: {
                en: 'Английский',
                ru: 'Русский',
                kk: 'Казахский',
                de: 'Немецкий',
            },
            common: { loading: 'Загрузка...', backToCourse: 'Назад к курсу', noDescription: 'Описание не указано.', open: 'Открыть', publish: 'Опубликовать', error: 'Что-то пошло не так.' },
            dashboard: { overview: 'Обзор', welcome: 'Добро пожаловать, {{name}}', studentDescription: 'Отслеживайте обучение и последние результаты.', teacherDescription: 'Управляйте курсами и работами студентов.', loadError: 'Не удалось загрузить информацию панели.', enrolledCourses: 'Записанные курсы', submittedAssignments: 'Отправленные задания', gradedAssignments: 'Оценённые задания', averageQuizScore: 'Средний результат тестов', continueLearning: 'Продолжить обучение', viewAssignments: 'Посмотреть задания', myCourses: 'Мои курсы', assignments: 'Задания', awaitingGrading: 'Ожидают оценки', manageCourses: 'Управлять курсами', reviewAssignments: 'Проверить задания' },
            courses: { title: 'Курсы', catalog: 'Каталог курсов', description: 'Изучайте доступные курсы и продолжайте обучение.', loadError: 'Не удалось загрузить курсы.', loading: 'Загрузка курсов...', mine: 'Мои курсы', noneMine: 'Вы ещё не создали курсы.', all: 'Все курсы', none: 'Курсов пока нет', publishedHere: 'Опубликованные курсы появятся здесь.', openCourse: 'Открыть курс' },
            learning: { backToCourses: 'Назад к курсам', courseNotFound: 'Курс не найден.', lessonNotFound: 'Урок не найден.', courseIdMissing: 'Идентификатор курса отсутствует.', lessonIdMissing: 'Идентификатор урока отсутствует.', invalidLessonId: 'Некорректный идентификатор урока.', loadCourse: 'Загрузка курса...', loadLesson: 'Загрузка урока...', loadCourseError: 'Не удалось загрузить содержимое курса.', loadLessonError: 'Не удалось загрузить урок.', progress: 'Прогресс', lessons: 'уроков', enroll: 'Записаться на курс', enrollError: 'Не удалось записаться на этот курс.', completed: 'Завершено', complete: 'Завершить', completeLesson: 'Завершить урок', completing: 'Завершение...', completeError: 'Не удалось отметить урок как завершённый.', deleteLesson: 'Удалить урок', deleting: 'Удаление...', deleteLessonError: 'Не удалось удалить этот урок.', noContent: 'Содержимое не указано.', due: 'Срок сдачи', lessonsTitle: 'Уроки', quizzes: 'Тесты', assignments: 'Задания', noLessons: 'Уроков пока нет.', noQuizzes: 'Тестов пока нет.', noAssignments: 'Заданий пока нет.', addLesson: 'Добавить урок', addQuiz: 'Добавить тест', addAssignment: 'Добавить задание', lessonTitle: 'Название урока', lessonContent: 'Содержание урока', quizTitle: 'Название теста', quizDescription: 'Описание теста', assignmentTitle: 'Название задания', assignmentDescription: 'Описание задания', createLesson: 'Создать урок', createQuiz: 'Создать тест', createAssignment: 'Создать задание', createLessonError: 'Не удалось создать урок.', createQuizError: 'Не удалось создать тест.', createAssignmentError: 'Не удалось создать задание.' },
            work: { assignment: 'Задание', loadAssignments: 'Загрузка заданий...', loadAssignment: 'Загрузка задания...', noDeadline: 'Без срока сдачи', submission: 'Ваша работа', submissions: 'Работы', noSubmissions: 'Работ пока нет.', submit: 'Сдать задание', update: 'Обновить работу', saving: 'Сохранение...', grade: 'Оценка', feedback: 'Комментарий', noFeedback: 'Комментарий не указан.', quizHistory: 'История тестов', loadHistory: 'Загрузка истории тестов...', noHistory: 'Завершённых тестов пока нет.', completed: 'Завершено', quizManagement: 'Управление тестом', questions: 'Вопросы', addQuestion: 'Добавить вопрос', loadingQuestions: 'Загрузка вопросов...', noQuestions: 'Вопросов пока нет.', correct: 'Верно', question: 'Вопрос', option: 'Вариант', adding: 'Добавление...', createCourse: 'Создать курс', creating: 'Создание...', title: 'Название', description: 'Описание' },
        },
    },
    kk: {
        translation: {
            brand: {
                portal: 'Оқу порталы',
            },
            role: {
                student: 'Студент',
                teacher: 'Оқытушы',
                admin: 'Әкімші',
            },
            auth: {
                signIn: 'Кіру',
                signingIn: 'Кіруде...',
                createAccount: 'Тіркелу',
                creatingAccount: 'Тіркелуде...',
                email: 'Электрондық пошта',
                password: 'Құпия сөз',
                fullName: 'Толық аты-жөні',
                loginDescription:
                    'Курстарыңызға, сабақтарыңызға, тестілеріңіз бен тапсырмаларыңызға кіріңіз.',
                registerDescription:
                    'EduMindAI жүйесіне студент немесе оқытушы ретінде қосылыңыз.',
                noAccount: 'Тіркелмегенсіз бе?',
                haveAccount: 'Тіркелгенсіз бе?',
                createOne: 'Тіркелу',
                invalidCredentials: 'Электрондық пошта немесе құпия сөз қате.',
                registerError: 'Тіркелу мүмкін болмады. Басқа электрондық поштаны байқап көрiңiз.',
            },
            nav: {
                dashboard: 'Басты бет',
                courses: 'Курстар',
                assignments: 'Тапсырмалар',
                quizHistory: 'Тест тарихы',
                settings: 'Баптаулар',
                logout: 'Шығу',
            },
            settings: {
                title: 'Баптаулар',
                region: 'Аймақ',
                language: 'Интерфейс тілі',
                save: 'Баптауларды сақтау',
                saving: 'Сақталуда...',
                saved: 'Баптаулар сақталды.',
                error: 'Баптауларды сақтау мүмкін болмады.',
            },
            region: {
                kazakhstan: 'Қазақстан',
                europe: 'Еуропа',
            },
            language: {
                en: 'Ағылшын тілі',
                ru: 'Орыс тілі',
                kk: 'Қазақ тілі',
                de: 'Неміс тілі',
            },
            common: { loading: 'Жүктелуде...', backToCourse: 'Курсқа оралу', noDescription: 'Сипаттама берілмеген.', open: 'Ашу', publish: 'Жариялау', error: 'Бірдеңе дұрыс болмады.' },
            dashboard: { overview: 'Шолу', welcome: 'Қош келдіңіз, {{name}}', studentDescription: 'Оқуыңыз бен соңғы нәтижелеріңізді бақылаңыз.', teacherDescription: 'Курстарыңыз бен студенттердің жұмыстарын басқарыңыз.', loadError: 'Басқару тақтасының деректерін жүктеу мүмкін болмады.', enrolledCourses: 'Жазылған курстар', submittedAssignments: 'Жіберілген тапсырмалар', gradedAssignments: 'Бағаланған тапсырмалар', averageQuizScore: 'Тесттердің орташа нәтижесі', continueLearning: 'Оқуды жалғастыру', viewAssignments: 'Тапсырмаларды қарау', myCourses: 'Менің курстарым', assignments: 'Тапсырмалар', awaitingGrading: 'Бағалауды күтуде', manageCourses: 'Курстарды басқару', reviewAssignments: 'Тапсырмаларды тексеру' },
            courses: { title: 'Курстар', catalog: 'Курс каталогы', description: 'Қолжетімді курстарды зерттеп, оқуды жалғастырыңыз.', loadError: 'Курстарды жүктеу мүмкін болмады.', loading: 'Курстар жүктелуде...', mine: 'Менің курстарым', noneMine: 'Сіз әлі курс құрмадыңыз.', all: 'Барлық курстар', none: 'Әзірге курс жоқ', publishedHere: 'Жарияланған курстар осында көрсетіледі.', openCourse: 'Курсты ашу' },
            learning: { backToCourses: 'Курстарға оралу', courseNotFound: 'Курс табылмады.', lessonNotFound: 'Сабақ табылмады.', courseIdMissing: 'Курс идентификаторы жоқ.', lessonIdMissing: 'Сабақ идентификаторы жоқ.', invalidLessonId: 'Сабақ идентификаторы қате.', loadCourse: 'Курс жүктелуде...', loadLesson: 'Сабақ жүктелуде...', loadCourseError: 'Курс мазмұнын жүктеу мүмкін болмады.', loadLessonError: 'Сабақты жүктеу мүмкін болмады.', progress: 'Үлгерім', lessons: 'сабақ', enroll: 'Курсқа жазылу', enrollError: 'Бұл курсқа жазылу мүмкін болмады.', completed: 'Аяқталды', complete: 'Аяқтау', completeLesson: 'Сабақты аяқтау', completing: 'Аяқталуда...', completeError: 'Сабақты аяқталды деп белгілеу мүмкін болмады.', deleteLesson: 'Сабақты жою', deleting: 'Жойылуда...', deleteLessonError: 'Бұл сабақты жою мүмкін болмады.', noContent: 'Мазмұн берілмеген.', due: 'Мерзімі', lessonsTitle: 'Сабақтар', quizzes: 'Тестілер', assignments: 'Тапсырмалар', noLessons: 'Әзірге сабақ жоқ.', noQuizzes: 'Әзірге тест жоқ.', noAssignments: 'Әзірге тапсырма жоқ.', addLesson: 'Сабақ қосу', addQuiz: 'Тест қосу', addAssignment: 'Тапсырма қосу', lessonTitle: 'Сабақ атауы', lessonContent: 'Сабақ мазмұны', quizTitle: 'Тест атауы', quizDescription: 'Тест сипаттамасы', assignmentTitle: 'Тапсырма атауы', assignmentDescription: 'Тапсырма сипаттамасы', createLesson: 'Сабақ құру', createQuiz: 'Тест құру', createAssignment: 'Тапсырма құру', createLessonError: 'Сабақты құру мүмкін болмады.', createQuizError: 'Тестті құру мүмкін болмады.', createAssignmentError: 'Тапсырманы құру мүмкін болмады.' },
            work: { assignment: 'Тапсырма', loadAssignments: 'Тапсырмалар жүктелуде...', loadAssignment: 'Тапсырма жүктелуде...', noDeadline: 'Мерзімі жоқ', submission: 'Сіздің жұмысыңыз', submissions: 'Жұмыстар', noSubmissions: 'Әзірге жұмыс жоқ.', submit: 'Тапсырманы жіберу', update: 'Жұмысты жаңарту', saving: 'Сақталуда...', grade: 'Баға', feedback: 'Пікір', noFeedback: 'Пікір берілмеген.', quizHistory: 'Тест тарихы', loadHistory: 'Тест тарихы жүктелуде...', noHistory: 'Аяқталған тест әлі жоқ.', completed: 'Аяқталды', quizManagement: 'Тестті басқару', questions: 'Сұрақтар', addQuestion: 'Сұрақ қосу', loadingQuestions: 'Сұрақтар жүктелуде...', noQuestions: 'Әзірге сұрақ жоқ.', correct: 'Дұрыс', question: 'Сұрақ', option: 'Нұсқа', adding: 'Қосылуда...', createCourse: 'Курс құру', creating: 'Құрылуда...', title: 'Атауы', description: 'Сипаттама' },
        },
    },
    de: {
        translation: {
            brand: {
                portal: 'Lernportal',
            },
            role: {
                student: 'Student',
                teacher: 'Lehrkraft',
                admin: 'Administrator',
            },
            auth: {
                signIn: 'Anmelden',
                signingIn: 'Anmeldung...',
                createAccount: 'Konto erstellen',
                creatingAccount: 'Konto wird erstellt...',
                email: 'E-Mail',
                password: 'Passwort',
                fullName: 'Vollständiger Name',
                loginDescription:
                    'Greifen Sie auf Ihre Kurse, Lektionen, Quizzes und Aufgaben zu.',
                registerDescription:
                    'Treten Sie EduMindAI als Student oder Lehrkraft bei.',
                noAccount: 'Noch kein Konto?',
                haveAccount: 'Bereits ein Konto?',
                createOne: 'Konto erstellen',
                invalidCredentials: 'Ungültige E-Mail-Adresse oder Passwort.',
                registerError: 'Konto konnte nicht erstellt werden. Versuchen Sie eine andere E-Mail.',
            },
            nav: {
                dashboard: 'Übersicht',
                courses: 'Kurse',
                assignments: 'Aufgaben',
                quizHistory: 'Quizverlauf',
                settings: 'Einstellungen',
                logout: 'Abmelden',
            },
            settings: {
                title: 'Einstellungen',
                region: 'Region',
                language: 'Sprache der Oberfläche',
                save: 'Einstellungen speichern',
                saving: 'Wird gespeichert...',
                saved: 'Einstellungen gespeichert.',
                error: 'Einstellungen konnten nicht gespeichert werden.',
            },
            region: {
                kazakhstan: 'Kasachstan',
                europe: 'Europa',
            },
            language: {
                en: 'Englisch',
                ru: 'Russisch',
                kk: 'Kasachisch',
                de: 'Deutsch',
            },
            common: { loading: 'Wird geladen...', backToCourse: 'Zurück zum Kurs', noDescription: 'Keine Beschreibung vorhanden.', open: 'Öffnen', publish: 'Veröffentlichen', error: 'Etwas ist schiefgelaufen.' },
            dashboard: { overview: 'Übersicht', welcome: 'Willkommen, {{name}}', studentDescription: 'Verfolgen Sie Ihren Lernfortschritt und Ihre Ergebnisse.', teacherDescription: 'Verwalten Sie Ihre Kurse und studentischen Arbeiten.', loadError: 'Dashboard-Informationen konnten nicht geladen werden.', enrolledCourses: 'Belegte Kurse', submittedAssignments: 'Eingereichte Aufgaben', gradedAssignments: 'Bewertete Aufgaben', averageQuizScore: 'Durchschnittliches Quiz-Ergebnis', continueLearning: 'Weiterlernen', viewAssignments: 'Aufgaben ansehen', myCourses: 'Meine Kurse', assignments: 'Aufgaben', awaitingGrading: 'Warten auf Bewertung', manageCourses: 'Kurse verwalten', reviewAssignments: 'Aufgaben prüfen' },
            courses: { title: 'Kurse', catalog: 'Kurskatalog', description: 'Entdecken Sie verfügbare Kurse und lernen Sie weiter.', loadError: 'Kurse konnten nicht geladen werden.', loading: 'Kurse werden geladen...', mine: 'Meine Kurse', noneMine: 'Sie haben noch keine Kurse erstellt.', all: 'Alle Kurse', none: 'Noch keine Kurse', publishedHere: 'Veröffentlichte Kurse erscheinen hier.', openCourse: 'Kurs öffnen' },
            learning: { backToCourses: 'Zurück zu den Kursen', courseNotFound: 'Kurs nicht gefunden.', lessonNotFound: 'Lektion nicht gefunden.', courseIdMissing: 'Kurs-ID fehlt.', lessonIdMissing: 'Lektions-ID fehlt.', invalidLessonId: 'Ungültige Lektions-ID.', loadCourse: 'Kurs wird geladen...', loadLesson: 'Lektion wird geladen...', loadCourseError: 'Kursinhalt konnte nicht geladen werden.', loadLessonError: 'Lektion konnte nicht geladen werden.', progress: 'Fortschritt', lessons: 'Lektionen', enroll: 'Für Kurs anmelden', enrollError: 'Für diesen Kurs konnte keine Anmeldung erfolgen.', completed: 'Abgeschlossen', complete: 'Abschließen', completeLesson: 'Lektion abschließen', completing: 'Wird abgeschlossen...', completeError: 'Lektion konnte nicht als abgeschlossen markiert werden.', deleteLesson: 'Lektion löschen', deleting: 'Wird gelöscht...', deleteLessonError: 'Diese Lektion konnte nicht gelöscht werden.', noContent: 'Kein Inhalt vorhanden.', due: 'Fällig', lessonsTitle: 'Lektionen', quizzes: 'Quizzes', assignments: 'Aufgaben', noLessons: 'Noch keine Lektionen.', noQuizzes: 'Noch keine Quizzes.', noAssignments: 'Noch keine Aufgaben.', addLesson: 'Lektion hinzufügen', addQuiz: 'Quiz hinzufügen', addAssignment: 'Aufgabe hinzufügen', lessonTitle: 'Lektionstitel', lessonContent: 'Lektionsinhalt', quizTitle: 'Quiztitel', quizDescription: 'Quizbeschreibung', assignmentTitle: 'Aufgabentitel', assignmentDescription: 'Aufgabenbeschreibung', createLesson: 'Lektion erstellen', createQuiz: 'Quiz erstellen', createAssignment: 'Aufgabe erstellen', createLessonError: 'Lektion konnte nicht erstellt werden.', createQuizError: 'Quiz konnte nicht erstellt werden.', createAssignmentError: 'Aufgabe konnte nicht erstellt werden.' },
            work: { assignment: 'Aufgabe', loadAssignments: 'Aufgaben werden geladen...', loadAssignment: 'Aufgabe wird geladen...', noDeadline: 'Keine Frist', submission: 'Ihre Einreichung', submissions: 'Einreichungen', noSubmissions: 'Noch keine Einreichungen.', submit: 'Aufgabe einreichen', update: 'Einreichung aktualisieren', saving: 'Wird gespeichert...', grade: 'Bewertung', feedback: 'Feedback', noFeedback: 'Kein Feedback vorhanden.', quizHistory: 'Quizverlauf', loadHistory: 'Quizverlauf wird geladen...', noHistory: 'Noch keine abgeschlossenen Quizzes.', completed: 'Abgeschlossen', quizManagement: 'Quizverwaltung', questions: 'Fragen', addQuestion: 'Frage hinzufügen', loadingQuestions: 'Fragen werden geladen...', noQuestions: 'Noch keine Fragen.', correct: 'Richtig', question: 'Frage', option: 'Option', adding: 'Wird hinzugefügt...', createCourse: 'Kurs erstellen', creating: 'Wird erstellt...', title: 'Titel', description: 'Beschreibung' },
        },
    },
};

i18n.use(initReactI18next).init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
        escapeValue: false,
    },
});

export default i18n;
