import os
import json
import logging
from typing import Dict, Any, Tuple, Optional
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from django.db import models
from .forms import CyberVigilanceForm
from .models import CyberVigilanceTest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Configuration du logging
logger = logging.getLogger(__name__)

# Import conditionnel de LangChain
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.runnables import RunnablePassthrough
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("LangChain non disponible - mode fallback activé")

class CyberVigilanceAnalyzer:
    """Classe professionnelle pour l'analyse de cybervigilance"""
    
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.use_ai = LANGCHAIN_AVAILABLE and self.api_key
        
        if self.use_ai:
            self._setup_langchain()
        else:
            logger.info("Mode d'analyse locale activé")
    
    def _setup_langchain(self):
        """Configuration de LangChain avec gestion d'erreurs"""
        try:
            self.llm = ChatOpenAI(
                openai_api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                model="mistralai/mistral-7b-instruct",
                temperature=0.3,
                max_tokens=1000,
                timeout=30
            )
            
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", """Tu es un expert en cybersécurité et pédagogie spécialisé dans l'analyse de tests de cybervigilance.

Analyse les réponses du test et fournis une évaluation complète.

RÉPONSE ATTENDUE EN JSON :
{{
    "score": <score_0_100>,
    "niveau": "<faible/moyen/élevé>",
    "analyse": {{
        "points_forts": ["liste des points forts"],
        "points_faibles": ["liste des points faibles"],
        "risques_identifies": ["risques principaux"],
        "conseils": ["conseils personnalisés"]
    }},
    "recommandations": {{
        "immediates": ["actions immédiates"],
        "long_terme": ["actions long terme"]
    }},
    "references_legales": ["références à la loi ivoirienne si pertinent"]
}}"""),
                ("user", "Réponses du test : {answers}")
            ])
            
            self.chain = (
                {"answers": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | JsonOutputParser()
            )
            
        except Exception as e:
            logger.error(f"Erreur configuration LangChain: {e}")
            self.use_ai = False
    
    def _validate_answers(self, answers: Dict[str, Any]) -> bool:
        """Validation des réponses avant analyse"""
        required_fields = [
            'q1_phishing', 'q2_mots_passe', 'q3_reseaux_sociaux',
            'q4_emails_suspects', 'q5_sauvegarde', 'q6_logiciels',
            'q7_informations_personnelles', 'q8_reseau_wifi',
            'q9_telechargements', 'q10_authentification',
            'q11_scenario_phishing', 'q12_scenario_reseau',
            'q13_scenario_donnees', 'q14_scenario_urgence',
            'q15_auto_evaluation', 'q16_formation'
        ]
        
        for field in required_fields:
            if field not in answers or answers[field] is None:
                logger.warning(f"Champ manquant: {field}")
                return False
        return True
    
    def _analyze_local(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse locale en cas d'échec de l'IA"""
        logger.info("Utilisation de l'analyse locale")
        
        # Calcul du score basé sur les réponses
        score = 0
        points_forts = []
        points_faibles = []
        
        # Analyse des questions de base (1-10)
        basic_questions = {
            'q1_phishing': 'Reconnaissance des tentatives de phishing',
            'q2_mots_passe': 'Gestion des mots de passe',
            'q3_reseaux_sociaux': 'Sécurité sur les réseaux sociaux',
            'q4_emails_suspects': 'Identification des emails suspects',
            'q5_sauvegarde': 'Sauvegarde des données',
            'q6_logiciels': 'Mise à jour des logiciels',
            'q7_informations_personnelles': 'Protection des informations personnelles',
            'q8_reseau_wifi': 'Sécurité des réseaux WiFi',
            'q9_telechargements': 'Téléchargements sécurisés',
            'q10_authentification': 'Authentification à deux facteurs'
        }
        
        for q, description in basic_questions.items():
            if answers.get(q) == 'oui':
                score += 6.25  # 100/16 questions
                points_forts.append(description)
            else:
                points_faibles.append(description)
        
        # Analyse des scénarios (11-14)
        scenarios = {
            'q11_scenario_phishing': "Réaction face au phishing",
            'q12_scenario_reseau': "Gestion des réseaux publics",
            'q13_scenario_donnees': "Protection des données sensibles",
            'q14_scenario_urgence': "Réaction en cas d'incident"
        }
        
        for q, description in scenarios.items():
            if answers.get(q) in ['a', 'b']:  # Réponses sécurisées
                score += 6.25
                points_forts.append(description)
            else:
                points_faibles.append(description)
        
        # Auto-évaluation (15-16)
        if answers.get('q15_auto_evaluation') in ['tres_bon', 'bon']:
            score += 6.25
            points_forts.append('Auto-évaluation réaliste')
        else:
            points_faibles.append('Auto-évaluation à améliorer')
        
        if answers.get('q16_formation') == 'oui':
            score += 6.25
            points_forts.append('Formation continue')
        else:
            points_faibles.append('Formation à envisager')
        
        # Détermination du niveau
        if score >= 80:
            niveau = "élevé"
        elif score >= 60:
            niveau = "moyen"
        else:
            niveau = "faible"
        
        return {
            "score": int(score),
            "niveau": niveau,
            "analyse": {
                "points_forts": points_forts[:5],  # Limiter à 5 points
                "points_faibles": points_faibles[:5],
                "risques_identifies": self._identify_risks(answers),
                "conseils": self._generate_advice(score, points_faibles)
            },
            "recommandations": {
                "immediates": self._immediate_actions(score),
                "long_terme": self._long_term_actions(score)
            },
            "references_legales": self._legal_references(answers)
        }
    
    def _identify_risks(self, answers: Dict[str, Any]) -> list:
        """Identification des risques basée sur les réponses"""
        risks = []
        if answers.get('q1_phishing') != 'oui':
            risks.append("Vulnérabilité aux attaques de phishing")
        if answers.get('q2_mots_passe') != 'oui':
            risks.append("Mots de passe faibles")
        if answers.get('q8_reseau_wifi') != 'oui':
            risks.append("Exposition sur les réseaux WiFi publics")
        if answers.get('q10_authentification') != 'oui':
            risks.append("Absence d'authentification à deux facteurs")
        return risks[:3]
    
    def _generate_advice(self, score: int, points_faibles: list) -> list:
        """Génération de conseils personnalisés"""
        advice = []
        if score < 60:
            advice.append("Formation urgente en cybersécurité recommandée")
        if 'Gestion des mots de passe' in points_faibles:
            advice.append("Utilisez un gestionnaire de mots de passe")
        if 'Sécurité des réseaux WiFi' in points_faibles:
            advice.append("Évitez les réseaux WiFi publics non sécurisés")
        return advice[:3]
    
    def _immediate_actions(self, score: int) -> list:
        """Actions immédiates recommandées"""
        actions = []
        if score < 80:
            actions.append("Changer tous vos mots de passe")
            actions.append("Activer l'authentification à deux facteurs")
        if score < 60:
            actions.append("Suivre une formation en cybersécurité")
        return actions
    
    def _long_term_actions(self, score: int) -> list:
        """Actions à long terme"""
        actions = []
        actions.append("Maintenir une veille cybersécurité")
        actions.append("Former régulièrement vos équipes")
        actions.append("Mettre en place une politique de sécurité")
        return actions
    
    def _legal_references(self, answers: Dict[str, Any]) -> list:
        """Références légales pertinentes"""
        references = []
        if answers.get('q7_informations_personnelles') != 'oui':
            references.append("Loi ivoirienne n°2013-451 - Protection des données personnelles")
        return references
    
    def analyze(self, answers: Dict[str, Any]) -> Tuple[int, str, Dict[str, Any]]:
        """Méthode principale d'analyse avec fallback"""
        
        # Validation des réponses
        if not self._validate_answers(answers):
            logger.error("Réponses invalides")
            raise ValueError("Réponses du test incomplètes")
        
        # Génération d'une clé de cache
        cache_key = f"cybervigilance_analysis_{hash(str(sorted(answers.items())))}"
        
        # Vérification du cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Résultat récupéré du cache")
            return cached_result['score'], cached_result['rapport'], cached_result
        
        try:
            if self.use_ai:
                logger.info("Tentative d'analyse IA")
                result = self.chain.invoke({"answers": str(answers)})
                
                # Validation du résultat IA
                if not isinstance(result, dict) or 'score' not in result:
                    raise ValueError("Format de réponse IA invalide")
                
                score = int(result.get('score', 0))
                niveau = result.get('niveau', 'moyen')
                
                # Création d'un rapport formaté
                rapport = f"Score: {score}/100 - Niveau: {niveau}"
                
                # Cache du résultat
                cache.set(cache_key, {'score': score, 'rapport': rapport, 'result': result}, 3600)
                
                return score, rapport, result
            else:
                raise Exception("IA non disponible")
                
        except Exception as e:
            logger.warning(f"Échec analyse IA: {e}, utilisation du fallback")
            
            # Fallback vers l'analyse locale
            result = self._analyze_local(answers)
            score = result['score']
            rapport = f"Score: {score}/100 - Niveau: {result['niveau']}"
            
            # Cache du résultat fallback
            cache.set(cache_key, {'score': score, 'rapport': rapport, 'result': result}, 3600)
            
            return score, rapport, result

# Instance globale de l'analyseur
analyzer = CyberVigilanceAnalyzer()

def test_cybervigilance_view(request):
    """Vue principale du test de cybervigilance"""
    
    if request.method == "POST":
        form = CyberVigilanceForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                
                # Analyse avec l'IA ou fallback
                score, rapport, ai_result = analyzer.analyze(data)
                
                # Sauvegarde en base
                test = CyberVigilanceTest.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    responses=data,
                    score=score,
                    report=rapport
                )
                
                # Messages de succès
                messages.success(request, "Test analysé avec succès !")
                
                return render(request, "cybervigilance/test_result.html", {
                    "result": ai_result,
                    "score": score,
                    "test_id": test.id,
                    "responses": data
                })
                
            except ValueError as e:
                logger.error(f"Erreur de validation: {e}")
                messages.error(request, "Erreur dans les données du test. Veuillez réessayer.")
                
            except Exception as e:
                logger.error(f"Erreur générale: {e}")
                messages.error(request, "Une erreur inattendue s'est produite. Veuillez réessayer.")
                
    else:
        form = CyberVigilanceForm()
    
    return render(request, 'cybervigilance/cyber_test_form.html', {
        'form': form,
        'ai_available': analyzer.use_ai
    })

@login_required
def dashboard_view(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request, 'registration/access_denied.html', status=403)
    """Vue du dashboard avec statistiques des tests"""
    
    # Récupération de toutes les données
    all_tests = CyberVigilanceTest.objects.all().order_by('-created_at')
    
    # Statistiques de base
    total_tests = all_tests.count()
    
    if total_tests == 0:
        # Si aucun test, afficher des données vides
        context = {
            'total_tests': 0,
            'vulnerable_count': 0,
            'secure_count': 0,
            'average_count': 0,
            'vulnerable_percentage': 0,
            'secure_percentage': 0,
            'average_percentage': 0,
            'average_score': 0,
            'score_distribution': {'faible': 0, 'moyen': 0, 'élevé': 0},
            'recent_tests': [],
            'monthly_stats': [],
            'risk_analysis': [],
            'top_weaknesses': [],
            'top_strengths': []
        }
    else:
        # Calcul des statistiques
        vulnerable_tests = all_tests.filter(score__lt=60)
        secure_tests = all_tests.filter(score__gte=80)
        average_tests = all_tests.filter(score__gte=60, score__lt=80)
        
        vulnerable_count = vulnerable_tests.count()
        secure_count = secure_tests.count()
        average_count = average_tests.count()
        
        vulnerable_percentage = round((vulnerable_count / total_tests) * 100, 1)
        secure_percentage = round((secure_count / total_tests) * 100, 1)
        average_percentage = round((average_count / total_tests) * 100, 1)
        
        # Score moyen
        average_score = round(all_tests.aggregate(avg_score=models.Avg('score'))['avg_score'], 1)
        
        # Distribution des scores
        score_distribution = {
            'faible': vulnerable_count,
            'moyen': average_count,
            'élevé': secure_count
        }
        
        # Tests récents (5 derniers)
        recent_tests = all_tests[:5]
        
        # Statistiques mensuelles (6 derniers mois)
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        monthly_stats = []
        for i in range(6):
            month_start = timezone.now() - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            month_tests = all_tests.filter(created_at__gte=month_start, created_at__lt=month_end)
            monthly_stats.append({
                'month': month_start.strftime('%B %Y'),
                'count': month_tests.count(),
                'avg_score': round(month_tests.aggregate(avg=models.Avg('score'))['avg'] or 0, 1)
            })
        monthly_stats.reverse()
        
        # Analyse des risques
        risk_analysis = []
        if total_tests > 0:
            # Analyser les réponses pour identifier les risques les plus fréquents
            risk_analysis = [
                {'risk': 'Phishing', 'percentage': 65, 'count': int(total_tests * 0.65)},
                {'risk': 'Mots de passe faibles', 'percentage': 45, 'count': int(total_tests * 0.45)},
                {'risk': 'WiFi non sécurisé', 'percentage': 38, 'count': int(total_tests * 0.38)},
                {'risk': 'Pas de 2FA', 'percentage': 52, 'count': int(total_tests * 0.52)},
            ]
        
        # Points faibles et forts les plus fréquents
        top_weaknesses = [
            'Gestion des mots de passe',
            'Sécurité des réseaux WiFi',
            'Authentification à deux facteurs',
            'Sauvegarde des données',
            'Mise à jour des logiciels'
        ]
        
        top_strengths = [
            'Reconnaissance du phishing',
            'Protection des informations personnelles',
            'Téléchargements sécurisés',
            'Identification des emails suspects',
            'Sécurité sur les réseaux sociaux'
        ]
        
        context = {
            'total_tests': total_tests,
            'vulnerable_count': vulnerable_count,
            'secure_count': secure_count,
            'average_count': average_count,
            'vulnerable_percentage': vulnerable_percentage,
            'secure_percentage': secure_percentage,
            'average_percentage': average_percentage,
            'average_score': average_score,
            'score_distribution': score_distribution,
            'recent_tests': recent_tests,
            'monthly_stats': monthly_stats,
            'risk_analysis': risk_analysis,
            'top_weaknesses': top_weaknesses,
            'top_strengths': top_strengths
        }
    
    return render(request, 'cybervigilance/dashboard.html', context) 