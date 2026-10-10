import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
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
        },
    },
    ru: {
        translation: {
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
        },
    },
    kk: {
        translation: {
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
        },
    },
    de: {
        translation: {
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

