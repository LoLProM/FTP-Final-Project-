import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { FaUpload, FaDownload, FaList, FaTrash, FaBars, FaSignOutAlt, FaInfoCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [files, setFiles] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const isAuthenticated = true; // Aquí se debe implementar la lógica de autenticación
    if (!isAuthenticated) {
      navigate('/');
    }
  }, [navigate]);

  const handleUpload = () => {
    // Lógica para subir archivo
    setFiles([...files, 'newFile.txt']); // Ejemplo de agregar un archivo
  };

  const handleDownload = (fileName) => {
    // Lógica para descargar archivo
    console.log(`Descargando ${fileName}`);
  };

  const handleListFiles = () => {
    // Lógica para listar archivos
    setFiles(['file1.txt', 'file2.txt']); // Ejemplo de listar archivos
  };

  const handleDelete = (fileName) => {
    // Lógica para eliminar archivo
    setFiles(files.filter(file => file !== fileName));
    console.log(`Eliminando ${fileName}`);
  };

  const handleLogout = () => {
    // Lógica para cerrar sesión
    navigate('/');
  };

  const handleAbout = () => {
    navigate('/about');
  };

  return (
    <Container>
      <Header>
        <Title>Cliente FTP</Title>
        <IconButton onClick={() => setMenuOpen(!menuOpen)}><FaBars /></IconButton>
        <Menu open={menuOpen}>
          <MenuItem onClick={handleUpload}><FaUpload /> Subir Archivo</MenuItem>
          <MenuItem onClick={handleListFiles}><FaList /> Listar Archivos</MenuItem>
          <MenuItem onClick={handleLogout}><FaSignOutAlt /> LogOut</MenuItem>
          <MenuItem onClick={handleAbout}><FaInfoCircle /> Acerca De</MenuItem>
        </Menu>
      </Header>
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
  font-family: 'Arial', sans-serif;
`;

const Header = styled.header`
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #007bff;
  padding: 10px 20px;
  color: white;
  position: relative;
`;

const Title = styled.h1`
  margin: 0;
`;

const IconButton = styled.button`
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.5em;

  &:hover {
    color: #0056b3;
  }
`;

const slideDown = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const Menu = styled.div`
  display: ${props => (props.open ? 'block' : 'none')};
  position: absolute;
  top: 60px;
  right: 20px;
  background-color: #007bff;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: ${slideDown} 0.3s ease-out;
  color: white;
`;

const MenuItem = styled.div`
  padding: 10px 20px;
  display: flex;
  align-items: center;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }

  svg {
    margin-right: 10px;
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
