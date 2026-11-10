import re
import json
import os
import random
from datetime import datetime

# Intent response dictionaries
INTENTS = {
    "greeting": {
        "patterns": [r"\b(hi|hello|hey|namaste|hola|good morning|good evening|good afternoon)\b"],
        "responses": [
            "Hello! How can I help you today?",
            "Hi there! Ask me about business hours, products, pricing, delivery or support.",
            "Hey! Welcome to Datheon Support. What do you need help with?"
        ]
    },
    "business_hours": {
        "patterns": [r"(business|working|open|close|timing|hours|open.*time|when.*open)"],
        "responses": [
            "We are open Monday to Saturday, 9:00 AM to 6:00 PM. Sunday is closed.",
            "Our business hours: Mon-Sat, 9 AM - 6 PM. We are closed on Sundays."
        ]
    },
    "pricing": {
        "patterns": [r"(price|cost|charge|fee|pricing|how much|package|plan)"],
        "responses": [
            "Our plans start at Rs. 999/month. Basic: Rs.999, Pro: Rs.1999, Premium: Rs.2999. Which plan are you interested in?",
            "Pricing: Basic Rs.999/mo, Pro Rs.1999/mo, Premium Rs.2999/mo. All plans include support."
        ]
    },
    "products": {
        "patterns": [r"(product|service|what.*sell|what.*offer|features|do you have)"],
        "responses": [
            "We offer: 1) Training Programs, 2) Python Projects, 3) Web Development, 4) Career Support. Which one do you want details for?",
            "Our products: Training, Projects, Internship Support & Career Guidance. Tell me which one to explain."
        ]
    },
    "delivery": {
        "patterns": [r"(delivery|shipping|dispatch|when.*arrive|track|order.*status)"],
        "responses": [
            "Delivery takes 3-5 working days. You can track your order with your Order ID on our website.",
            "Orders are dispatched within 24 hours and delivered in 3-5 working days."
        ]
    },
    "refund": {
        "patterns": [r"(refund|return|exchange|money back|cancel.*order)"],
        "responses": [
            "We offer a 7-day refund policy. Share your Order ID and reason, our team will process it in 3-5 working days.",
            "For refund/return, please share your Order ID. Refunds are processed within 3-5 working days."
        ]
    },
    "support": {
        "patterns": [r"(support|help|contact|human|agent|call|email|complaint|issue|problem)"],
        "responses": [
            "You can contact support at support@datheon.in or call 1800-123-4567 (Mon-Sat, 9 AM - 6 PM).",
            "For human support, email support@datheon.in. Our team replies within 24 hours."
        ]
    },
    "thanks": {
        "patterns": [r"\b(thanks|thank you|shukriya|great|awesome|nice)\b"],
        "responses": [
            "You're welcome! Anything else I can help with?",
            "Glad I could help! Let me know if you need anything else."
        ]
    },
    "name": {
        "patterns": [r"(your name|who are you|what.*your.*name)"],
        "responses": [
            "I'm Datheon Assistant - a rule-based chatbot built in Python. How can I help you?",
        ]
    },
    "joke": {
        "patterns": [r"(joke|funny|make me laugh)"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the Python developer go broke? Because he couldn't C!",
        ]
    },
}

EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "see you"}

def load_faq_from_json(filename="faq.json"):
    faqs = []
    if os.path.exists(filename):
        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    faqs = data
                elif isinstance(data, dict):
                    faqs = data.get("faqs", data.get("intents", []))
        except Exception:
            pass
    return faqs

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

def extract_keywords(text: str):
    return re.findall(r"[a-z]+", text)

def find_intents(user_input: str):
    matched = []
    for intent_name, data in INTENTS.items():
        for pattern in data["patterns"]:
            if re.search(pattern, user_input, re.IGNORECASE):
                matched.append(intent_name)
                break
    return matched

def find_faq_match(user_input: str, faqs):
    best = None
    best_score = 0
    user_words = set(extract_keywords(user_input))
    for item in faqs:
        q = item.get("question", "") if isinstance(item, dict) else ""
        q_words = set(extract_keywords(q.lower()))
        if not q_words:
            continue
        score = len(user_words & q_words)
        if score > best_score:
            best_score = score
            best = item
    if best and best_score >= 1:
        return best.get("answer", "")
    return None

def get_response(user_input: str, faqs, context: dict):
    clean = normalize(user_input)
    if clean in EXIT_COMMANDS or any(w in clean for w in EXIT_COMMANDS):
        return None

    faq_answer = find_faq_match(clean, faqs)
    if faq_answer:
        return faq_answer

    intents = find_intents(clean)
    if intents:
        replies = []
        for intent in intents:
            replies.append(random.choice(INTENTS[intent]["responses"]))
        context["last_intent"] = intents[-1]
        return " ".join(replies)

    fallbacks = [
        "Sorry, I didn't understand that. I can help with business hours, products, pricing, delivery, refund or support. Which one?",
        "Hmm, I'm not sure about that. Try asking about 'business hours', 'price', 'products', or type 'help' for options.",
        "I didn't catch that. Could you rephrase? For example: 'What are your business hours?'"
    ]
    return random.choice(fallbacks)

def main():
    faqs = load_faq_from_json()
    context = {"state": "greeting", "last_intent": None}

    print("=" * 60)
    print("  DATHEON ASSISTANT - Rule-Based Chatbot")
    print("=" * 60)
    print("Type 'help' to see what I can do. Type 'bye' / 'exit' / 'quit' to stop.")
    print("-" * 60)
    print("Bot: Hello! I'm Datheon Assistant. How can I help you today?")

    while True:
        try:
            user = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! Have a great day!")
            break

        if not user:
            print("Bot: Please type something. Or type 'bye' to exit.")
            continue

        if normalize(user) == "help":
            print("Bot: I can help with:")
            print("     - Greeting (hi/hello)")
            print("     - Business Hours (when are you open?)")
            print("     - Products (what do you offer?)")
            print("     - Pricing (how much?)")
            print("     - Delivery / Refund / Support")
            print("     - Type 'bye' to exit")
            continue

        if normalize(user) in {"yes", "yeah", "ok", "sure"} and context["last_intent"]:
            print(f"Bot: Great! Tell me more about '{context['last_intent']}' - what exactly do you want to know?")
            continue

        response = get_response(user, faqs, context)

        if response is None:
            print("Bot: Goodbye! Thanks for chatting. Have a great day!")
            break

        print(f"Bot: {response}")

if __name__ == "__main__":
    main()