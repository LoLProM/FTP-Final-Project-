import React, { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { FaUser, FaLock, FaEye, FaEyeSlash } from 'react-icons/fa';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    // Lógica para autenticar al usuario
    if (username === 'testuser' && password === 'testpass') {
      navigate('/home');
    } else {
      alert('Usuario o contraseña incorrectos');
    }
  };

  return (
    <Container>
      <LoginBox>
        <Title>Iniciar Sesión</Title>
        <Form onSubmit={(e) => { e.preventDefault(); handleLogin(); }}>
          <InputWrapper>
            <FaUser />
            <Input
              type="text"
              placeholder="Usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </InputWrapper>
          <InputWrapper>
            <FaLock />
            <Input
              type={showPassword ? 'text' : 'password'}
              placeholder="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <EyeIcon onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </EyeIcon>
          </InputWrapper>
          <Button type="submit">Ingresar</Button>
        </Form>
      </LoginBox>
    </Container>
  );
};

export default Login;

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
`;

const LoginBox = styled.div`
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Title = styled.h1`
  margin-bottom: 20px;
  color: #333;
`;

const Form = styled.form`
  width: 100%;
`;

const InputWrapper = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;

  svg {
    margin-right: 10px;
    color: #007bff;
  }
`;

const Input = styled.input`
  width: 100%;
  border: none;
  outline: none;
  background: none;
  color: #333;
`;

const EyeIcon = styled.div`
  cursor: pointer;
  margin-left: 10px;
  color: #007bff;
`;

const Button = styled.button`
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  margin-top: 20px;
  width: 100%;
  text-align: center;

  &:hover {
    background-color: #0056b3;
  }
`;
