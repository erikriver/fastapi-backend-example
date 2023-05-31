import styled from 'styled-components';

const Button = styled.button`
  font-family: BioSans-Bold;
  display: inline-flex;
  height: 50px;
  width: 160px;
  text-transform: uppercase;
  text-decoration: none;
  font-size: 0.8em;
  letter-spacing: 1.5px;
  -webkit-box-align: center;
  align-items: center;
  -webkit-box-pack: center;
  justify-content: center;
  border: none;
  color: var(--koffie-yellow);
  background-color: var(--koffie-primary-navy);
  opacity: 1;
  cursor: pointer;
  transition: background-color 300ms ease 0s;
`;

export default Button;
