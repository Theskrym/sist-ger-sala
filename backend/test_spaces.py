import requests
import json

BASE_URL = "http://localhost:8000/api"
AUTH_URL = "http://localhost:8000/api/auth"

# Substitua com suas credenciais
EMAIL = "enzo.machado@cesmac.edu.br"
PASSWORD = "hgpvp123"

def get_auth_token():
    """Obtém token JWT"""
    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(f"{AUTH_URL}/login/", json=login_data)
        if response.status_code == 200:
            print("✅ Login realizado com sucesso!")
            return response.json()['access']
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(response.json())
            return None
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def test_endpoint(url, headers, name):
    """Testa um endpoint específico"""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"✅ {name}: SUCCESSO")
            data = response.json()
            print(f"   Resultados: {len(data)} itens")
            for item in data[:3]:  # Mostra apenas os primeiros 3
                print(f"   - {item.get('name', item.get('title', 'Sem nome'))}")
            if len(data) > 3:
                print(f"   ... e mais {len(data) - 3} itens")
        else:
            print(f"❌ {name}: ERRO {response.status_code}")
            print(f"   Mensagem: {response.json()}")
    except Exception as e:
        print(f"❌ {name}: Erro de conexão - {e}")

def main():
    print("🔐 Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🚀 Testando endpoints da API...")
    
    # Testar cada endpoint
    test_endpoint(f"{BASE_URL}/buildings/", headers, "Prédios")
    test_endpoint(f"{BASE_URL}/space-types/", headers, "Tipos de Espaço")
    test_endpoint(f"{BASE_URL}/spaces/", headers, "Espaços")
    test_endpoint(f"{BASE_URL}/reservations/", headers, "Reservas")
    
    print("\n📋 Teste completo!")

if __name__ == "__main__":
    main()