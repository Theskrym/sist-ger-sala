import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import logoCesmac from "../../assets/logo-CESMAC.svg";
import iconePerfil from "../../assets/Icones-Perfil.svg";
import iconeCadeado from "../../assets/ICONE CADEADO.svg";
import campus1 from "../../assets/Campus1.svg";
import "./Login.css";

export const Login = (): JSX.Element => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!username.trim() || !password) {
      setError("Por favor, preencha todos os campos");
      return;
    }

    setLoading(true);
    setError("");
    const fullEmail = `${username}@cesmac.edu.br`;

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: fullEmail,
          password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.token);
        // Optional: Store user data if needed
        localStorage.setItem('user', JSON.stringify(data.user));
        navigate('/agendamento');
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Usuário ou senha incorretos");
      }
    } catch (err) {
      setError("Falha ao tentar acessar. Verifique sua conexão.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login">
      <div className="rectangle-base">
        {/* Logo only shows here in desktop mode */}
        <img className="logo-CESMAC-desktop" alt="Logo CESMAC" src={logoCesmac} />
      </div>
      <div className="content-container">
        {/* Logo shows here only in mobile mode */}
        <img className="logo-CESMAC-mobile" alt="Logo CESMAC" src={logoCesmac} />
        <div className="portal-title">Portal de Agendamentos</div>
        <div className="welcome-text">Boas-Vindas!</div>

        <form className="login-form" onSubmit={handleLogin}>
          <div className="input-container">
            <img src={iconePerfil} alt="" className="input-icon" />
            <input
              type="text"
              className="login-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Insira seu usuário"
              disabled={loading}
            />
          </div>
          
          <div className="input-container">
            <img src={iconeCadeado} alt="" className="input-icon" />
            <input
              type="password"
              className="login-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Insira sua senha"
              disabled={loading}
            />
          </div>

          <div className={`error-message ${error ? 'visible' : ''}`}>
            {error}
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>
      <img className="image" alt="Campus CESMAC" src={campus1} />
    </div>
  );
};