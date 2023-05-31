import { useEffect } from 'react';
import { useRouter } from 'next/router';

const Index = () => {
  const router = useRouter();
  const token = null;

  useEffect(() => {
    // Perform localStorage action
    const token = localStorage.getItem('token');
  }, []);

  useEffect(() => {
    // Check if the user is authenticated
    if (token) {
      router.push('/search');
    } else {
      router.push('/login');
    }
  }, [router, token]);

  return null; // No content to render on this page
};

export default { Index, GlobalStyle };
