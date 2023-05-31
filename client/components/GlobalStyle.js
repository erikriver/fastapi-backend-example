import styled, { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
    @font-face {
        font-family: BioSans-Regular;
        src: local("BioSans-Regular"),url(/fonts/BioSans-Regular.otf) format("truetype")
    }

    @font-face {
        font-family: BioSans-Bold;
        src: local("BioSans-Bold"),url(/fonts/BioSans-Bold.otf) format("truetype")
    }

    body {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-family: BioSans-Regular,Roboto,Arial,sans-serif;
        margin: 0
    }

    h1,h2,h3 {
        font-family: BioSans-Bold;
        font-weight: 400
    }

    input::-webkit-input-placeholder {
        color: rgba(34,31,32,.5);
        text-align: left
    }

    input::placeholder {
        color: rgba(34,31,32,.5);
        text-align: left
    }

    :root {
        --koffie-primary: #001489;
        --koffie-primary-navy: #001489;
        --koffie-primary-darker: #221f20;
        --koffie-primary-black: #221f20;
        --koffie-primary-hover: rgba(0,71,187,.2);
        --koffie-primary-blue: #0047bb;
        --koffie-yellow: #ffd600;
        --koffie-orange: #ffa100;
        --koffie-light-blue: #bcdef0;
        --koffie-dusty-blue: #8ec1e3;
        --koffie-secondary: #168c7f;
        --koffie-grey: #4e4e4e;
        --koffie-light-blue: #f0fffd;
        --background-grey: #f5f7fa;
        --background-darker-grey: #eceef3;
        --background-lighter-grey: #fcfcfc;
        --base-margin: 1.5em;
        --base-box-shadow: 0 2px 2px -2px rgba(0,0,0,.2)
    }
    .label {
        font-family: BioSans-Bold;
        font-size: 1.05em;
        color: var(--koffie-black);
        margin-right: 10px;
        text-align: left;

        display: flex;
        position: relative;
        width: 100%;
        flex-direction: column;
        box-sizing: border-box;
        text-align: left;
    }

`;

export default GlobalStyle;
