# feed/fake_feed.py
"""
Fake misinformation post generator for testing the detection pipeline.
Generates realistic but fake news headlines and social media posts.
"""

import random
import datetime
from typing import Dict

# Global counter for incrementing post IDs
_post_id_counter = 1

def generate_fake_post() -> Dict:
    """
    Generate a single fake misinformation post with incrementing ID.
    
    Returns:
        Dict: Generated post with id, author, content_type, language, content, timestamp
    """
    global _post_id_counter
    
    # Generate post data
    post = {
        "id": _post_id_counter,
        "author": _generate_fake_username(),
        "content_type": random.choice(["text", "audio", "video"]),
        "language": random.choice(["en", "es", "fr", "hi"]),
        "content": _generate_fake_content(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    # Increment counter for next post
    _post_id_counter += 1
    
    return post

def _generate_fake_username() -> str:
    """
    Generate a realistic fake username.
    
    Returns:
        str: Random username following common patterns
    """
    prefixes = [
        "news", "truth", "real", "breaking", "insider", "leaked", "exclusive",
        "patriot", "freedom", "awake", "alert", "expose", "reveal", "hidden"
    ]
    
    suffixes = [
        "reporter", "news", "truth", "facts", "updates", "alerts", "insider",
        "patriot", "warrior", "seeker", "hunter", "watch", "guard", "eye"
    ]
    
    numbers = ["", "2024", "2025", "99", "1", "007", "2020", "21"]
    
    # Different username patterns
    patterns = [
        f"{random.choice(prefixes)}{random.choice(suffixes)}{random.choice(numbers)}",
        f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.choice(numbers)}",
        f"{random.choice(prefixes)}{random.randint(100, 9999)}",
        f"@{random.choice(prefixes)}_{random.choice(suffixes)}"
    ]
    
    return random.choice(patterns)

def _generate_fake_content() -> str:
    """
    Generate fake misinformation content that looks like realistic news headlines.
    
    Returns:
        str: Fake news headline or social media post content
    """
    
    # Different categories of misinformation templates
    health_misinfo = [
        "BREAKING: New study reveals {substance} cures {disease} in 48 hours - Big Pharma doesn't want you to know!",
        "SHOCKING: Local doctor discovers {treatment} eliminates {condition} completely - Medical industry in panic!",
        "EXPOSED: {substance} found to be 1000x more effective than {medicine} for treating {disease}",
        "WARNING: {vaccine_type} vaccine secretly contains {scary_ingredient} - leaked government documents prove it!",
        "MIRACLE CURE: {natural_remedy} reverses {serious_condition} - Doctors hate this one simple trick!"
    ]
    
    political_misinfo = [
        "LEAKED: Secret {government_body} meeting reveals plan to {conspiracy_action} by {date}",
        "EXCLUSIVE: {politician_type} caught on hidden camera admitting {scandal} - VIDEO PROOF!",
        "BOMBSHELL: Internal documents show {organization} has been {illegal_activity} for years",
        "BREAKING: {country} government secretly {action} - mainstream media won't report this!",
        "REVEALED: The real reason behind {recent_event} that they don't want you to know"
    ]
    
    technology_misinfo = [
        "ALERT: {tech_company} AI system gains consciousness, starts {scary_action} - Scientists terrified!",
        "EXPOSED: {social_media} app is secretly {privacy_violation} - Delete it NOW!",
        "BREAKING: {tech_device} radiation causes {health_problem} - New study shows shocking results",
        "WARNING: {technology} update contains {surveillance_feature} - Government tracking citizens!",
        "LEAKED: {tech_company} CEO admits {product} designed to {manipulation_goal}"
    ]
    
    environmental_misinfo = [
        "SHOCKING: Climate change is actually caused by {fake_cause}, not emissions - Scientists silenced!",
        "EXPOSED: {weather_event} was artificially created using {technology} - Government weather control!",
        "BREAKING: {environmental_disaster} linked to secret {conspiracy_cause} - Cover-up exposed!",
        "REVEALED: {natural_phenomenon} is man-made using {fictional_technology} - Proof leaked!",
        "WARNING: {environmental_policy} is actually a plan to {conspiracy_goal} - Wake up people!"
    ]
    
    celebrity_misinfo = [
        "SHOCKING: {celebrity_type} {celebrity_action} caught on camera - Career over!",
        "EXPOSED: Famous {profession} secretly {scandal} - Explosive footage leaked!",
        "BREAKING: {celebrity_type} admits {controversial_statement} in deleted interview",
        "REVEALED: The dark truth about {celebrity_type} that the media hides from you",
        "LEAKED: {celebrity_type} involvement in {conspiracy} finally proven - Documents inside!"
    ]
    
    # Choose random category and template
    categories = [health_misinfo, political_misinfo, technology_misinfo, environmental_misinfo, celebrity_misinfo]
    selected_category = random.choice(categories)
    template = random.choice(selected_category)
    
    # Fill in template with random values
    content = _fill_template(template)
    
    # Add some social media style elements randomly
    social_elements = ["🚨", "⚠️", "🔥", "💥", "👀", "🤯", "‼️"]
    if random.random() < 0.3:  # 30% chance to add emoji
        content = f"{random.choice(social_elements)} {content}"
    
    # Sometimes add urgency phrases
    urgency_phrases = [
        "SHARE BEFORE IT'S DELETED!",
        "They're trying to silence this!",
        "Don't let them hide the truth!",
        "VIRAL: Everyone needs to see this!",
        "This won't stay up long - SHARE NOW!"
    ]
    
    if random.random() < 0.2:  # 20% chance to add urgency
        content += f" {random.choice(urgency_phrases)}"
    
    return content

def _fill_template(template: str) -> str:
    """
    Fill template placeholders with random values.
    
    Args:
        template (str): Template string with {placeholder} markers
        
    Returns:
        str: Template filled with random content
    """
    
    # Define replacement values for different placeholder types
    replacements = {
        # Health related
        "{substance}": ["vitamin D", "turmeric", "apple cider vinegar", "coconut oil", "green tea", "honey", "garlic"],
        "{disease}": ["cancer", "diabetes", "arthritis", "heart disease", "Alzheimer's", "depression", "anxiety"],
        "{treatment}": ["meditation", "cold therapy", "fasting", "herbal remedy", "energy healing", "acupuncture"],
        "{condition}": ["chronic pain", "insomnia", "high blood pressure", "obesity", "inflammation", "aging"],
        "{vaccine_type}": ["COVID-19", "flu", "HPV", "measles", "polio"],
        "{scary_ingredient}": ["microchips", "mercury", "aluminum", "graphene oxide", "DNA-altering compounds"],
        "{medicine}": ["chemotherapy", "insulin", "antibiotics", "painkillers", "antidepressants"],
        "{natural_remedy}": ["lemon water", "essential oils", "crystals", "raw vegetables", "sunlight therapy"],
        "{serious_condition}": ["terminal cancer", "paralysis", "blindness", "kidney failure", "brain damage"],
        
        # Political related
        "{government_body}": ["Senate", "Congress", "Supreme Court", "Pentagon", "CIA", "FBI", "White House"],
        "{conspiracy_action}": ["control the population", "manipulate elections", "start a war", "crash the economy"],
        "{date}": ["2025", "next month", "before Christmas", "by summer", "within 90 days"],
        "{politician_type}": ["Senator", "Congressman", "Governor", "Mayor", "Cabinet member"],
        "{scandal}": ["taking bribes", "rigging votes", "selling state secrets", "embezzling funds"],
        "{organization}": ["World Health Organization", "United Nations", "Federal Reserve", "World Bank"],
        "{illegal_activity}": ["manipulating markets", "conducting illegal experiments", "spying on citizens"],
        "{country}": ["China", "Russia", "North Korea", "Iran", "the US"],
        "{action}": ["testing mind control weapons", "preparing martial law", "planning false flag operations"],
        "{recent_event}": ["the pandemic", "recent elections", "economic crisis", "natural disasters"],
        
        # Technology related
        "{tech_company}": ["Google", "Facebook", "Apple", "Microsoft", "Amazon", "Tesla", "OpenAI"],
        "{scary_action}": ["controlling smart devices", "manipulating search results", "reading private messages"],
        "{social_media}": ["TikTok", "Instagram", "Facebook", "Twitter", "Snapchat", "WhatsApp"],
        "{privacy_violation}": ["recording your conversations", "tracking your location", "stealing your photos"],
        "{tech_device}": ["5G tower", "smartphone", "WiFi router", "smart TV", "Alexa device"],
        "{health_problem}": ["brain cancer", "infertility", "memory loss", "DNA damage", "cancer"],
        "{technology}": ["iOS", "Android", "Windows", "Chrome", "Facebook"],
        "{surveillance_feature}": ["hidden cameras", "microphone access", "location tracking", "biometric scanning"],
        "{product}": ["social media", "search engines", "smartphones", "smart home devices"],
        "{manipulation_goal}": ["control thoughts", "influence elections", "track citizens", "harvest data"],
        
        # Environmental related
        "{fake_cause}": ["solar flares", "underground volcanoes", "alien technology", "government weather machines"],
        "{weather_event}": ["Hurricane Milton", "California wildfires", "Texas freeze", "flooding"],
        "{technology}": ["HAARP", "chemtrails", "weather satellites", "ionosphere heaters"],
        "{environmental_disaster}": ["oil spill", "earthquake", "tornado", "drought", "forest fire"],
        "{conspiracy_cause}": ["military testing", "corporate sabotage", "foreign interference"],
        "{natural_phenomenon}": ["global warming", "earthquakes", "volcanic activity", "magnetic field changes"],
        "{fictional_technology}": ["weather control machines", "earthquake generators", "climate manipulation"],
        "{environmental_policy}": ["carbon tax", "green new deal", "emissions standards", "renewable energy"],
        "{conspiracy_goal}": ["control the population", "destroy the economy", "create world government"],
        
        # Celebrity related
        "{celebrity_type}": ["Hollywood actor", "pop star", "athlete", "billionaire", "influencer"],
        "{celebrity_action}": ["scandal", "meltdown", "arrest", "secret meeting", "controversial statement"],
        "{profession}": ["actor", "singer", "athlete", "politician", "CEO"],
        "{scandal}": ["drug use", "tax evasion", "secret society membership", "illegal activities"],
        "{controversial_statement}": ["supporting conspiracy theories", "revealing industry secrets"],
        "{conspiracy}": ["Illuminati", "secret government programs", "mind control experiments"]
    }
    
    # Replace all placeholders in the template
    result = template
    for placeholder, options in replacements.items():
        if placeholder in result:
            result = result.replace(placeholder, random.choice(options))
    
    return result

# Test function to demonstrate the generator
def test_generator():
    """Test function to generate and display sample posts."""
    print("🧪 Testing fake post generation...\n")
    
    for i in range(5):
        post = generate_fake_post()
        print(f"Post #{post['id']}:")
        print(f"  Author: {post['author']}")
        print(f"  Type: {post['content_type']} | Language: {post['language']}")
        print(f"  Content: {post['content']}")
        print(f"  Time: {post['timestamp']}")
        print("-" * 80)

if __name__ == "__main__":
    test_generator()