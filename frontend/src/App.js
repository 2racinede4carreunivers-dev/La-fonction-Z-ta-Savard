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
import { Search, MessageCircle, BookOpen, Sparkles, Atom, Calculator, Telescope, Send, ArrowRight, Star, Zap, Globe, Brain, Play, Info, TrendingUp, Layers, Target } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

// Page d'accueil enrichie
const HomePage = () => {
  const navigate = useNavigate();
  const [concepts, setConcepts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [tableaux, setTableaux] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [conceptsRes, categoriesRes, tableauxRes] = await Promise.all([
        axios.get(`${API_URL}/api/concepts`),
        axios.get(`${API_URL}/api/categories`),
        axios.get(`${API_URL}/api/tableaux-philippot`)
      ]);
      setConcepts(conceptsRes.data);
      setCategories(categoriesRes.data);
      setTableaux(tableauxRes.data);
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (categorie) => {
    const icons = {
      'Géométrie': <Atom className="w-5 h-5" />,
      'Méthode': <Layers className="w-5 h-5" />,
      'Innovation': <Sparkles className="w-5 h-5" />,
      'Calculs': <Calculator className="w-5 h-5" />,
      'Exemples': <Target className="w-5 h-5" />,
      'Relations': <TrendingUp className="w-5 h-5" />,
      'Validation': <Star className="w-5 h-5" />
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
                Découvrez la méthode révolutionnaire de Philippôt : 14 tableaux géométriques pour déterminer 
                les nombres premiers avec une précision parfaite, validée par l'Intelligence Artificielle.
              </p>
            </div>

            <div className="flex flex-wrap justify-center gap-4 mb-12">
              <Button 
                onClick={() => navigate('/methode-philippot')}
                className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
              >
                <Play className="w-5 h-5 mr-2" />
                Méthode de Philippôt
              </Button>
              
              <Button 
                onClick={() => navigate('/explorer')}
                variant="outline"
                className="border-2 border-purple-400 text-purple-300 hover:bg-purple-400 hover:text-slate-900 px-8 py-3 rounded-full font-semibold transition-all duration-300"
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
                IA spécialisée
              </Button>
            </div>

            {/* Statistiques enrichies */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-cyan-400 mb-2">{tableaux.length}</div>
                <div className="text-blue-200">Tableaux de Philippôt</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-purple-400 mb-2">{concepts.length}</div>
                <div className="text-blue-200">Concepts détaillés</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-indigo-400 mb-2">{categories.length}</div>
                <div className="text-blue-200">Domaines d'étude</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="text-3xl font-bold text-emerald-400 mb-2">8</div>
                <div className="text-blue-200">Position du Digamma</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Section Exemples précis de la Méthode */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-white mb-4">
          Exemples précis de la Méthode de Philippôt
        </h2>
        <p className="text-center text-blue-200 mb-12 max-w-3xl mx-auto">
          Découvrez 3 calculs complets détaillés montrant comment les séquences de racines carrées 
          génèrent précisément les nombres premiers 29, 31, et 2999.
        </p>
        
        <div className="space-y-8">
          {/* Tableau détaillé pour le nombre premier 29 */}
          <Card className="bg-white/5 backdrop-blur-sm border border-cyan-400/30">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl text-cyan-400 mb-2">
                    Nombre Premier 29 - 10ème position
                  </CardTitle>
                  <CardDescription className="text-blue-200">
                    Calcul complet avec 10 données - Rapport triangulaire optimisé
                  </CardDescription>
                </div>
                <div className="text-4xl font-bold text-purple-400">29</div>
              </div>
            </CardHeader>
            
            <CardContent>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Suite 1 */}
                <Card className="bg-slate-800/50 border-slate-600">
                  <CardHeader>
                    <CardTitle className="text-cyan-300 text-lg">Suite 1 (Racines carrées)</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm">
                      {["√5", "√13", "√25", "√41", "√61", "√85", "√113", "√145", "√181", "√221"].map((valeur, index) => (
                        <div key={index} className="flex justify-between">
                          <span className="text-blue-200">Position {index + 1} :</span>
                          <code className={`${index === 7 ? 'text-yellow-400 font-bold' : 'text-white'} bg-slate-700 px-2 py-1 rounded`}>
                            {valeur} {index === 7 && '← Digamma'}
                          </code>
                        </div>
                      ))}
                      <div className="border-t border-slate-600 pt-2 mt-3">
                        <div className="flex justify-between font-semibold">
                          <span className="text-cyan-300">Somme :</span>
                          <code className="text-cyan-300">√3452805</code>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Suite 2 */}
                <Card className="bg-slate-800/50 border-slate-600">
                  <CardHeader>
                    <CardTitle className="text-purple-300 text-lg">Suite 2 (Carrés)</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm">
                      {["5", "13", "25", "41", "61", "85", "113", "145", "181", "221"].map((valeur, index) => (
                        <div key={index} className="flex justify-between">
                          <span className="text-blue-200">Position {index + 1} :</span>
                          <code className="text-white bg-slate-700 px-2 py-1 rounded">
                            {valeur}
                          </code>
                        </div>
                      ))}
                      <div className="border-t border-slate-600 pt-2 mt-3">
                        <div className="flex justify-between font-semibold">
                          <span className="text-purple-300">Somme :</span>
                          <code className="text-purple-300">√13300805</code>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Calcul final */}
              <Card className="bg-gradient-to-r from-emerald-900/30 to-cyan-900/30 border-emerald-400/30 mt-6">
                <CardHeader>
                  <CardTitle className="text-emerald-300 text-lg">Calcul Final</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="bg-slate-800/70 p-4 rounded-lg">
                      <div className="text-sm text-blue-200 mb-2">Digamma (8ème position) :</div>
                      <code className="text-yellow-400 text-lg">√81920</code>
                    </div>
                    <div className="bg-slate-800/70 p-4 rounded-lg">
                      <div className="text-sm text-blue-200 mb-2">Formule appliquée :</div>
                      <code className="text-emerald-300 text-lg">(√3452805 − √81920) / √5120 = 29</code>
                    </div>
                    <div className="text-center">
                      <Badge className="bg-purple-600 text-white text-lg px-4 py-2">
                        29 est le 10ème nombre premier
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </CardContent>
          </Card>

          {/* Tableau détaillé pour le nombre premier 31 */}
          <Card className="bg-white/5 backdrop-blur-sm border border-purple-400/30">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl text-purple-400 mb-2">
                    Nombre Premier 31 - 11ème position
                  </CardTitle>
                  <CardDescription className="text-blue-200">
                    Calcul avec 11 données - Séquence étendue
                  </CardDescription>
                </div>
                <div className="text-4xl font-bold text-cyan-400">31</div>
              </div>
            </CardHeader>
            
            <CardContent>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Suite 1 étendue */}
                <Card className="bg-slate-800/50 border-slate-600">
                  <CardHeader>
                    <CardTitle className="text-cyan-300 text-lg">Suite 1 (11 termes)</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm">
                      {["√5", "√13", "√25", "√41", "√61", "√85", "√113", "√145", "√181", "√221", "√265"].map((valeur, index) => (
                        <div key={index} className="flex justify-between">
                          <span className="text-blue-200">Position {index + 1} :</span>
                          <code className={`${index === 7 ? 'text-yellow-400 font-bold' : 'text-white'} bg-slate-700 px-2 py-1 rounded`}>
                            {valeur} {index === 7 && '← Digamma'}
                          </code>
                        </div>
                      ))}
                      <div className="border-t border-slate-600 pt-2 mt-3">
                        <div className="flex justify-between font-semibold">
                          <span className="text-cyan-300">Somme :</span>
                          <code className="text-cyan-300">√7079856640</code>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Calcul pour 31 */}
                <Card className="bg-gradient-to-b from-purple-900/30 to-indigo-900/30 border-purple-400/30">
                  <CardHeader>
                    <CardTitle className="text-purple-300 text-lg">Calcul pour 31</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="bg-slate-800/70 p-3 rounded">
                        <div className="text-sm text-blue-200">Digamma (8ème) :</div>
                        <code className="text-yellow-400">√145 = √281300</code>
                      </div>
                      <div className="bg-slate-800/70 p-3 rounded">
                        <div className="text-sm text-blue-200">Suite 2 :</div>
                        <code className="text-purple-300">√6.333294724 × 10¹⁰</code>
                      </div>
                      <div className="bg-slate-800/70 p-3 rounded">
                        <div className="text-sm text-blue-200">Calcul intermédiaire :</div>
                        <code className="text-emerald-300">√7079856640 - √281300</code>
                      </div>
                      <div className="text-center">
                        <Badge className="bg-cyan-600 text-white text-lg px-4 py-2">
                          Résultat : 31 (11ème premier)
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>

          {/* Tableau pour le rapport 1/5 donnant 2999 */}
          <Card className="bg-white/5 backdrop-blur-sm border border-emerald-400/30">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl text-emerald-400 mb-2">
                    Rapport 1/5 → Premier 2999
                  </CardTitle>
                  <CardDescription className="text-blue-200">
                    Triangle base/hauteur 1/5 - Calcul avancé
                  </CardDescription>
                </div>
                <div className="text-4xl font-bold text-emerald-400">2999</div>
              </div>
            </CardHeader>
            
            <CardContent>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Configuration du triangle */}
                <Card className="bg-slate-800/50 border-slate-600">
                  <CardHeader>
                    <CardTitle className="text-emerald-300 text-lg">Configuration Géométrique</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-blue-200">Rapport base/hauteur :</span>
                        <code className="text-emerald-400 bg-slate-700 px-2 py-1 rounded">1/5</code>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-blue-200">Séquence générée :</span>
                        <code className="text-white bg-slate-700 px-2 py-1 rounded">Position 55-56</code>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-blue-200">Digamma calculé :</span>
                        <code className="text-yellow-400 bg-slate-700 px-2 py-1 rounded">√((55)² + 56)¹/²</code>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Calcul final complexe */}
                <Card className="bg-gradient-to-b from-emerald-900/30 to-teal-900/30 border-emerald-400/30">
                  <CardHeader>
                    <CardTitle className="text-emerald-300 text-lg">Calcul Final</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="bg-slate-800/70 p-3 rounded">
                        <div className="text-sm text-blue-200 mb-1">Suite 1 :</div>
                        <code className="text-cyan-300 text-sm">√3.580561045 × 10¹⁵</code>
                      </div>
                      <div className="bg-slate-800/70 p-3 rounded">
                        <div className="text-sm text-blue-200 mb-1">Suite 2 :</div>
                        <code className="text-purple-300 text-sm">√1.452125243 × 10¹⁴</code>
                      </div>
                      <div className="bg-slate-800/70 p-3 rounded">
                        <div className="text-sm text-blue-200 mb-1">Formule :</div>
                        <code className="text-emerald-300 text-xs break-all">
                          (√3.580561045×10¹⁵ - √1.452125243×10¹⁴) / √((55)²+56) = 2999
                        </code>
                      </div>
                      <div className="text-center">
                        <Badge className="bg-emerald-600 text-white text-lg px-4 py-2">
                          2999 est un nombre premier
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="text-center mt-12">
          <Button 
            onClick={() => navigate('/methode-philippot')}
            className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white px-8 py-3 rounded-full font-semibold"
          >
            Voir tous les 14 tableaux <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </div>

      {/* Section Concepts */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-white mb-12">
          Concepts fondamentaux enrichis
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
                  <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-600/20">
                    {getCategoryIcon(concept.categorie)}
                  </div>
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
                <Badge variant="secondary" className="bg-purple-900/50 text-purple-300 border-purple-400/30">
                  {concept.categorie}
                </Badge>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

// Page Méthode de Philippôt (nouvelle)
const MethodePhilippotPage = () => {
  const [tableaux, setTableaux] = useState([]);
  const [selectedTableau, setSelectedTableau] = useState(null);
  const [calculatorData, setCalculatorData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTableaux();
  }, []);

  const fetchTableaux = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/tableaux-philippot`);
      setTableaux(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des tableaux:', error);
    } finally {
      setLoading(false);
    }
  };

  const simulateCalculation = async (rapport) => {
    const [base, hauteur] = rapport.split('/').map(Number);
    try {
      const response = await axios.post(`${API_URL}/api/calculateur-philippot`, {
        rapport_base: base,
        rapport_hauteur: hauteur
      });
      setCalculatorData(response.data);
    } catch (error) {
      console.error('Erreur lors du calcul:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">La Méthode de Philippôt</h1>
          <p className="text-blue-200 text-lg">
            14 tableaux géométriques utilisant différents rapports base/hauteur pour déterminer les nombres premiers avec précision.
          </p>
        </div>

        {/* Guide de la méthode */}
        <Card className="bg-white/5 backdrop-blur-sm border border-white/10 mb-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Info className="w-5 h-5 text-cyan-400" />
              Comment fonctionne la méthode
            </CardTitle>
          </CardHeader>
          <CardContent className="text-blue-100">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-cyan-300 mb-2">🔸 Construction des suites</h4>
                <p className="text-sm mb-4">
                  Pour chaque rapport base/hauteur, on construit deux suites de 10 termes utilisant des racines carrées selon la formule √((n+i)² + (n+i+1)²).
                </p>
                
                <h4 className="font-semibold text-cyan-300 mb-2">🔸 Calcul du Digamma</h4>
                <p className="text-sm">
                  Le "Digamma" est toujours calculé à la 8ème position selon √((n+7)² + (n+8)²). C'est l'innovation clé de Philippôt !
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-cyan-300 mb-2">🔸 Formule finale</h4>
                <p className="text-sm mb-4">
                  On applique soit une soustraction soit une addition du Digamma avec la somme de la première suite, puis on divise par un terme spécifique.
                </p>
                
                <h4 className="font-semibold text-cyan-300 mb-2">🔸 Résultat</h4>
                <p className="text-sm">
                  Chaque calcul donne un nombre premier précis ! La méthode a été validée par une IA.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Grille des tableaux */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tableaux.map((tableau) => (
            <Dialog key={tableau.id}>
              <DialogTrigger asChild>
                <Card className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-cyan-400/30 transition-all duration-300 hover:scale-105 cursor-pointer">
                  <CardHeader className="pb-4">
                    <div className="flex items-center justify-between mb-2">
                      <Badge className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white">
                        Rapport {tableau.rapport}
                      </Badge>
                      <div className="text-2xl font-bold text-purple-400">
                        {tableau.nombre_premier_resultat}
                      </div>
                    </div>
                    <CardTitle className="text-white text-lg">
                      {tableau.description}
                    </CardTitle>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-blue-200">Digamma (8ème) :</span>
                        <code className="text-cyan-300 bg-slate-800/50 px-2 py-1 rounded">
                          {tableau.digamma_valeur}
                        </code>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-blue-200">Position :</span>
                        <span className="text-purple-300 font-semibold">
                          {tableau.position_nombre_premier}ème nombre premier
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-blue-200">Opération :</span>
                        <Badge variant="outline" className={
                          tableau.calcul_detaille.operation_digamma === 'soustraction' 
                            ? "border-red-400/30 text-red-300" 
                            : "border-green-400/30 text-green-300"
                        }>
                          {tableau.calcul_detaille.operation_digamma}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </DialogTrigger>
              
              <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-4xl max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="text-2xl text-cyan-400 flex items-center gap-2">
                    <Calculator className="w-6 h-6" />
                    Tableau {tableau.rapport} - Détails complets
                  </DialogTitle>
                  <DialogDescription className="text-blue-200">
                    Calcul détaillé pour obtenir le nombre premier {tableau.nombre_premier_resultat}
                  </DialogDescription>
                </DialogHeader>
                
                <div className="space-y-6">
                  {/* Informations principales */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="bg-slate-800 border-slate-700">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-purple-400 mb-1">
                          {tableau.nombre_premier_resultat}
                        </div>
                        <div className="text-sm text-blue-200">
                          {tableau.position_nombre_premier}ème nombre premier
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-slate-800 border-slate-700">
                      <CardContent className="p-4 text-center">
                        <div className="text-lg font-bold text-cyan-400 mb-1">
                          Position 8
                        </div>
                        <div className="text-sm text-blue-200">
                          Digamma calculé
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-slate-800 border-slate-700">
                      <CardContent className="p-4 text-center">
                        <div className="text-lg font-bold text-emerald-400 mb-1">
                          {tableau.calcul_detaille.operation_digamma}
                        </div>
                        <div className="text-sm text-blue-200">
                          Opération utilisée
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Suites détaillées */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card className="bg-slate-800 border-slate-700">
                      <CardHeader>
                        <CardTitle className="text-cyan-300 text-lg">Suite 1 (Racines carrées)</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {tableau.suite_1.map((valeur, index) => (
                            <div key={index} className="flex justify-between text-sm">
                              <span className="text-blue-200">Position {index + 1} :</span>
                              <code className={`${index === 7 ? 'text-yellow-400 font-bold' : 'text-white'} bg-slate-700 px-2 py-1 rounded`}>
                                {valeur} {index === 7 && '← Digamma'}
                              </code>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-slate-800 border-slate-700">
                      <CardHeader>
                        <CardTitle className="text-purple-300 text-lg">Suite 2 (Carrés)</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {tableau.suite_2.map((valeur, index) => (
                            <div key={index} className="flex justify-between text-sm">
                              <span className="text-blue-200">Position {index + 1} :</span>
                              <code className="text-white bg-slate-700 px-2 py-1 rounded">
                                {valeur}
                              </code>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Calculs */}
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-emerald-300 text-lg">Calcul final</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="bg-slate-700 p-4 rounded-lg">
                          <div className="text-sm text-blue-200 mb-2">Somme Suite 1 :</div>
                          <code className="text-cyan-300">{tableau.calcul_detaille.somme_suite_1}</code>
                        </div>
                        
                        <div className="bg-slate-700 p-4 rounded-lg">
                          <div className="text-sm text-blue-200 mb-2">Digamma (8ème position) :</div>
                          <code className="text-yellow-400">{tableau.digamma_valeur}</code>
                        </div>
                        
                        <div className="bg-slate-700 p-4 rounded-lg">
                          <div className="text-sm text-blue-200 mb-2">Formule appliquée :</div>
                          <code className="text-emerald-300">{tableau.calcul_detaille.formule}</code>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <div className="text-center">
                    <Button 
                      onClick={() => simulateCalculation(tableau.rapport)}
                      className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700"
                    >
                      <Play className="w-4 h-4 mr-2" />
                      Simuler le calcul
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          ))}
        </div>
      </div>
    </div>
  );
};

// Page Explorer enrichie
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

  const getCategoryIcon = (categorie) => {
    const icons = {
      'Géométrie': <Atom className="w-4 h-4" />,
      'Méthode': <Layers className="w-4 h-4" />,
      'Innovation': <Sparkles className="w-4 h-4" />,
      'Calculs': <Calculator className="w-4 h-4" />,
      'Exemples': <Target className="w-4 h-4" />,
      'Relations': <TrendingUp className="w-4 h-4" />,
      'Validation': <Star className="w-4 h-4" />
    };
    return icons[categorie] || <Star className="w-4 h-4" />;
  };

  const filteredConcepts = selectedCategory 
    ? concepts.filter(c => c.categorie === selectedCategory)
    : concepts;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Explorer la théorie enrichie</h1>
          <p className="text-blue-200">Découvrez tous les aspects de la méthode révolutionnaire de Philippôt et ses applications.</p>
        </div>

        {/* Filtres et recherche */}
        <Card className="bg-white/5 backdrop-blur-sm border border-white/10 mb-8">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="flex gap-2">
                  <Input
                    placeholder="Rechercher concepts, méthodes, calculs..."
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
                    <span className="mr-1">{getCategoryIcon(cat.categorie)}</span>
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
                      <div className="flex-1">
                        <CardTitle className="text-white text-lg mb-2">
                          {concept.titre}
                        </CardTitle>
                        <CardDescription className="text-blue-200">
                          {concept.description}
                        </CardDescription>
                      </div>
                      <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-600/20">
                        {getCategoryIcon(concept.categorie)}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-1 mb-4">
                      {concept.mots_cles.map((mot) => (
                        <Badge key={mot} variant="outline" className="text-xs border-cyan-400/30 text-cyan-300">
                          {mot}
                        </Badge>
                      ))}
                    </div>
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary" className="bg-purple-900/50 text-purple-300 border-purple-400/30">
                        {concept.categorie}
                      </Badge>
                      <div className="text-xs text-blue-300">
                        {concept.document_source.split('.')[0]}
                      </div>
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

// Page Chat enrichie
const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [extendedMode, setExtendedMode] = useState(true);

  // Charger les documents au démarrage
  useEffect(() => {
    if (sessionId) {
      fetchDocuments();
    }
  }, [sessionId]);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/documents/${sessionId}`);
      setUploadedDocuments(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des documents:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    if (files.length === 0) return;

    setUploading(true);
    const currentSessionId = sessionId || new Date().getTime().toString();

    for (const file of files) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', currentSessionId);

        const response = await axios.post(`${API_URL}/api/upload-document`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (response.data.success) {
          const analysisMessage = {
            type: 'system',
            content: `📄 Document "${file.name}" analysé avec succès !\n\n🔍 Analyse automatique :\n${response.data.analysis}`
          };
          setMessages(prev => [...prev, analysisMessage]);
        }

      } catch (error) {
        console.error('Erreur lors de l\'upload:', error);
        const errorMessage = {
          type: 'system',
          content: `❌ Erreur lors de l'upload de "${file.name}"`
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    }

    setSessionId(currentSessionId);
    setUploading(false);
    await fetchDocuments();
    
    // Réinitialiser l'input
    event.target.value = '';
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { type: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    
    try {
      const endpoint = extendedMode ? '/api/chat-extended' : '/api/chat';
      const requestData = extendedMode ? {
        message: inputMessage,
        session_id: sessionId,
        attached_files: selectedFiles,
        context_mode: 'extended'
      } : {
        message: inputMessage,
        session_id: sessionId
      };

      const response = await axios.post(`${API_URL}${endpoint}`, requestData);
      
      setSessionId(response.data.session_id);
      
      const aiMessage = { type: 'ai', content: response.data.response, extended: extendedMode };
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
      setSelectedFiles([]);
    }
  };

  const suggestions = [
    "Explique-moi la méthode de Philippôt",
    "Comment calcule-t-on le Digamma à la 8ème position ?",
    "Pourquoi le rapport 1/2 donne-t-il 29 ?",
    "Quelle est la différence avec les méthodes classiques ?",
    "Comment l'IA a-t-elle validé la théorie ?"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-6 py-8 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Assistant IA spécialisé</h1>
          <p className="text-blue-200">Claude Sonnet 3.5 expert en théorie "L'univers est au carré" et méthode de Philippôt.</p>
        </div>

        <Card className="bg-white/5 backdrop-blur-sm border border-white/10 h-[700px] flex flex-col">
          <CardHeader className="border-b border-white/10">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-white flex items-center gap-2">
                  <Brain className="w-5 h-5 text-cyan-400" />
                  Assistant IA Personnel - Philippe Thomas Savard
                </CardTitle>
                <CardDescription className="text-blue-200">
                  {extendedMode ? 'Mode enrichi avec mémoire étendue et analyse de documents' : 'Mode standard spécialisé dans votre théorie'}
                </CardDescription>
              </div>
              
              <div className="flex items-center gap-2">
                <Button
                  variant={extendedMode ? "default" : "outline"}
                  size="sm"
                  onClick={() => setExtendedMode(!extendedMode)}
                  className={extendedMode ? "bg-emerald-600 hover:bg-emerald-700" : "border-emerald-400 text-emerald-300 hover:bg-emerald-400/10"}
                >
                  {extendedMode ? "🧠 Enrichi" : "📝 Standard"}
                </Button>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="flex-1 flex flex-col p-0">
            <ScrollArea className="flex-1 p-6">
              <div className="space-y-4">
                {messages.length === 0 && (
                  <div className="text-center py-8">
                    <div className="bg-gradient-to-r from-cyan-500/20 to-blue-600/20 rounded-2xl p-6 max-w-md mx-auto mb-6">
                      <Brain className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
                      <h3 className="text-white font-semibold mb-2">Bonjour ! Je suis votre expert IA</h3>
                      <p className="text-blue-200 text-sm">
                        Je connais parfaitement la méthode de Philippôt, ses 14 tableaux, 
                        le calcul du Digamma, et toute la théorie "L'univers est au carré".
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <p className="text-blue-300 text-sm mb-3">Suggestions de questions :</p>
                      {suggestions.map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => setInputMessage(suggestion)}
                          className="border-cyan-400/30 text-cyan-300 hover:bg-cyan-400/10 text-xs mx-1 mb-2"
                        >
                          {suggestion}
                        </Button>
                      ))}
                    </div>
                  </div>
                )}
                
                {messages.map((message, index) => (
                  <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : message.type === 'system' ? 'justify-center' : 'justify-start'}`}>
                    <div className={`max-w-[80%] rounded-2xl p-4 ${
                      message.type === 'user' 
                        ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white' 
                        : message.type === 'system'
                        ? 'bg-gradient-to-r from-purple-900/50 to-indigo-900/50 border border-purple-400/30 text-purple-100'
                        : message.extended
                        ? 'bg-gradient-to-r from-emerald-900/30 to-cyan-900/30 border border-emerald-400/30 text-blue-100'
                        : 'bg-white/10 backdrop-blur-sm text-blue-100'
                    }`}>
                      {message.extended && (
                        <div className="flex items-center gap-2 mb-2 text-xs text-emerald-300">
                          <Brain className="w-3 h-3" />
                          <span>Mode enrichi avec contexte personnel</span>
                        </div>
                      )}
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                  </div>
                ))}
                
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-cyan-400"></div>
                        <span className="text-blue-200">L'expert IA analyse votre question...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>
            
            {/* Barre d'outils avec upload */}
            {extendedMode && (
              <div className="border-t border-white/10 p-4">
                <div className="flex items-center gap-4 mb-4">
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-emerald-400/30 text-emerald-300 hover:bg-emerald-400/10"
                      disabled={uploading}
                    >
                      <BookOpen className="w-4 h-4 mr-2" />
                      {uploading ? 'Upload...' : 'Ajouter document'}
                    </Button>
                    <input
                      id="file-upload"
                      type="file"
                      multiple
                      accept=".pdf,.txt,.docx,.png,.jpg,.jpeg"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </label>
                  
                  {uploadedDocuments.length > 0 && (
                    <div className="text-sm text-blue-200">
                      {uploadedDocuments.length} document{uploadedDocuments.length > 1 ? 's' : ''} analysé{uploadedDocuments.length > 1 ? 's' : ''}
                    </div>
                  )}
                </div>

                {/* Liste des documents */}
                {uploadedDocuments.length > 0 && (
                  <div className="bg-slate-800/50 rounded-lg p-3 mb-4 max-h-32 overflow-y-auto">
                    <div className="text-xs text-cyan-300 mb-2">Documents analysés :</div>
                    <div className="space-y-1">
                      {uploadedDocuments.slice(0, 3).map((doc) => (
                        <div key={doc.id} className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            checked={selectedFiles.includes(doc.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedFiles(prev => [...prev, doc.id]);
                              } else {
                                setSelectedFiles(prev => prev.filter(id => id !== doc.id));
                              }
                            }}
                            className="w-3 h-3"
                          />
                          <span className="text-xs text-blue-200 truncate">{doc.filename}</span>
                        </div>
                      ))}
                      {uploadedDocuments.length > 3 && (
                        <div className="text-xs text-blue-300">+{uploadedDocuments.length - 3} autres...</div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="border-t border-white/10 p-6">
              <div className="flex gap-2">
                <Input
                  placeholder={extendedMode ? "Discutons de votre théorie avec contexte enrichi..." : "Posez votre question sur la méthode de Philippôt..."}
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  className="bg-white/10 border-white/20 text-white placeholder:text-blue-200"
                  onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
                  disabled={loading}
                />
                <Button 
                  onClick={sendMessage} 
                  disabled={loading || !inputMessage.trim()}
                  className={`${extendedMode ? 'bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-700 hover:to-cyan-700' : 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700'}`}
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
              
              {selectedFiles.length > 0 && (
                <div className="mt-2 text-xs text-emerald-300">
                  📎 {selectedFiles.length} document{selectedFiles.length > 1 ? 's' : ''} attaché{selectedFiles.length > 1 ? 's' : ''}
                </div>
              )}
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
            <Link to="/methode-philippot" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Méthode Philippôt
            </Link>
            <Link to="/explorer" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Explorer
            </Link>
            <Link to="/chat" className="text-blue-200 hover:text-cyan-400 transition-colors">
              IA Expert
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
          <Route path="/methode-philippot" element={<MethodePhilippotPage />} />
          <Route path="/explorer" element={<ExplorerPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;