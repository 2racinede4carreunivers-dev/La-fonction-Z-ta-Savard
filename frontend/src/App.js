import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Composants UI
import { Button } from './components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Input } from './components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Badge } from './components/ui/badge';
import { Separator } from './components/ui/separator';
import { ScrollArea } from './components/ui/scroll-area';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';

// Icônes
import { Search, MessageCircle, BookOpen, Sparkles, Atom, Calculator, Telescope, Send, ArrowRight, Star, Zap, Globe, Brain } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

// Page d'accueil
const HomePage = () => {
  const navigate = useNavigate();
  const [concepts, setConcepts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [conceptsRes, categoriesRes] = await Promise.all([
        axios.get(`${API_URL}/api/concepts`),
        axios.get(`${API_URL}/api/categories`)
      ]);
      setConcepts(conceptsRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (categorie) => {
    const icons = {
      'Géométrie': <Atom className="w-5 h-5" />,
      'Méthodologie': <Calculator className="w-5 h-5" />,
      'Mathématiques': <Brain className="w-5 h-5" />,
      'Théorèmes': <Sparkles className="w-5 h-5" />,
      'Algorithmes': <Zap className="w-5 h-5" />,
      'Cosmologie': <Telescope className="w-5 h-5" />
    };
    return icons[categorie] || <Star className="w-5 h-5" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-cyan-400 mx-auto mb-4"></div>
          <p className="text-white text-lg">Chargement de l'univers...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      {/* Header Hero */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMyIvPjwvZz48L2c+PC9zdmc+')] opacity-20"></div>
        
        <div className="relative container mx-auto px-6 py-16">
          <div className="text-center max-w-4xl mx-auto">
            <div className="mb-8">
              <div className="inline-flex items-center gap-2 bg-cyan-900/30 backdrop-blur-sm border border-cyan-400/30 rounded-full px-4 py-2 mb-6">
                <Globe className="w-4 h-4 text-cyan-400" />
                <span className="text-cyan-300 text-sm font-medium">Théorie de Philippe Thomas Savard</span>
              </div>
              
              <h1 className="text-6xl font-bold bg-gradient-to-r from-cyan-400 via-blue-300 to-purple-400 bg-clip-text text-transparent mb-6 leading-tight">
                L'univers est au carré
              </h1>
              
              <p className="text-xl text-blue-100 mb-8 leading-relaxed">
                Explorez une approche géométrique révolutionnaire des nombres premiers, 
                alliant intuition mathématique et vision cosmologique dans une théorie personnelle unique.
              </p>
            </div>

            <div className="flex flex-wrap justify-center gap-4 mb-12">
              <Button 
                onClick={() => navigate('/explorer')}
                className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
              >
                <BookOpen className="w-5 h-5 mr-2" />
                Explorer la théorie
              </Button>
              
              <Button 
                onClick={() => navigate('/chat')}
                variant="outline"
                className="border-2 border-cyan-400 text-cyan-300 hover:bg-cyan-400 hover:text-slate-900 px-8 py-3 rounded-full font-semibold transition-all duration-300"
              >
                <MessageCircle className="w-5 h-5 mr-2" />
                Discuter avec l'IA
              </Button>
            </div>

            {/* Statistiques */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl mx-auto">
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-cyan-400 mb-2">{concepts.length}</div>
                <div className="text-blue-200">Concepts explorés</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-purple-400 mb-2">{categories.length}</div>
                <div className="text-blue-200">Domaines d'étude</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-indigo-400 mb-2">3</div>
                <div className="text-blue-200">Documents sources</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Section Catégories */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-white mb-12">
          Domaines d'exploration
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category) => (
            <Card 
              key={category.categorie}
              className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-cyan-400/30 transition-all duration-300 hover:scale-105 cursor-pointer"
              onClick={() => navigate(`/explorer?categorie=${category.categorie}`)}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-600/20">
                    {getCategoryIcon(category.categorie)}
                  </div>
                  <div>
                    <CardTitle className="text-white text-lg">{category.categorie}</CardTitle>
                    <CardDescription className="text-blue-200">
                      {category.count} concept{category.count > 1 ? 's' : ''}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-cyan-300 font-semibold">Explorer</span>
                  <ArrowRight className="w-4 h-4 text-cyan-400" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Section Concepts récents */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-white mb-12">
          Concepts fondamentaux
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {concepts.slice(0, 6).map((concept) => (
            <Card 
              key={concept.id}
              className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-purple-400/30 transition-all duration-300 hover:scale-105 cursor-pointer group"
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-white text-lg mb-2 group-hover:text-cyan-300 transition-colors">
                      {concept.titre}
                    </CardTitle>
                    <CardDescription className="text-blue-200">
                      {concept.description}
                    </CardDescription>
                  </div>
                  <Badge variant="secondary" className="bg-purple-900/50 text-purple-300 border-purple-400/30">
                    {concept.categorie}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-1 mb-4">
                  {concept.mots_cles.slice(0, 3).map((mot) => (
                    <Badge key={mot} variant="outline" className="text-xs border-cyan-400/30 text-cyan-300">
                      {mot}
                    </Badge>
                  ))}
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  className="text-cyan-400 hover:text-cyan-300 hover:bg-cyan-400/10 p-0"
                >
                  Lire plus <ArrowRight className="w-3 h-3 ml-1" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

// Page Explorer
const ExplorerPage = () => {
  const [concepts, setConcepts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    // Récupérer la catégorie depuis l'URL si présente
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('categorie');
    if (categoryParam) {
      setSelectedCategory(categoryParam);
    }
  }, []);

  const fetchData = async () => {
    try {
      const [conceptsRes, categoriesRes] = await Promise.all([
        axios.get(`${API_URL}/api/concepts`),
        axios.get(`${API_URL}/api/categories`)
      ]);
      setConcepts(conceptsRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchData();
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/search`, {
        query: searchQuery,
        categorie: selectedCategory || null
      });
      setConcepts(response.data);
    } catch (error) {
      console.error('Erreur lors de la recherche:', error);
    }
  };

  const filteredConcepts = selectedCategory 
    ? concepts.filter(c => c.categorie === selectedCategory)
    : concepts;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Explorer la théorie</h1>
          <p className="text-blue-200">Naviguez parmi les concepts et découvrez les liens entre géométrie, nombres premiers et cosmologie.</p>
        </div>

        {/* Filtres et recherche */}
        <Card className="bg-white/5 backdrop-blur-sm border border-white/10 mb-8">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="flex gap-2">
                  <Input
                    placeholder="Rechercher dans les concepts..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="bg-white/10 border-white/20 text-white placeholder:text-blue-200"
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  />
                  <Button onClick={handleSearch} className="bg-cyan-600 hover:bg-cyan-700">
                    <Search className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                <Button
                  variant={!selectedCategory ? "default" : "outline"}
                  onClick={() => setSelectedCategory('')}
                  className={!selectedCategory ? "bg-cyan-600" : "border-white/20 text-white hover:bg-white/10"}
                >
                  Tous
                </Button>
                {categories.map((cat) => (
                  <Button
                    key={cat.categorie}
                    variant={selectedCategory === cat.categorie ? "default" : "outline"}
                    onClick={() => setSelectedCategory(cat.categorie)}
                    className={selectedCategory === cat.categorie ? "bg-cyan-600" : "border-white/20 text-white hover:bg-white/10"}
                  >
                    {cat.categorie} ({cat.count})
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Liste des concepts */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredConcepts.map((concept) => (
            <Dialog key={concept.id}>
              <DialogTrigger asChild>
                <Card className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-cyan-400/30 transition-all duration-300 hover:scale-105 cursor-pointer">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-white text-lg mb-2">
                        {concept.titre}
                      </CardTitle>
                      <Badge variant="secondary" className="bg-purple-900/50 text-purple-300 border-purple-400/30">
                        {concept.categorie}
                      </Badge>
                    </div>
                    <CardDescription className="text-blue-200">
                      {concept.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-1 mb-4">
                      {concept.mots_cles.map((mot) => (
                        <Badge key={mot} variant="outline" className="text-xs border-cyan-400/30 text-cyan-300">
                          {mot}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-xs text-blue-300">
                      Source: {concept.document_source}
                    </div>
                  </CardContent>
                </Card>
              </DialogTrigger>
              
              <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-2xl">
                <DialogHeader>
                  <DialogTitle className="text-2xl text-cyan-400">{concept.titre}</DialogTitle>
                  <DialogDescription className="text-blue-200">
                    {concept.description}
                  </DialogDescription>
                </DialogHeader>
                
                <div className="space-y-4">
                  <div>
                    <Badge className="bg-purple-900/50 text-purple-300 border-purple-400/30">
                      {concept.categorie}
                    </Badge>
                  </div>
                  
                  <Separator className="bg-slate-700" />
                  
                  <div>
                    <h4 className="font-semibold text-cyan-300 mb-2">Contenu détaillé</h4>
                    <p className="text-blue-100 leading-relaxed">{concept.contenu}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-cyan-300 mb-2">Mots-clés</h4>
                    <div className="flex flex-wrap gap-1">
                      {concept.mots_cles.map((mot) => (
                        <Badge key={mot} variant="outline" className="border-cyan-400/30 text-cyan-300">
                          {mot}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div className="text-sm text-blue-300 pt-2">
                    Document source: {concept.document_source}
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          ))}
        </div>

        {filteredConcepts.length === 0 && !loading && (
          <div className="text-center py-12">
            <p className="text-blue-200 text-lg">Aucun concept trouvé pour cette recherche.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Page Chat
const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { type: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    
    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: inputMessage,
        session_id: sessionId
      });
      
      setSessionId(response.data.session_id);
      
      const aiMessage = { type: 'ai', content: response.data.response };
      setMessages(prev => [...prev, aiMessage]);
      
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      const errorMessage = { 
        type: 'ai', 
        content: 'Désolé, une erreur s\'est produite. Veuillez réessayer.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setInputMessage('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-6 py-8 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Assistant IA spécialisé</h1>
          <p className="text-blue-200">Posez vos questions sur la théorie "L'univers est au carré". L'IA est spécialisée uniquement dans cette théorie.</p>
        </div>

        <Card className="bg-white/5 backdrop-blur-sm border border-white/10 h-[600px] flex flex-col">
          <CardHeader className="border-b border-white/10">
            <CardTitle className="text-white flex items-center gap-2">
              <Brain className="w-5 h-5 text-cyan-400" />
              Chat avec Claude (spécialisé)
            </CardTitle>
          </CardHeader>
          
          <CardContent className="flex-1 flex flex-col p-0">
            <ScrollArea className="flex-1 p-6">
              <div className="space-y-4">
                {messages.length === 0 && (
                  <div className="text-center py-8">
                    <div className="bg-gradient-to-r from-cyan-500/20 to-blue-600/20 rounded-2xl p-6 max-w-md mx-auto">
                      <Brain className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
                      <h3 className="text-white font-semibold mb-2">Bonjour ! Je suis votre assistant IA</h3>
                      <p className="text-blue-200 text-sm">
                        Je suis spécialisé dans la théorie "L'univers est au carré" de Philippe Thomas Savard. 
                        Posez-moi vos questions sur cette théorie fascinante !
                      </p>
                    </div>
                  </div>
                )}
                
                {messages.map((message, index) => (
                  <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] rounded-2xl p-4 ${
                      message.type === 'user' 
                        ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white' 
                        : 'bg-white/10 backdrop-blur-sm text-blue-100'
                    }`}>
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                  </div>
                ))}
                
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-cyan-400"></div>
                        <span className="text-blue-200">L'IA réfléchit...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>
            
            <div className="border-t border-white/10 p-6">
              <div className="flex gap-2">
                <Input
                  placeholder="Posez votre question sur la théorie..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  className="bg-white/10 border-white/20 text-white placeholder:text-blue-200"
                  onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
                  disabled={loading}
                />
                <Button 
                  onClick={sendMessage} 
                  disabled={loading || !inputMessage.trim()}
                  className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Navigation
const Navigation = () => {
  return (
    <nav className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <span className="text-white font-bold text-lg">L'univers est au carré</span>
          </Link>
          
          <div className="flex items-center gap-6">
            <Link to="/" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Accueil
            </Link>
            <Link to="/explorer" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Explorer
            </Link>
            <Link to="/chat" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Chat IA
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

// App principale
const App = () => {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/explorer" element={<ExplorerPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;