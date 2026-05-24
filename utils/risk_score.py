ALARMING_WORDS = {
    'Financial': ['crisis', 'crash', 'bankrupt', 'plunge', 'loss', 'collapse', 'default', 'debt', 'inflation', 'recession'],
    'Security': ['scam', 'fraud', 'disaster', 'warning', 'danger', 'risk', 'fail', 'emergency', 'threat', 'breach', 'hack', 'attack'],
    'Legal/Other': ['lawsuit', 'investigation', 'scandal', 'illegal', 'penalty', 'fine', 'guilty']
}

def calculate_risk_score(articles_data):
    """
    Calculates a risk score from 0 to 100 and returns risk categories.
    """
    if not articles_data:
        return 0, {}

    negative_count = 0
    alarming_word_count = 0
    total_articles = len(articles_data)
    category_counts = {'Financial': 0, 'Security': 0, 'Legal/Other': 0}

    for article in articles_data:
        if article.get('sentiment') == 'Negative':
            negative_count += 1
        
        text_to_check = str(article.get('title', '')) + " " + str(article.get('description', ''))
        text_to_check = text_to_check.lower()
        
        for category, words in ALARMING_WORDS.items():
            for word in words:
                if word in text_to_check:
                    alarming_word_count += 1
                    category_counts[category] += 1

    negative_percentage = (negative_count / total_articles) * 100
    alarming_penalty = min(alarming_word_count * 5, 40)
    risk_score = (negative_percentage * 0.6) + alarming_penalty
    
    return min(risk_score, 100), category_counts
