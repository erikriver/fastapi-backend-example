import { useState } from 'react';
import { useRouter } from 'next/router';
import styled from 'styled-components';
import Container from '../components/Container';
import GlobalStyle from '../components/GlobalStyle';
import Button from '../components/Button';
import Input from '../components/Input';

const FormContainer = styled.div`
  background-color: white;
  box-shadow: var(--base-box-shadow);
  padding: 2.5em 2.5em 2.8em;
  width: 380px;
  transition: height 300ms ease 0s;
`;

const Login = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleFormSubmit = async (e) => {
    //e.preventDefault();

    // Check if the email and password match the local values
    if (email === 'user@demo.com' && password === 'password') {
      try {
        // Make a POST request to generate a JWT token
        const response = await fetch(
          `${process.env.BACKEND_URL}/generate-token`,
          {
            method: 'POST',
          }
        );

        if (response.ok) {
          const { token } = await response.json();

          // Save the token in localStorage
          localStorage.setItem('token', token);

          // Redirect to the Home view with the token in the header
          router.push('/search');
        } else {
          console.log('Failed to generate token');
        }
      } catch (error) {
        console.log(error);
      }
    } else {
      console.log('Invalid email or password');
    }
  };

  return (
    <>
      <GlobalStyle />
      <Container>
        <FormContainer>
          <form onSubmit={handleFormSubmit}>
            <label className="label">Email</label>
            <Input
              type="email"
              placeholder="user@demo.com"
              value={email}
              onChange={handleEmailChange}
            />
            <label className="label">Password</label>
            <Input
              type="password"
              placeholder="password"
              value={password}
              onChange={handlePasswordChange}
            />
            <Button type="submit">Login</Button>
          </form>
        </FormContainer>
      </Container>
    </>
  );
};

export default Login;
