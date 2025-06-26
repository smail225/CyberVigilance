from django import forms

class CyberVigilanceForm(forms.Form):
    # Champs pour l'IA (16 questions)
    q1_phishing = forms.ChoiceField(
        label="Reconnaissez-vous les tentatives de phishing ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q2_mots_passe = forms.ChoiceField(
        label="Utilisez-vous des mots de passe forts et uniques ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q3_reseaux_sociaux = forms.ChoiceField(
        label="Êtes-vous prudent avec vos informations sur les réseaux sociaux ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q4_emails_suspects = forms.ChoiceField(
        label="Savez-vous identifier les emails suspects ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q5_sauvegarde = forms.ChoiceField(
        label="Faites-vous des sauvegardes régulières de vos données ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q6_logiciels = forms.ChoiceField(
        label="Mettez-vous à jour régulièrement vos logiciels ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q7_informations_personnelles = forms.ChoiceField(
        label="Protégez-vous vos informations personnelles en ligne ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q8_reseau_wifi = forms.ChoiceField(
        label="Êtes-vous prudent avec les réseaux WiFi publics ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q9_telechargements = forms.ChoiceField(
        label="Téléchargez-vous uniquement depuis des sources fiables ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q10_authentification = forms.ChoiceField(
        label="Utilisez-vous l'authentification à deux facteurs ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )
    
    q11_scenario_phishing = forms.ChoiceField(
        label="Vous recevez un email urgent de votre banque. Que faites-vous ?",
        choices=[
            ('a', 'Je clique immédiatement sur le lien'),
            ('b', 'Je vérifie l\'adresse email et contacte ma banque'),
            ('c', 'Je réponds avec mes informations'),
            ('d', 'Je transfère l\'email à mes amis')
        ],
        required=True
    )
    
    q12_scenario_reseau = forms.ChoiceField(
        label="Vous êtes dans un café et devez vous connecter à Internet. Que faites-vous ?",
        choices=[
            ('a', 'Je me connecte au WiFi public sans hésiter'),
            ('b', 'J\'utilise mes données mobiles ou un VPN'),
            ('c', 'Je demande le mot de passe WiFi au serveur'),
            ('d', 'Je ne me connecte pas du tout')
        ],
        required=True
    )
    
    q13_scenario_donnees = forms.ChoiceField(
        label="Une application demande l'accès à vos contacts et photos. Que faites-vous ?",
        choices=[
            ('a', 'J\'accepte pour pouvoir utiliser l\'app'),
            ('b', 'Je refuse et cherche une alternative'),
            ('c', 'J\'accepte mais je supprime l\'app après'),
            ('d', 'Je ne sais pas')
        ],
        required=True
    )
    
    q14_scenario_urgence = forms.ChoiceField(
        label="Votre ordinateur affiche un message de rançon. Que faites-vous ?",
        choices=[
            ('a', 'Je paie immédiatement la rançon'),
            ('b', 'Je déconnecte l\'ordinateur et contacte un expert'),
            ('c', 'Je continue à utiliser l\'ordinateur normalement'),
            ('d', 'Je supprime tous mes fichiers')
        ],
        required=True
    )
    
    q15_auto_evaluation = forms.ChoiceField(
        label="Comment évaluez-vous votre niveau de cybervigilance ?",
        choices=[
            ('tres_bon', 'Très bon'),
            ('bon', 'Bon'),
            ('moyen', 'Moyen'),
            ('faible', 'Faible')
        ],
        required=True
    )
    
    q16_formation = forms.ChoiceField(
        label="Avez-vous suivi une formation en cybersécurité ?",
        choices=[('oui', 'Oui'), ('non', 'Non')],
        required=True
    )

    # Questions avancées/scénarios (anciennes questions)
    s1 = forms.CharField(label="Vous téléchargez un fichier de devoir via WhatsApp, puis votre appareil devient inutilisable. Que faites-vous ?", widget=forms.Textarea, required=False)
    s2 = forms.CharField(label="Vous recevez un SMS d'Orange CI avec une mise à jour Android. Quels sont vos réflexes ?", widget=forms.Textarea, required=False)
    s3 = forms.CharField(label="Après utilisation d'un Wi-Fi public, votre compte Facebook montre une connexion inconnue. Que suspectez-vous ?", widget=forms.Textarea, required=False)
    s4 = forms.CharField(label="Vous vous êtes connecté depuis un cyber, sans vous déconnecter. Des messages étranges sont envoyés. Que s'est-il passé ?", widget=forms.Textarea, required=False)
    s5 = forms.CharField(label="On vous demande de scanner un QR code pour participer à un événement. Après cela, une appli s'installe. Qu'auriez-vous dû faire ?", widget=forms.Textarea, required=False)
    s6 = forms.CharField(label="Vous installez une appli de prière par lien Drive, et votre téléphone se dérègle. Expliquez les risques.", widget=forms.Textarea, required=False)
    s7 = forms.CharField(label="Votre téléphone perd le signal, et votre compte mobile money est vidé. Quel type d'attaque imaginez-vous ?", widget=forms.Textarea, required=False)
    s8 = forms.CharField(label="Un mail .edu vous demande vos infos personnelles dans un formulaire. Comment réagissez-vous ?", widget=forms.Textarea, required=False)
    s9 = forms.CharField(label="Votre écran affiche des enregistrements d'écran alors que vous n'avez rien lancé. Que vérifiez-vous ?", widget=forms.Textarea, required=False)
    s10 = forms.CharField(label="Vous recevez une vidéo de votre oncle vous demandant de l'aide. La vidéo semble réelle. Comment confirmez-vous l'identité ?", widget=forms.Textarea, required=False)

    a1 = forms.ChoiceField(label="Sur une échelle de 1 à 10, à quel point vous sentez-vous prudent sur Internet ?", choices=[(str(i), str(i)) for i in range(1, 11)], required=False)
    a2 = forms.CharField(label="Qu'est-ce qui vous fait le plus peur en ligne aujourd'hui ?", widget=forms.Textarea, required=False)
    a3 = forms.CharField(label="Quelle est votre plus grande faiblesse numérique selon vous ?", widget=forms.Textarea, required=False)
    a4 = forms.CharField(label="Avez-vous déjà sensibilisé quelqu'un autour de vous à la cybersécurité ? Pourquoi ?", widget=forms.Textarea, required=False) 