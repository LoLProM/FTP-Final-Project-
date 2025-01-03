import React from 'react';
import styled from 'styled-components';

const About = () => {
  return (
    <Container>
      <Title>Acerca De</Title>
      <Content>
        <p>Esta aplicación es un cliente FTP que permite a los usuarios subir, descargar y listar archivos en un servidor FTP. Fue desarrollada utilizando React y Vite para proporcionar una interfaz de usuario moderna y rápida.</p>
        <p>El proyecto está diseñado para ser fácil de usar y confiable, con un enfoque en la seguridad y la eficiencia. Utiliza tecnologías modernas como styled-components para el diseño y react-icons para los iconos.</p>
        <p>Desarrollado por Richard Alejandro Matos Arderí y Mauricio Sunde Jiménez.</p>
      </Content>
    </Container>
  );
};

export default About;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100vh;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 20px;
`;

const Content = styled.div`
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  text-align: center;
  line-height: 1.6;
`;
