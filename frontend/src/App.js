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
import { Search, MessageCircle, BookOpen, Sparkles, Atom, Calculator, Telescope, Send, ArrowRight, Star, Zap, Globe, Brain, Play, Info, TrendingUp, Layers, Target, Edit3, Save, Plus, List, Type, AlignLeft, Bold, Italic, Underline, Menu } from 'lucide-react';

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
                Une théorie personnelle en deux parties : découvrez les trois domaines distincts d'exploration - 
                l'énigme de Riemann, l'intrication quantique et la mécanique du chaos discret.
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

      {/* Section des Trois Domaines Distincts */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-white mb-4">
          Trois Domaines Distincts de la Théorie
        </h2>
        <p className="text-center text-blue-200 mb-12 max-w-4xl mx-auto">
          La théorie "L'univers est au carré" se compose de trois domaines d'étude séparés, 
          chacun explorant des aspects uniques sans connexions forcées.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <Card className="bg-gradient-to-b from-cyan-900/30 to-blue-900/30 border border-cyan-400/30 hover:border-cyan-300 transition-all duration-300 hover:scale-105">
            <CardHeader className="text-center pb-4">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-full flex items-center justify-center">
                <Calculator className="w-8 h-8 text-white" />
              </div>
              <CardTitle className="text-2xl text-cyan-300">Énigme de Riemann</CardTitle>
              <CardDescription className="text-blue-200">
                Analyse numérique métrique des nombres premiers
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <ul className="text-sm text-blue-100 space-y-2 text-left">
                <li>• Représentation en tesseract sur sphère</li>
                <li>• Rapports fractionnels (1/2, 1/3, 1/5)</li>
                <li>• Technique du "moulinet"</li>
                <li>• Concept du Digamma</li>
                <li>• Zéros non triviaux de la fonction Zêta</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-b from-purple-900/30 to-indigo-900/30 border border-purple-400/30 hover:border-purple-300 transition-all duration-300 hover:scale-105">
            <CardHeader className="text-center pb-4">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-purple-400 to-indigo-600 rounded-full flex items-center justify-center">
                <Atom className="w-8 h-8 text-white" />
              </div>
              <CardTitle className="text-2xl text-purple-300">Intrication Quantique</CardTitle>
              <CardDescription className="text-blue-200">
                Théorème de Philippôt et géométrie du "squaring"
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <ul className="text-sm text-blue-100 space-y-2 text-left">
                <li>• Triangles intriqués géométriquement</li>
                <li>• Invariance selon choix d'unité</li>
                <li>• Produit alternatif</li>
                <li>• Rectangles élevés au carré</li>
                <li>• Matrice de longueurs unitaires</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-b from-emerald-900/30 to-teal-900/30 border border-emerald-400/30 hover:border-emerald-300 transition-all duration-300 hover:scale-105">
            <CardHeader className="text-center pb-4">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-emerald-400 to-teal-600 rounded-full flex items-center justify-center">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <CardTitle className="text-2xl text-emerald-300">Chaos Discret</CardTitle>
              <CardDescription className="text-blue-200">
                Mécanique harmonique et géométrie relationnelle
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <ul className="text-sm text-blue-100 space-y-2 text-left">
                <li>• Géométrie relationnelle</li>
                <li>• Matrice à dérive première</li>
                <li>• Équilibre dynamique</li>
                <li>• Chaons et pression gravito-spectrale</li>
                <li>• Structures auto-organisatrices</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Section Deuxième Partie */}
      <div className="container mx-auto px-6 py-16 bg-gradient-to-r from-slate-800/30 to-purple-900/30">
        <h2 className="text-3xl font-bold text-center text-white mb-4">
          Deuxième Partie : Géométrie du Spectre
        </h2>
        <p className="text-center text-blue-200 mb-12 max-w-4xl mx-auto">
          Exploration des fondements invisibles de l'univers à travers une géométrie singulière 
          issue du spectre des nombres premiers.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-yellow-400/30 transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="text-yellow-300 text-lg">Théorème Principal</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-blue-100">
                <strong>"Trois carrés égale un triangle"</strong>
                <p className="text-xs text-blue-200 mt-2">
                  Ancré dans le théorème de Pythagore, établit une relation fondamentale entre carrés et triangles rectangles.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-yellow-400/30 transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="text-yellow-300 text-lg">Innovations Métriques</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-blue-100">
                <strong>Longueur de Philippôt</strong>
                <p className="text-xs text-blue-200 mt-2">
                  Inspirée de la longueur de Planck, liée à la position du Soleil selon la perspective théorique.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-yellow-400/30 transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="text-yellow-300 text-lg">Cercle Denis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-blue-100">
                <strong>Diamètre 1, Circonférence ≈ 4</strong>
                <p className="text-xs text-blue-200 mt-2">
                  Relie constantes physiques (pression atmosphérique) aux formes géométriques.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-yellow-400/30 transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="text-yellow-300 text-lg">√10 comme π</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-blue-100">
                <strong>Nouvelle approximation</strong>
                <p className="text-xs text-blue-200 mt-2">
                  √10 remplace π car il représente mieux le volume et la surface d'un espace selon Philippôt.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Section Catégories */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-white mb-12">
          Navigation par domaines
        </h2>
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
    setSessionId(currentSessionId);

    try {
      for (const file of files) {
        console.log(`Uploading file: ${file.name}`);
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', currentSessionId);

        const response = await axios.post(`${API_URL}/api/upload-document`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (response.data && response.data.success) {
          const analysisMessage = {
            type: 'system',
            content: `📄 Document "${file.name}" téléchargé avec succès !\n\n${response.data.analysis ? `🔍 Analyse : ${response.data.analysis}` : ''}`
          };
          setMessages(prev => [...prev, analysisMessage]);
        } else {
          throw new Error('Upload failed');
        }
      }
      
      // Recharger la liste des documents
      await fetchDocuments();
      
    } catch (error) {
      console.error('Erreur lors de l\'upload:', error);
      const errorMessage = {
        type: 'system',
        content: `❌ Erreur lors du téléchargement. Veuillez réessayer.`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setUploading(false);
      // Réinitialiser l'input
      if (event.target) {
        event.target.value = '';
      }
    }
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
                    <div className={`${extendedMode ? 'bg-gradient-to-r from-emerald-500/20 to-cyan-600/20 border border-emerald-400/30' : 'bg-gradient-to-r from-cyan-500/20 to-blue-600/20'} rounded-2xl p-6 max-w-md mx-auto mb-6`}>
                      <Brain className={`w-12 h-12 ${extendedMode ? 'text-emerald-400' : 'text-cyan-400'} mx-auto mb-4`} />
                      <h3 className="text-white font-semibold mb-2">
                        {extendedMode ? 'Bonjour Philippe ! Votre assistant personnel' : 'Bonjour ! Je suis votre expert IA'}
                      </h3>
                      <p className="text-blue-200 text-sm">
                        {extendedMode 
                          ? 'Mode enrichi activé : je me souviens de nos discussions, analyse vos documents, et adapte mes réponses à votre style de raisonnement unique.'
                          : 'Je connais parfaitement la méthode de Philippôt, ses 14 tableaux, le calcul du Digamma, et toute la théorie "L\'univers est au carré".'
                        }
                      </p>
                      
                      {extendedMode && (
                        <div className="mt-4 text-xs text-emerald-300">
                          🧠 Contexte personnel actif • 📚 {uploadedDocuments.length} documents analysés • 💭 Mémoire étendue
                        </div>
                      )}
                    </div>
                    
                    <div className="space-y-2">
                      <p className="text-blue-300 text-sm mb-3">
                        {extendedMode ? 'Questions adaptées à votre recherche :' : 'Suggestions de questions :'}
                      </p>
                      {(extendedMode ? [
                        "Analysons cette nouvelle idée que j'ai développée...",
                        "Que penses-tu de cette connexion avec mes travaux précédents ?",
                        "Comment puis-je approfondir cette piste de recherche ?",
                        "Aide-moi à structurer cette nouvelle approche",
                        "Quelles implications cela a-t-il pour ma théorie globale ?"
                      ] : suggestions).map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => setInputMessage(suggestion)}
                          className={`${extendedMode ? 'border-emerald-400/30 text-emerald-300 hover:bg-emerald-400/10' : 'border-cyan-400/30 text-cyan-300 hover:bg-cyan-400/10'} text-xs mx-1 mb-2`}
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
                  <div className="relative">
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-emerald-400/30 text-emerald-300 hover:bg-emerald-400/10"
                      disabled={uploading}
                      onClick={() => document.getElementById('file-upload').click()}
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
                      style={{ display: 'none' }}
                    />
                  </div>
                  
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

// Page Concepts Enrichis
const ConceptsEnrichisPage = () => {
  const [concepts, setConcepts] = useState([]);
  const [domaines, setDomaines] = useState([]);
  const [domaineSelectionne, setDomaineSelectionne] = useState('');
  const [conceptSelectionne, setConceptSelectionne] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConcepts();
  }, []);

  const loadConcepts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/concepts-enrichis`);
      if (response.data.success) {
        setConcepts(response.data.concepts);
        setDomaines(response.data.domaines);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des concepts:', error);
    } finally {
      setLoading(false);
    }
  };

  const conceptsFiltres = domaineSelectionne 
    ? concepts.filter(c => c.domaine_principal === domaineSelectionne)
    : concepts;

  const handleConceptSelect = (concept) => {
    setConceptSelectionne(concept);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4 flex items-center gap-2">
            <Brain className="w-8 h-8 text-cyan-400" />
            Concepts Théoriques Enrichis
          </h1>
          <p className="text-blue-200 text-lg">
            Exploration approfondie de la deuxième partie de "L'univers est au carré" - Concepts séparés par domaines théoriques.
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400"></div>
            <span className="ml-2 text-white">Chargement des concepts...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Sidebar - Filtres par domaine */}
            <Card className="bg-white/5 backdrop-blur-sm border border-white/10 lg:col-span-1">
              <CardHeader>
                <CardTitle className="text-white text-lg">Domaines Théoriques</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Button
                    onClick={() => setDomaineSelectionne('')}
                    variant={domaineSelectionne === '' ? "default" : "ghost"}
                    className={`w-full justify-start ${domaineSelectionne === '' 
                      ? 'bg-cyan-600 hover:bg-cyan-700' 
                      : 'text-blue-200 hover:bg-white/10'}`}
                  >
                    Tous les domaines ({concepts.length})
                  </Button>
                  {domaines.map((domaine) => (
                    <Button
                      key={domaine}
                      onClick={() => setDomaineSelectionne(domaine)}
                      variant={domaineSelectionne === domaine ? "default" : "ghost"}
                      className={`w-full justify-start text-sm ${domaineSelectionne === domaine 
                        ? 'bg-cyan-600 hover:bg-cyan-700' 
                        : 'text-blue-200 hover:bg-white/10'}`}
                    >
                      {domaine} ({concepts.filter(c => c.domaine_principal === domaine).length})
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Zone principale - Liste des concepts */}
            <div className="lg:col-span-3">
              {conceptSelectionne ? (
                // Vue détaillée d'un concept
                <Card className="bg-white/5 backdrop-blur-sm border border-white/10">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="text-white text-2xl">{conceptSelectionne.titre}</CardTitle>
                        <Badge className="mt-2 bg-gradient-to-r from-purple-600 to-indigo-600">
                          {conceptSelectionne.domaine_principal}
                        </Badge>
                      </div>
                      <Button
                        onClick={() => setConceptSelectionne(null)}
                        variant="ghost"
                        className="text-blue-200 hover:bg-white/10"
                      >
                        ← Retour
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div>
                      <h3 className="text-lg font-semibold text-cyan-400 mb-2">Description</h3>
                      <p className="text-blue-100">{conceptSelectionne.description}</p>
                    </div>

                    {conceptSelectionne.concepts_cles.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-cyan-400 mb-2">Concepts Clés</h3>
                        <div className="flex flex-wrap gap-2">
                          {conceptSelectionne.concepts_cles.map((concept, index) => (
                            <Badge key={index} variant="secondary" className="bg-slate-700 text-blue-200">
                              {concept}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {conceptSelectionne.formules.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-cyan-400 mb-2">Formules Importantes</h3>
                        <div className="bg-slate-800/50 p-4 rounded-lg">
                          {conceptSelectionne.formules.map((formule, index) => (
                            <div key={index} className="text-blue-100 font-mono text-sm mb-2">
                              • {formule}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {conceptSelectionne.definitions.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-cyan-400 mb-2">Définitions</h3>
                        <div className="space-y-2">
                          {conceptSelectionne.definitions.map((definition, index) => (
                            <div key={index} className="bg-indigo-900/30 p-3 rounded border-l-4 border-cyan-400">
                              <p className="text-blue-100">{definition}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {conceptSelectionne.relations.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-cyan-400 mb-2">Relations Théoriques</h3>
                        <ul className="space-y-1">
                          {conceptSelectionne.relations.map((relation, index) => (
                            <li key={index} className="text-blue-100 flex items-center">
                              <ArrowRight className="w-4 h-4 text-cyan-400 mr-2" />
                              {relation}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="border-t border-white/10 pt-4">
                      <p className="text-sm text-blue-300">
                        <strong>Source:</strong> {conceptSelectionne.document_source} - {conceptSelectionne.page_reference}
                      </p>
                      <p className="text-sm text-blue-300">
                        <strong>Niveau:</strong> {conceptSelectionne.niveau_complexite}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                // Vue grille des concepts
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-white">
                      {domaineSelectionne || 'Tous les concepts'} ({conceptsFiltres.length})
                    </h2>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {conceptsFiltres.map((concept) => (
                      <Card
                        key={concept.id}
                        className="bg-white/5 backdrop-blur-sm border border-white/10 hover:border-cyan-400/30 transition-all cursor-pointer card-hover"
                        onClick={() => handleConceptSelect(concept)}
                      >
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-white text-lg">{concept.titre}</CardTitle>
                            <Badge 
                              className={`text-xs ${
                                concept.niveau_complexite === 'fondamental' ? 'bg-green-600' :
                                concept.niveau_complexite === 'intermediaire' ? 'bg-yellow-600' :
                                'bg-red-600'
                              }`}
                            >
                              {concept.niveau_complexite}
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <p className="text-blue-200 text-sm mb-3 line-clamp-3">
                            {concept.description}
                          </p>
                          
                          <div className="space-y-2">
                            <div>
                              <span className="text-xs text-cyan-400 font-medium">Domaine:</span>
                              <Badge variant="secondary" className="ml-2 text-xs bg-slate-700 text-blue-200">
                                {concept.domaine_principal}
                              </Badge>
                            </div>
                            
                            <div>
                              <span className="text-xs text-cyan-400 font-medium">Concepts:</span>
                              <span className="text-xs text-blue-300 ml-2">
                                {concept.concepts_cles.slice(0, 2).join(', ')}
                                {concept.concepts_cles.length > 2 && '...'}
                              </span>
                            </div>
                          </div>
                          
                          <div className="flex items-center justify-between mt-4">
                            <span className="text-xs text-blue-400">{concept.page_reference}</span>
                            <ArrowRight className="w-4 h-4 text-cyan-400" />
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Navigation
const Navigation = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <nav className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <span className="text-white font-bold text-lg hidden sm:inline">L'univers est au carré</span>
            <span className="text-white font-bold text-sm sm:hidden">L'univers²</span>
          </Link>
          
          {/* Navigation desktop */}
          <div className="hidden lg:flex items-center gap-6">
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
            <Link to="/collaboration" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Collaboration
            </Link>
            <Link to="/concepts-enrichis" className="text-blue-200 hover:text-cyan-400 transition-colors">
              Concepts Enrichis
            </Link>
          </div>

          {/* Navigation mobile compacte */}
          <div className="lg:hidden flex items-center gap-2">
            <Link to="/chat" className="text-blue-200 hover:text-cyan-400 transition-colors text-sm px-2">
              IA
            </Link>
            <Link to="/collaboration" className="text-blue-200 hover:text-cyan-400 transition-colors text-sm px-2">
              Collab
            </Link>
            <button 
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-blue-200 hover:text-cyan-400 transition-colors p-1"
            >
              <Menu className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Menu mobile déroulant */}
        {isMobileMenuOpen && (
          <div className="lg:hidden bg-black/30 backdrop-blur-sm border-t border-white/10 py-4">
            <div className="flex flex-col space-y-2">
              <Link 
                to="/" 
                className="text-blue-200 hover:text-cyan-400 transition-colors px-4 py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Accueil
              </Link>
              <Link 
                to="/methode-philippot" 
                className="text-blue-200 hover:text-cyan-400 transition-colors px-4 py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Méthode Philippôt
              </Link>
              <Link 
                to="/explorer" 
                className="text-blue-200 hover:text-cyan-400 transition-colors px-4 py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Explorer
              </Link>
              <Link 
                to="/chat" 
                className="text-blue-200 hover:text-cyan-400 transition-colors px-4 py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                IA Expert
              </Link>
              <Link 
                to="/collaboration" 
                className="text-blue-200 hover:text-cyan-400 transition-colors px-4 py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Collaboration
              </Link>
              <Link 
                to="/concepts-enrichis" 
                className="text-blue-200 hover:text-cyan-400 transition-colors px-4 py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Concepts Enrichis
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

// Symboles mathématiques pour l'éditeur
const SYMBOLES_MATHEMATIQUES = {
  'Grec': ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'λ', 'μ', 'π', 'ρ', 'σ', 'τ', 'φ', 'χ', 'ψ', 'ω', 'Γ', 'Δ', 'Θ', 'Λ', 'Π', 'Σ', 'Φ', 'Ψ', 'Ω'],
  'Racines': ['√', '∛', '∜', '√²', '√³', '√ⁿ'],
  'Opérateurs': ['±', '∓', '×', '÷', '∞', '∑', '∏', '∫', '∂', '∇', '≈', '≠', '≤', '≥', '≡', '∝', '∈', '∉', '⊂', '⊆', '∪', '∩'],
  'Exposants': ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', 'ⁿ', '⁻¹', '⁻²'],
  'Indices': ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉', 'ₙ', 'ₓ', 'ᵢ'],
  'Géométrie': ['°', '∠', '⊥', '∥', '△', '□', '◯', '⌒', '⌓'],
  'Ensembles': ['ℕ', 'ℤ', 'ℚ', 'ℝ', 'ℂ', '∅', '∀', '∃', '∄']
};

// Page Collaboration avec interface à 3 zones
const CollaborationPage = () => {
  // États pour la zone d'édition/création
  const [document, setDocument] = useState('');
  const [documentTitle, setDocumentTitle] = useState('Nouveau Document');
  const [currentDocId, setCurrentDocId] = useState(null);
  const [savedDocuments, setSavedDocuments] = useState([]);
  const [saveStatus, setSaveStatus] = useState('');
  const [showSymbols, setShowSymbols] = useState(false);
  const [selectedSymbolCategory, setSelectedSymbolCategory] = useState('Grec');
  const [showLatex, setShowLatex] = useState(false);
  const [latexContent, setLatexContent] = useState('');
  
  // États pour la zone chatbot
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isChatLoading, setIsChatLoading] = useState(false);
  
  // États généraux
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const newSessionId = `collab_${Date.now()}`;
    setSessionId(newSessionId);
    loadSavedDocuments();
  }, []);

  const loadSavedDocuments = async () => {
    try {
      if (sessionId) {
        const response = await axios.get(`${API_URL}/api/collaboration-documents/${sessionId}`);
        if (response.data && Array.isArray(response.data)) {
          setSavedDocuments(response.data.map(doc => ({
            id: doc.id,
            title: doc.title,
            date: doc.updated_at || doc.created_at,
            content: doc.content
          })));
        } else {
          // Documents par défaut si aucun document sauvegardé
          setSavedDocuments([]);
        }
      }
    } catch (error) {
      console.error('Erreur lors du chargement des documents:', error);
      // En cas d'erreur, garder des documents par défaut
      setSavedDocuments([
        { id: 'default-1', title: 'Nouveau document', date: new Date().toISOString() }
      ]);
    }
  };

  const insertText = (before, after = '') => {
    try {
      const textarea = window.document.querySelector('#collaboration-editor');
      if (!textarea) return;
      
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selectedText = document.substring(start, end);
      const newText = document.substring(0, start) + before + selectedText + after + document.substring(end);
      setDocument(newText);
      
      // Repositionner le curseur
      setTimeout(() => {
        if (textarea) {
          textarea.focus();
          textarea.setSelectionRange(start + before.length, start + before.length + selectedText.length);
        }
      }, 100);
    } catch (error) {
      console.warn('Erreur insertText:', error);
    }
  };

  const insertSymbol = (symbol) => {
    insertText(symbol);
    // Garder le focus sur le textarea après insertion
    setTimeout(() => {
      try {
        const textarea = window.document.querySelector('#collaboration-editor');
        if (textarea) {
          textarea.focus();
        }
      } catch (error) {
        console.warn('Erreur focus textarea:', error);
      }
    }, 100);
  };

  const createNewDocument = () => {
    setDocument('');
    setDocumentTitle('Nouveau Document');
    setCurrentDocId(null);
    setSaveStatus('');
    // Focus sur l'éditeur
    setTimeout(() => {
      const textarea = window.document.querySelector('#collaboration-editor');
      if (textarea) {
        textarea.focus();
      }
    }, 100);
  };

  // Fonction pour envoyer un message dans le chatbot
  const sendChatMessage = async () => {
    if (!chatMessage.trim()) return;

    const userMessage = chatMessage;
    setChatMessage('');
    setIsChatLoading(true);

    // Ajouter le message utilisateur à l'historique
    setChatHistory(prev => [...prev, {
      type: 'user',
      content: userMessage,
      timestamp: new Date().toLocaleTimeString()
    }]);

    try {
      const response = await axios.post(`${API_URL}/api/chat-extended`, {
        message: userMessage,
        session_id: sessionId,
        context_mode: 'extended'
      });

      if (response.data.response) {
        // Ajouter la réponse IA à l'historique
        setChatHistory(prev => [...prev, {
          type: 'ai',
          content: response.data.response,
          timestamp: new Date().toLocaleTimeString()
        }]);
      }
    } catch (error) {
      console.error('Erreur chat:', error);
      setChatHistory(prev => [...prev, {
        type: 'error',
        content: 'Erreur lors de la communication avec l\'IA',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  const generateLatex = async () => {
    if (!document.trim()) {
      alert('Aucun contenu à convertir en LaTeX');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/generate-latex`, {
        content: document,
        title: documentTitle,
        session_id: sessionId
      });

      if (response.data.success) {
        setLatexContent(response.data.latex_content);
        setShowLatex(true);
      }
    } catch (error) {
      console.error('Erreur lors de la génération LaTeX:', error);
      alert('Erreur lors de la génération du LaTeX');
    } finally {
      setLoading(false);
    }
  };

  const formatText = (type) => {
    switch (type) {
      case 'bold':
        insertText('**', '**');
        break;
      case 'italic':
        insertText('*', '*');
        break;
      case 'bullet':
        insertText('\n• ');
        break;
      case 'number':
        insertText('\n1. ');
        break;
      case 'heading':
        insertText('\n## ');
        break;
      case 'paragraph':
        insertText('\n\n');
        break;
      default:
        break;
    }
  };

  const collaborateWithAI = async (request) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/collaborate`, {
        document: document,
        request: request,
        session_id: sessionId,
        document_title: documentTitle
      });

      if (response.data.success) {
        setDocument(response.data.updated_document);
        // Notification de succès simple
        console.log('✓ Contenu enrichi par l\'IA');
      } else {
        console.error('Réponse API sans succès:', response.data);
        alert('Erreur: La collaboration IA a échoué');
      }
    } catch (error) {
      console.error('Erreur lors de la collaboration:', error);
      alert(`Erreur de collaboration: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const saveDocument = async () => {
    try {
      setSaveStatus('Sauvegarde...');
      const response = await axios.post(`${API_URL}/api/save-collaboration`, {
        document: document,
        title: documentTitle,
        session_id: sessionId,
        document_id: currentDocId
      });

      if (response.data.success) {
        setCurrentDocId(response.data.document_id);
        await loadSavedDocuments();
        setSaveStatus('✓ Sauvegardé');
        setTimeout(() => setSaveStatus(''), 3000);
      }
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      setSaveStatus('Erreur sauvegarde');
      setTimeout(() => setSaveStatus(''), 3000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-2">
            <Edit3 className="w-7 h-7 text-cyan-400" />
            Espace de Collaboration - L'univers est au carré
          </h1>
          <p className="text-blue-200">
            Trois zones de travail : Chatbot • Création • Affichage des réponses
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-[calc(100vh-180px)]">
          {/* ZONE 1: CHATBOT SIMPLE */}
          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 flex flex-col">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-lg flex items-center gap-2">
                <MessageCircle className="w-5 h-5 text-cyan-400" />
                Chat IA Spécialisée
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col">
              {/* Historique des messages */}
              <div className="flex-1 bg-slate-900/50 rounded-lg p-3 mb-3 overflow-y-auto max-h-80">
                {chatHistory.length === 0 ? (
                  <div className="text-center text-blue-300 text-sm py-8">
                    Posez vos questions sur la théorie "L'univers est au carré"
                  </div>
                ) : (
                  <div className="space-y-3">
                    {chatHistory.map((msg, index) => (
                      <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[85%] rounded-lg p-2 text-sm ${
                          msg.type === 'user' 
                            ? 'bg-cyan-600 text-white' 
                            : msg.type === 'error'
                            ? 'bg-red-600/20 text-red-200 border border-red-500/30'
                            : 'bg-indigo-600/30 text-blue-100 border border-indigo-500/30'
                        }`}>
                          <div className="whitespace-pre-wrap">{msg.content}</div>
                          <div className="text-xs opacity-70 mt-1">{msg.timestamp}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {isChatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-indigo-600/30 text-blue-100 border border-indigo-500/30 rounded-lg p-2 text-sm">
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-cyan-400"></div>
                        L'IA réfléchit...
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Zone de saisie du chat */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !isChatLoading && sendChatMessage()}
                  placeholder="Posez votre question..."
                  className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:border-cyan-400 focus:outline-none"
                  disabled={isChatLoading}
                />
                <Button
                  onClick={sendChatMessage}
                  disabled={isChatLoading || !chatMessage.trim()}
                  className="bg-cyan-600 hover:bg-cyan-700 px-4"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* ZONE 2: CRÉATION ET ÉDITION */}
          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 flex flex-col">
            <CardHeader className="border-b border-white/10 pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Edit3 className="w-5 h-5 text-cyan-400" />
                  <span className="text-white text-lg font-semibold">Création & Édition</span>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    onClick={createNewDocument}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Nouveau
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col p-4">
              <div className="mb-3">
                <Input
                  value={documentTitle}
                  onChange={(e) => setDocumentTitle(e.target.value)}
                  className="bg-slate-800 border-slate-600 text-white text-base"
                  placeholder="Titre du document..."
                />
              </div>
              
              <textarea
                id="collaboration-editor"
                value={document}
                onChange={(e) => setDocument(e.target.value)}
                placeholder="Commencez à écrire votre document sur la théorie 'L'univers est au carré'..."
                className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm resize-none focus:border-cyan-400 focus:outline-none"
              />
              
              <div className="mt-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Button
                    onClick={() => collaborateWithAI("Complète cette section en développant les idées présentées")}
                    disabled={loading}
                    className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700"
                  >
                    <Brain className="w-4 h-4 mr-2" />
                    IA : Compléter
                  </Button>
                  <Button
                    onClick={() => collaborateWithAI("Améliore la structure et la clarté de ce texte")}
                    disabled={loading}
                    className="bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-700 hover:to-cyan-700"
                  >
                    <Sparkles className="w-4 h-4 mr-2" />
                    IA : Améliorer
                  </Button>
                </div>
                
                <Button
                  onClick={saveDocument}
                  className="bg-emerald-600 hover:bg-emerald-700"
                >
                  <Save className="w-4 h-4 mr-2" />
                  Sauvegarder
                </Button>
              </div>
              
              {saveStatus && (
                <div className="mt-2 text-sm text-emerald-400">{saveStatus}</div>
              )}
            </CardContent>
          </Card>

          {/* ZONE 3: AFFICHAGE ET HISTORIQUE */}
          <Card className="bg-white/5 backdrop-blur-sm border border-white/10 flex flex-col">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-lg flex items-center gap-2">
                <List className="w-5 h-5 text-cyan-400" />
                Documents & Historique
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col">
              <div className="text-center text-blue-300 text-sm py-8">
                Historique des collaborations avec l'IA
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Modal LaTeX (si nécessaire) */}
        {showLatex && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <Card className="bg-white/5 backdrop-blur-sm border border-white/10 max-w-4xl max-h-[90vh] overflow-hidden">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white text-2xl">Version LaTeX Générée</CardTitle>
                  <Button
                    onClick={() => setShowLatex(false)}
                    variant="ghost"
                    className="text-blue-200 hover:bg-white/10"
                  >
                    ✕
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-slate-900/50 border border-slate-600 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap">
                    {latexContent}
                  </pre>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};
              <div className="border-b border-white/10 p-4">
                <div className="flex flex-wrap items-center gap-2">
                  <div className="flex items-center gap-1 border-r border-white/20 pr-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('bold')}
                      className="text-white hover:bg-white/10"
                    >
                      <Bold className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('italic')}
                      className="text-white hover:bg-white/10"
                    >
                      <Italic className="w-4 h-4" />
                    </Button>
                  </div>

                  <div className="flex items-center gap-1 border-r border-white/20 pr-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('heading')}
                      className="text-white hover:bg-white/10"
                    >
                      <Type className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('paragraph')}
                      className="text-white hover:bg-white/10"
                    >
                      <AlignLeft className="w-4 h-4" />
                    </Button>
                  </div>

                  <div className="flex items-center gap-1 border-r border-white/20 pr-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('bullet')}
                      className="text-white hover:bg-white/10"
                    >
                      <List className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('number')}
                      className="text-white hover:bg-white/10"
                    >
                      1.
                    </Button>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button
                      onClick={() => setShowSymbols(!showSymbols)}
                      variant="ghost"
                      className="text-white hover:bg-white/10"
                    >
                      ∑ Symboles
                    </Button>
                    
                    <div className="border-r border-white/20 h-6"></div>
                    
                    <Button
                      onClick={() => collaborateWithAI("Complète cette section en développant les idées présentées")}
                      disabled={loading}
                      className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700"
                    >
                      <Brain className="w-4 h-4 mr-2" />
                      IA : Compléter
                    </Button>
                    <Button
                      onClick={() => collaborateWithAI("Améliore la structure et la clarté de ce texte")}
                      disabled={loading}
                      className="bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-700 hover:to-cyan-700"
                    >
                      <Sparkles className="w-4 h-4 mr-2" />
                      IA : Améliorer
                    </Button>
                    
                    <div className="border-r border-white/20 h-6"></div>
                    
                    <Button
                      onClick={generateLatex}
                      disabled={loading}
                      className="bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700"
                    >
                      <Calculator className="w-4 h-4 mr-2" />
                      IA : LaTeX
                    </Button>
                  </div>
                </div>
              </div>

              {/* Palette de symboles mathématiques */}
              {showSymbols && (
                <div className="border-b border-white/10 p-4 bg-slate-800/30">
                  <div className="mb-3">
                    <span className="text-white text-sm font-medium mr-3">Catégories :</span>
                    {Object.keys(SYMBOLES_MATHEMATIQUES).map((category) => (
                      <Button
                        key={category}
                        onClick={() => setSelectedSymbolCategory(category)}
                        variant={selectedSymbolCategory === category ? "default" : "ghost"}
                        size="sm"
                        className={`mr-2 text-xs ${
                          selectedSymbolCategory === category 
                            ? 'bg-cyan-600 hover:bg-cyan-700' 
                            : 'text-blue-200 hover:bg-white/10'
                        }`}
                      >
                        {category}
                      </Button>
                    ))}
                  </div>
                  
                  <div className="flex flex-wrap gap-1">
                    {SYMBOLES_MATHEMATIQUES[selectedSymbolCategory].map((symbol, index) => (
                      <Button
                        key={index}
                        onClick={() => insertSymbol(symbol)}
                        variant="ghost"
                        size="sm"
                        className="text-white hover:bg-cyan-600/30 min-w-[2.5rem] h-8 text-base font-mono"
                        title={`Insérer ${symbol}`}
                      >
                        {symbol}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {/* Zone d'édition */}
              <CardContent className="p-0">
                <textarea
                  id="collaboration-editor"
                  value={document}
                  onChange={(e) => setDocument(e.target.value)}
                  placeholder="Commencez à écrire vos idées ici... L'IA peut vous aider à les développer et les structurer.

Exemples d'utilisation :
• Rédigez une idée de base
• Utilisez les boutons IA pour la faire développer
• Ajoutez votre propre contenu
• Collaborez de manière itérative

## Nouvelle section
Votre contenu ici...

1. Premier point
2. Deuxième point"
                  className="w-full h-96 bg-transparent text-white p-6 border-none resize-none focus:outline-none focus:ring-2 focus:ring-cyan-400 font-mono text-sm leading-relaxed"
                  disabled={loading}
                />
              </CardContent>

              {/* Barre de statut */}
              <div className="border-t border-white/10 p-4">
                <div className="flex items-center justify-between text-sm text-blue-300">
                  <div>
                    {document.length} caractères • {document.split(/\s+/).filter(word => word.length > 0).length} mots
                  </div>
                  <div className="flex items-center gap-4">
                    {loading && (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-cyan-400"></div>
                        <span>L'IA collabore...</span>
                      </div>
                    )}
                    <div className="text-xs">
                      Session: {sessionId?.slice(-8)}
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Modal LaTeX */}
        {showLatex && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <Card className="bg-white/5 backdrop-blur-sm border border-white/10 max-w-4xl max-h-[90vh] overflow-hidden">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white text-2xl">Version LaTeX Générée</CardTitle>
                  <Button
                    onClick={() => setShowLatex(false)}
                    variant="ghost"
                    className="text-blue-200 hover:bg-white/10"
                  >
                    ✕
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-cyan-400 font-medium">Document : {documentTitle}</span>
                  <Button
                    onClick={() => navigator.clipboard.writeText(latexContent)}
                    className="bg-cyan-600 hover:bg-cyan-700"
                  >
                    📋 Copier LaTeX
                  </Button>
                </div>
                
                <div className="bg-slate-900/50 border border-slate-600 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap">
                    {latexContent}
                  </pre>
                </div>
                
                <div className="text-sm text-blue-300 space-y-1">
                  <p>• Le code LaTeX a été généré automatiquement par l'IA spécialisée</p>
                  <p>• Vous pouvez copier ce code et l'utiliser dans votre éditeur LaTeX préféré</p>
                  <p>• Les formules mathématiques et symboles ont été convertis automatiquement</p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
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
          <Route path="/collaboration" element={<CollaborationPage />} />
          <Route path="/concepts-enrichis" element={<ConceptsEnrichisPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;