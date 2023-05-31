import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import styled from 'styled-components';
import Container from '../components/Container';
import Button from '../components/Button';
import Input from '../components/Input';

const SearchContainer = styled.div`
  background-color: white;
  box-shadow: var(--base-box-shadow);
  padding: 2.5em 2.5em 2.8em;
  width: 640px;
  transition: height 300ms ease 0s;
`;

const TableContainer = styled.div`
  background-color: white;
  padding: 20px;
  padding: 2.5em 2.5em 2.8em;
`;

const Message = styled.p`
  color: red;
  font-weight: bold;
`;

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    }
  }, []);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${process.env.BACKEND_URL}/lookup/${query}`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setResults(data.results);
      } else {
        setError('Results not found');
        setResults([]);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Container>
      <SearchContainer>
        <Input
          type="text"
          placeholder="Search"
          value={query}
          onChange={handleQueryChange}
        />
        <Button type="submit" onClick={handleSearch}>
          Search
        </Button>
      </SearchContainer>
      <TableContainer>
        {error && <Message>{error}</Message>}
        {results.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Result</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result, index) => (
                <tr key={index}>
                  <td>{result}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </TableContainer>
    </Container>
  );
};

export default Search;
