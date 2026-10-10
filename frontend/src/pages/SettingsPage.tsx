import { useEffect, useState, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import Button from '../components/ui/Button';
import { useAuth } from '../auth/AuthContext';
import type {
    InterfaceLanguage,
    UserRegion,
    } from '../types/auth';

const languagesByRegion: Record<
    UserRegion,
    InterfaceLanguage[]
 > = {
     kazakhstan: ['en', 'ru', 'kk'],
     europe: ['en', 'de']
     };

function SettingsPage() {

    const { user, updatePreferences } = useAuth();
    const { t, i18n } = useTranslation();

    const [region, setRegion] = useState<UserRegion>(
        user?.region ?? 'kazakhstan',
        );

    const [language, setLanguage] = useState<InterfaceLanguage>(
        user?.language ?? 'en',
        );

    const [isSaving, setIsSaving] = useState(false);
    const [message, setMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');


    useEffect(() => {

        if (!user) {
            return;
            }

        setRegion(user.region);
        setLanguage(user.language);
        }, [user]);

    function handleRegionChange(nextRegion: UserRegion) {

            setRegion(nextRegion);

            if (!languagesByRegion[nextRegion].includes(language)) {
                    setLanguage('en');
                }

        }

    async function handleSubmit(
        event: FormEvent<HTMLFormElement>,
        ) {
            event.preventDefault();

            setMessage('');
            setErrorMessage('');
            setIsSaving(true);

            try {

                   await updatePreferences({region, language});
                   await i18n.changeLanguage(language);
                   setMessage(t('settings.saved'));

                } catch {
                        setErrorMessage(t('settings.error'));
                    } finally {
                        setIsSaving(false);
                        }
            }

        return (
                <section className='max-w-xl'>
                    <h1 className='text-2xl font-semibold text-slate-950'>
                        {t('settings.title')}
                    </h1>

                    <form
                        className='mt-6 space-y-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'
                        onSubmit={handleSubmit}
                    >
                        <label className='block'>
                            <span className='text-sm font-medium text-slate-700'>
                                {t('settings.region')}
                            </span>

                            <select
                                className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm'
                                value={region}
                                onChange={(event) => handleRegionChange(event.target.value as UserRegion,)}
                            >
                                <option value='kazakhstan'>
                                    {t('region.kazakhstan')}
                                </option>
                                <option value='europe'>
                                    {t('region.europe')}
                                </option>

                            </select>
                        </label>

                        <label className='block'>
                            <span className='text-sm font-medium text-slate-700'>
                                {t('settings.language')}
                            </span>

                            <select
                                className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm'
                                value={language}
                                onChange={(event) => setLanguage(event.target.value as InterfaceLanguage,)}
                            >
                                {languagesByRegion[region].map(
                                    (availableLanguage) => (
                                        <option
                                            key={availableLanguage}
                                            value={availableLanguage}
                                        >
                                            {t(
                                                `language.${availableLanguage}`,
                                                )}
                                        </option>
                                        ),
                                    )}
                            </select>
                        </label>

                        {message && (
                            <p className='rounded-md bg-green-50 px-3 py-2 text-sm text-green-700'>
                                {message}
                            </p>
                        )}

                        {errorMessage && (
                            <p className='rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                                {errorMessage}
                            </p>
                            )}

                        <Button type='submit' disabled={isSaving}>
                            {
                                isSaving ? t('settings.saving') : t('settings.save')
                                }
                        </Button>
                    </form>
                </section>
            );
    }

export default SettingsPage;

