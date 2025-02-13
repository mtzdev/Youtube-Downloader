# 🎬 YouTube Video/Audio Downloader
Baixe vídeos e músicas do YouTube de forma rápida e prática! Este aplicativo permite pesquisar e baixar vídeos em MP4 e músicas em MP3 com diversas opções de qualidade. Interface moderna e prática, suporte a temas claro e escuro, e total controle sobre suas preferências.

## 👀 Demonstração do app
![Demonstração](https://github.com/user-attachments/assets/1dd35e40-78ca-420d-ac76-ca48c988bda4)

## 🚀 Funcionalidades
✅ **Busca integrada** - Pesquise vídeos diretamente pelo aplicativo ou insira o link do YouTube.<br>
✅ **Download rápido** - Baixe vídeos e músicas em diversas qualidades:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🎥 Vídeos: 1080p, 720p, 480p, 360p<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🎵 Áudio: 320kbps, 256kbps, 192kbps, 128kbps<br>
✅ **Modo escuro e claro** - Escolha o tema que preferir.<br>
✅ **Configurações personalizáveis** - Defina pasta de destino, número máximo de resultados na busca e tema da interface.<br>
✅ **Interface intuitiva** - Fácil de usar, sem complicações.

---

## 🛠️ Como Usar

1. **Pesquise um vídeo** digitando o nome ou cole o link diretamente na barra de busca.
2. **Escolha o formato** desejado: MP4 para vídeo ou MP3 para áudio.
4. **Selecione a qualidade** de download.
5. **Defina a pasta de destino** clicando no texto abaixo do botão "BAIXAR".
6. **Clique no botão Baixar** e acompanhe o progresso aguardando a conclusão do download.
7. **Acesse seus arquivos** na pasta configurada!

**OBS:** Demais configurações podem ser acessadas através do botão de configurações. (Localizado a direita da barra de pesquisa)

---

## 📥 Instalação

### 🔹 Baixar versão pronta (.exe)
A versão compilada está disponível na aba **[Releases](https://github.com/mtzdev/Youtube-Downloader/releases)** do GitHub. Basta baixar e executar!

### 🔹 Compilar manualmente
Caso queira compilar a aplicação por conta própria:

#### **1️⃣ Instale o Python**
- Recomendado usar **Python 3.12.5** (Versão testada)
- ⚠️ Problemas podem ocorrer a partir da 3.13

#### **2️⃣ Clone o repositório**
```bash
git clone https://github.com/mtzdev/Youtube-Downloader.git
```

#### **3️⃣ Instale as dependências**
```bash
pip install -r requirements.txt
```

#### **4️⃣ Compile com Nuitka**
```bash
python -m nuitka --onefile --plugin-enable=pyside6 --windows-console-mode=disabled --windows-icon-from-ico=data/logo.ico --include-data-files="data/*=data/" main.py
```

Isso gerará um executável na pasta `dist/` pronto para uso.

---

## 🛠️ Contribuição
Se quiser contribuir com melhorias ou correções, fique à vontade para abrir um PR ou relatar problemas.

📜 **Licença:** [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)  
