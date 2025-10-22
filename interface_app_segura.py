import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Briefcase, MessageSquare, Target, CheckCircle, Brain, Mic, MicOff, Volume2, VolumeX } from 'lucide-react';

const EntrevistaIA = () => {
  const [curriculo, setCurriculo] = useState('');
  const [vaga, setVaga] = useState('');
  const [pergunta, setPergunta] = useState('');
  const [resposta, setResposta] = useState(null);
  const [analise, setAnalise] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [suporteVoz, setSuporteVoz] = useState(true);
  
  const recognitionRef = useRef(null);
  const synthesisRef = useRef(null);

  useEffect(() => {
    // Verifica suporte para reconhecimento de voz
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'pt-BR';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setPergunta(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Erro no reconhecimento:', event.error);
        setIsListening(false);
        if (event.error === 'not-allowed') {
          alert('Permissão de microfone negada. Por favor, habilite o acesso ao microfone.');
        }
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    } else {
      setSuporteVoz(false);
    }

    // Verifica suporte para síntese de voz
    if ('speechSynthesis' in window) {
      synthesisRef.current = window.speechSynthesis;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (synthesisRef.current) {
        synthesisRef.current.cancel();
      }
    };
  }, []);

  const toggleListening = () => {
    if (!suporteVoz) {
      alert('Seu navegador não suporta reconhecimento de voz. Use Chrome, Edge ou Safari.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setPergunta('');
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const falarResposta = (texto) => {
    if (!synthesisRef.current) {
      alert('Seu navegador não suporta síntese de voz.');
      return;
    }

    if (isSpeaking) {
      synthesisRef.current.cancel();
      setIsSpeaking(false);
    } else {
      const utterance = new SpeechSynthesisUtterance(texto);
      utterance.lang = 'pt-BR';
      utterance.rate = 0.9;
      utterance.pitch = 1;
      
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      synthesisRef.current.speak(utterance);
    }
  };

  const extrairCompetencias = (texto) => {
    const competenciasComuns = [
      'liderança', 'comunicação', 'trabalho em equipe', 'gestão',
      'python', 'javascript', 'react', 'sql', 'excel', 'powerbi',
      'análise de dados', 'resolução de problemas', 'criatividade',
      'organização', 'planejamento', 'inglês', 'espanhol',
      'atendimento ao cliente', 'vendas', 'negociação', 'marketing',
      'java', 'node', 'angular', 'vue', 'typescript', 'git',
      'scrum', 'agile', 'kanban', 'design', 'ux', 'ui'
    ];
    
    const textoLower = texto.toLowerCase();
    return competenciasComuns.filter(comp => textoLower.includes(comp));
  };

  const extrairExperiencias = (curriculo) => {
    const linhas = curriculo.split('\n');
    const experiencias = [];
    
    linhas.forEach(linha => {
      if (linha.match(/\d{4}|\d+ anos?|experiência|atuei|trabalhei/i)) {
        experiencias.push(linha.trim());
      }
    });
    
    return experiencias;
  };

  const calcularMatch = (curriculo, vaga) => {
    const compsCurriculo = extrairCompetencias(curriculo);
    const compsVaga = extrairCompetencias(vaga);
    
    const intersecao = compsCurriculo.filter(c => compsVaga.includes(c));
    const matchPercentual = compsVaga.length > 0 
      ? Math.round((intersecao.length / compsVaga.length) * 100)
      : 0;
    
    return {
      percentual: matchPercentual,
      competenciasComuns: intersecao,
      competenciasFaltantes: compsVaga.filter(c => !compsCurriculo.includes(c))
    };
  };

  const classificarPergunta = (pergunta) => {
    const perguntaLower = pergunta.toLowerCase();
    
    if (perguntaLower.match(/conte|descreva|fale sobre|exemplo de quando/i)) {
      return 'comportamental';
    } else if (perguntaLower.match(/como você|qual sua experiência|o que sabe/i)) {
      return 'técnica';
    } else if (perguntaLower.match(/por que|motivação|interesse|objetivo/i)) {
      return 'motivacional';
    } else if (perguntaLower.match(/situação|desafio|problema|conflito/i)) {
      return 'situacional';
    }
    return 'geral';
  };

  const gerarResposta = () => {
    if (!curriculo || !vaga || !pergunta) {
      alert('Preencha todos os campos primeiro!');
      return;
    }

    const match = calcularMatch(curriculo, vaga);
    const tipoPergunta = classificarPergunta(pergunta);
    const experiencias = extrairExperiencias(curriculo);
    const competenciasCurriculo = extrairCompetencias(curriculo);

    let respostaGerada = '';
    
    switch(tipoPergunta) {
      case 'comportamental':
        respostaGerada = `Com base na minha experiência ${experiencias[0] || 'anterior'}, posso compartilhar que desenvolvi habilidades em ${competenciasCurriculo.slice(0, 3).join(', ')}. Um exemplo concreto foi quando apliquei essas competências para alcançar resultados mensuráveis, demonstrando ${match.competenciasComuns[0] || 'capacidade de adaptação'} que está alinhada com o que essa vaga requer.`;
        break;
      
      case 'técnica':
        respostaGerada = `Tenho experiência sólida em ${competenciasCurriculo.slice(0, 2).join(' e ')}, que são fundamentais para esta posição. ${experiencias[0] || 'Em meus projetos anteriores'}, utilizei essas habilidades para entregar soluções eficientes. Estou sempre buscando me atualizar e aprimorar meu conhecimento nessas áreas.`;
        break;
      
      case 'motivacional':
        respostaGerada = `Meu interesse nesta vaga se conecta diretamente com minhas competências em ${match.competenciasComuns.slice(0, 2).join(' e ')}. Vejo uma grande sinergia entre o que desenvolvi ${experiencias[0] ? 'ao longo da minha trajetória' : 'profissionalmente'} e os desafios que esta posição oferece. Busco contribuir de forma significativa aplicando minha experiência.`;
        break;
      
      case 'situacional':
        respostaGerada = `Em situações desafiadoras, costumo aplicar minha experiência em ${competenciasCurriculo[0] || 'resolução de problemas'}. Por exemplo, ${experiencias[0] || 'em um projeto anterior'}, enfrentei um desafio semelhante onde utilizei ${match.competenciasComuns[0] || 'trabalho em equipe'} para encontrar uma solução eficaz, resultando em outcomes positivos mensuráveis.`;
        break;
      
      default:
        respostaGerada = `Considerando minha formação e experiências, especialmente em ${competenciasCurriculo.slice(0, 2).join(' e ')}, acredito estar bem preparado para contribuir nesta posição. ${experiencias[0] || 'Minha trajetória profissional'} me proporcionou desenvolver competências que se alinham com os requisitos desta vaga.`;
    }

    setResposta(respostaGerada);
    setAnalise({
      tipo: tipoPergunta,
      match: match,
      experiencias: experiencias.slice(0, 3)
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="w-8 h-8 text-indigo-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800">Entrevista IA</h1>
                <p className="text-gray-600 text-sm">Sistema inteligente com reconhecimento de voz</p>
              </div>
            </div>
            {!suporteVoz && (
              <div className="bg-yellow-100 border border-yellow-300 text-yellow-800 px-4 py-2 rounded-lg text-sm">
                ⚠️ Use Chrome, Edge ou Safari para recursos de voz
              </div>
            )}
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <User className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-800">Currículo do Candidato</h2>
            </div>
            <textarea
              value={curriculo}
              onChange={(e) => setCurriculo(e.target.value)}
              placeholder="Cole aqui o currículo completo do candidato, incluindo experiências, formação e competências..."
              className="w-full h-48 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Briefcase className="w-5 h-5 text-indigo-600" />
              <h2 className="text-xl font-semibold text-gray-800">Descrição da Vaga</h2>
            </div>
            <textarea
              value={vaga}
              onChange={(e) => setVaga(e.target.value)}
              placeholder="Cole aqui a descrição completa da vaga, incluindo requisitos, responsabilidades e competências desejadas..."
              className="w-full h-48 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <MessageSquare className="w-5 h-5 text-green-600" />
            <h2 className="text-xl font-semibold text-gray-800">Pergunta do Entrevistador</h2>
          </div>
          <div className="flex gap-3">
            <button
              onClick={toggleListening}
              disabled={!suporteVoz}
              className={`${
                isListening 
                  ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                  : 'bg-blue-500 hover:bg-blue-600'
              } ${!suporteVoz ? 'opacity-50 cursor-not-allowed' : ''} text-white px-6 py-3 rounded-lg transition-all flex items-center gap-2 font-semibold`}
            >
              {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              {isListening ? 'Parar' : 'Microfone'}
            </button>
            <input
              type="text"
              value={pergunta}
              onChange={(e) => setPergunta(e.target.value)}
              placeholder={isListening ? "Escutando..." : "Digite ou fale a pergunta do entrevistador..."}
              className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && gerarResposta()}
            />
            <button
              onClick={gerarResposta}
              className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all flex items-center gap-2 font-semibold"
            >
              <Send className="w-5 h-5" />
              Gerar
            </button>
          </div>
          {isListening && (
            <div className="mt-3 flex items-center gap-2 text-red-600 animate-pulse">
              <div className="w-2 h-2 bg-red-600 rounded-full"></div>
              <span className="text-sm font-medium">Escutando sua pergunta...</span>
            </div>
          )}
        </div>

        {resposta && (
          <div className="grid md:grid-cols-3 gap-6">
            <div className="md:col-span-2 bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Target className="w-5 h-5 text-purple-600" />
                  <h2 className="text-xl font-semibold text-gray-800">Resposta Sugerida</h2>
                </div>
                <button
                  onClick={() => falarResposta(resposta)}
                  className={`${
                    isSpeaking 
                      ? 'bg-orange-500 hover:bg-orange-600' 
                      : 'bg-purple-500 hover:bg-purple-600'
                  } text-white px-4 py-2 rounded-lg transition-all flex items-center gap-2 text-sm font-semibold`}
                >
                  {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                  {isSpeaking ? 'Parar' : 'Ouvir'}
                </button>
              </div>
              <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
                <p className="text-gray-800 leading-relaxed">{resposta}</p>
              </div>
              <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                <p className="text-sm text-yellow-800">
                  <strong>💡 Dica:</strong> Personalize esta resposta com detalhes específicos e números concretos da sua experiência para torná-la ainda mais impactante!
                </p>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <h2 className="text-xl font-semibold text-gray-800">Análise</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-semibold text-gray-600 mb-2">Tipo de Pergunta:</p>
                  <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                    {analise.tipo.toUpperCase()}
                  </span>
                </div>

                <div>
                  <p className="text-sm font-semibold text-gray-600 mb-2">Match com a Vaga:</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full transition-all duration-500"
                        style={{ width: `${analise.match.percentual}%` }}
                      />
                    </div>
                    <span className="font-bold text-green-600">{analise.match.percentual}%</span>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-semibold text-gray-600 mb-2">Competências em Comum:</p>
                  <div className="flex flex-wrap gap-2">
                    {analise.match.competenciasComuns.map((comp, idx) => (
                      <span key={idx} className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                        {comp}
                      </span>
                    ))}
                  </div>
                </div>

                {analise.match.competenciasFaltantes.length > 0 && (
                  <div>
                    <p className="text-sm font-semibold text-gray-600 mb-2">Pontos a Mencionar:</p>
                    <div className="flex flex-wrap gap-2">
                      {analise.match.competenciasFaltantes.slice(0, 3).map((comp, idx) => (
                        <span key={idx} className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs">
                          {comp}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EntrevistaIA;
