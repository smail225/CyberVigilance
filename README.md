# 🇨🇮 CyberActu — Tester ma cybervigilance

**CyberActu** est une application web interactive de sensibilisation à la cybersécurité, pensée pour la Côte d'Ivoire et la francophonie. Elle permet à tout utilisateur d'évaluer son niveau de cybervigilance, d'obtenir des conseils personnalisés, et à l'administrateur de suivre les statistiques via un dashboard sécurisé.

---

## 🚀 Fonctionnalités principales

- **Test interactif de cybervigilance** (questions, scénarios, auto-évaluation)
- **Analyse intelligente** des réponses (IA ou fallback local)
- **Dashboard administrateur** (statistiques, tendances, points forts/faibles)
- **Design moderne** aux couleurs du drapeau ivoirien 🇨🇮 (orange, blanc, vert)
- **Authentification sécurisée** (accès dashboard réservé à l'admin)
- **Animations CSS élégantes** (fade-in, pulse, transitions)
- **Gestion des utilisateurs via Django admin**

---

## 🛠️ Installation

### Prérequis
- Python 3.11+
- pip
- (Optionnel) virtualenv

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/cyberactu.git
cd cyberactu
```

### 2. Créer et activer un environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Linux/macOS
# ou
env\Scripts\activate   # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirement.txt
```

### 4. Appliquer les migrations
```bash
python manage.py migrate
```

### 5. Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

---

## 💡 Utilisation

- Accédez au test : [http://localhost:8000/cybervigilance/](http://localhost:8000/cybervigilance/)
- Accédez au dashboard (admin uniquement) : [http://localhost:8000/cybervigilance/dashboard/](http://localhost:8000/cybervigilance/dashboard/)
- Accédez à l'admin Django : [http://localhost:8000/admin/](http://localhost:8000/admin/)

> **NB :** Seul l'utilisateur admin (is_staff ou is_superuser) peut consulter le dashboard.

---

## 🎨 Personnalisation

- **Couleurs** : toute la charte graphique est basée sur le drapeau ivoirien (orange, blanc, vert).
- **IA** : pour activer l'analyse IA, renseignez la clé API dans les variables d'environnement (`OPENROUTER_API_KEY`).
- **Textes, logos, footer** : modifiables dans les templates Django.

---

## 📸 Captures d'écran

_Ajoutez ici vos captures d'écran pour illustrer le test, le dashboard, la page de connexion, etc._

---

## 👨‍💻 Crédits

- Réalisé par **AKRE DANIEL**
- Design, développement et inspiration : 🇨🇮 Côte d'Ivoire, communauté francophone
- Icônes : [Twemoji](https://twemoji.twitter.com/) et émojis standards

---

## 📬 Contact

Pour toute question, suggestion ou contribution :
- [Votre email ou profil GitHub]

---

## �� Licence

Ce projet n'est pas open source.  
Tous droits réservés © AKRE ALLO DANIEL SERGE ROMARIC.  
Aucune utilisation, reproduction ou distribution n'est autorisée sans l'accord explicite de l'auteur. 