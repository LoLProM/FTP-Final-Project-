import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaUpload, FaDownload, FaList, FaTrash } from 'react-icons/fa';
import { useHistory } from 'react-router-dom';

const Home = () => {
  const [files, setFiles] = useState([]);
  const history = useHistory();

  useEffect(() => {
    // Verificar si el usuario está autenticado
    const isAuthenticated = true; // Aquí se debe implementar la lógica de autenticación
    if (!isAuthenticated) {
      history.push('/');
    }
  }, [history]);

  const handleUpload = () => {
    // Lógica para subir archivo
  };

  const handleDownload = (fileName) => {
    // Lógica para descargar archivo
  };

  const handleListFiles = () => {
    // Lógica para listar archivos
  };

  const handleDelete = (fileName) => {
    // Lógica para eliminar archivo
  };

  return (
    <Container>
      <Header>Cliente FTP</Header>
      <Button onClick={handleUpload}><FaUpload /> Subir Archivo</Button>
      <Button onClick={handleListFiles}><FaList /> Listar Archivos</Button>
      <FileList>
        {files.map((file, index) => (
          <FileItem key={index}>
            {file}
            <IconButton onClick={() => handleDownload(file)}><FaDownload /></IconButton>
            <IconButton onClick={() => handleDelete(file)}><FaTrash /></IconButton>
          </FileItem>
        ))}
      </FileList>
    </Container>
  );
};

export default Home;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100vh;
`;

const Header = styled.h1`
  color: #333;
  margin-bottom: 20px;
`;

const Button = styled.button`
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 10px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;

  &:hover {
    background-color: #0056b3;
  }

  svg {
    margin-right: 5px;
  }
`;

const FileList = styled.ul`
  list-style: none;
  padding: 0;
  width: 100%;
  max-width: 600px;
`;

const FileItem = styled.li`
  background-color: white;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const IconButton = styled.button`
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  margin-left: 10px;

  &:hover {
    color: #0056b3;
  }
`;
