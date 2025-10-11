import React, { useState, useEffect } from 'react';
import './Agendamento.css';
import logoImg from '../../assets/logo-cesmac.svg';
import Campusico from '../../assets/Campus-ico.svg';

interface Agendamento {
  id: number;
  local: string;
  campus: string;
  data: string;
  horario: string;
  pessoas: string;
  status: 'pendente' | 'confirmado' | 'cancelado' | 'realizado';
}

export const Agendamento = (): JSX.Element => {
  const [agendamentos, setAgendamentos] = useState<Agendamento[]>([]);
  const [historico, setHistorico] = useState<Agendamento[]>([]);
  const [mostrarTodosAgendamentos, setMostrarTodosAgendamentos] = useState(false);
  const [mostrarTodoHistorico, setMostrarTodoHistorico] = useState(false);

  // Simular dados - substituir por chamada API real
  useEffect(() => {
    // Dados simulados
    const mockAgendamentos: Agendamento[] = [
      {
        id: 1,
        local: 'Sala Invertida 1',
        campus: 'Campus 1',
        data: '11/08/2025',
        horario: '08:00 às 20:00',
        pessoas: '080',
        status: 'pendente'
      },
      {
        id: 2,
        local: 'Laboratório 1',
        campus: 'Campus 1',
        data: '15/08/2025',
        horario: '10:00 às 11:00',
        pessoas: '020',
        status: 'confirmado'
      },
      // Adicionar mais agendamentos para teste
    ];

    const agendamentosAtivos = mockAgendamentos.filter(
      a => a.status === 'pendente' || a.status === 'confirmado'
    ).sort((a, b) => new Date(a.data).getTime() - new Date(b.data).getTime());

    const historicoAgendamentos = mockAgendamentos.filter(
      a => a.status === 'realizado' || a.status === 'cancelado'
    ).sort((a, b) => new Date(b.data).getTime() - new Date(a.data).getTime());

    setAgendamentos(agendamentosAtivos);
    setHistorico(historicoAgendamentos);
  }, []);

  return (
    <div className="agendamento-container">
      <header className="header">
        <div className="header-bar">
          <img src={logoImg} alt="CESMAC" className="logo" />
        </div>
        <div className="user-bar">
          <span>Bem-vindo!</span>
          <span className="username">Gabriela Saraiva</span>
          <button className="add-button">+</button>
        </div>
      </header>

      <main className="main-content">
        <section className="proximos-agendamentos">
          <h2>Meus agendamentos</h2>
          <div className="agendamentos-list">
            {agendamentos
              .slice(0, mostrarTodosAgendamentos ? undefined : 2)
              .map(agendamento => (
                <div key={agendamento.id} className="agendamento-card">
                  <div className="card-content">
                    <div className="card-left">
                      <div className="building-icon">
                        <img src={Campusico} alt="Campus" className="campus-icon" />
                        <span className="campus-name">{agendamento.campus}</span>
                      </div>
                    </div>
                    <div className="card-right">
                      <div className="header-buttons">
                        <button className="edit-button">Editar</button>
                        <button className="cancel-button-small">Cancelar</button>
                      </div>
                      <div className="local-details">
                        <h3>{agendamento.local}</h3>
                      </div>
                      <div className="agendamento-info">
                        <p>{agendamento.data}</p>
                        <p>{agendamento.horario}</p>
                        <p>{agendamento.pessoas}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
          </div>
          {agendamentos.length > 2 && (
            <button
              className="ver-mais"
              onClick={() => setMostrarTodosAgendamentos(!mostrarTodosAgendamentos)}
            >
              {mostrarTodosAgendamentos ? 'Ver menos' : 'Ver mais'}
            </button>
          )}
        </section>

        <section className="historico">
          <h2>Histórico de agendamento</h2>
          <div className="historico-list">
            {historico
              .slice(0, mostrarTodoHistorico ? undefined : 2)
              .map(agendamento => (
                <div key={agendamento.id} className="historico-card">
                  <div className="local-info">
                    <i className="building-icon" />
                    <div>
                      <h3>{agendamento.local}</h3>
                      <p>{agendamento.campus}</p>
                    </div>
                  </div>
                  <div className="agendamento-info">
                    <p>Data: {agendamento.data}</p>
                    <p>Horário: {agendamento.horario}</p>
                    <span className={`status ${agendamento.status}`}>
                      {agendamento.status}
                    </span>
                  </div>
                </div>
              ))}
          </div>
          {historico.length > 2 && (
            <button
              className="ver-mais"
              onClick={() => setMostrarTodoHistorico(!mostrarTodoHistorico)}
            >
              {mostrarTodoHistorico ? 'Ver menos' : 'Ver mais'}
            </button>
          )}
        </section>

        <section className="novo-agendamento">
          <h2>Novo Agendamento</h2>
          <div className="filtro">
            <select defaultValue="">
              <option value="" disabled>Buscar Sala específica</option>
              <option value="sala1">Sala 1</option>
              <option value="sala2">Sala 2</option>
            </select>
            <button className="search-button">→</button>
          </div>
        </section>
      </main>
    </div>
  );
};