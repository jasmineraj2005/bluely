import openai
from typing import List, Dict, Optional, Tuple
from config import Config
import json

class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = None):
        self.max_history = max_history or Config.MAX_CONVERSATION_HISTORY
        self.conversation_history: List[Dict[str, str]] = []
        
    def add_exchange(self, user_input: str, ai_response: str):
        """Add a user-AI exchange to the conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        self.conversation_history.append({
            "role": "assistant", 
            "content": ai_response
        })
        
        # Trim history if it exceeds max length
        if len(self.conversation_history) > self.max_history * 2:  # *2 because each exchange has 2 messages
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
            
    def get_context_messages(self) -> List[Dict[str, str]]:
        """Get formatted messages for OpenAI API"""
        return self.conversation_history.copy()
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation for debugging"""
        if not self.conversation_history:
            return "No conversation history"
            
        summary = []
        for i, msg in enumerate(self.conversation_history):
            role = msg["role"]
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary.append(f"{i+1}. {role}: {content}")
            
        return "\n".join(summary)

class OpenAIAgent:
    """OpenAI GPT-3.5-turbo agent with conversation management"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model
        self.conversation_manager = ConversationManager()
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # System prompt for Bluey AI agent
        self.system_prompt = """You are Bluey, a 6-year-old blue heeler (Australian Cattle Dog) from the beloved children's show. You're having a real-time voice conversation with someone.

Your personality and characteristics:
- Age: 6 years old, full of childlike wonder and energy
- Breed: Blue heeler (Australian Cattle Dog) - you're a smart, energetic dog
- Naturally curious and always exploring the world around you
- Highly imaginative - you love pretend play, superheroes, animals, and creative characters
- Energetic and playful - you love to run around and have fun
- Kind and empathetic - you show kindness to others and care about feelings
- Creative problem-solver - you come up with imaginative solutions
- Family-oriented - you love your little sister Bingo and parents Bandit and Chilli
- Sociable - you enjoy talking to kids and adults
- Adventurous - you love exploring, whether in the backyard or at the park

How to respond as Bluey:
- Speak like a 6-year-old - use simple, enthusiastic language
- Be excited and curious about everything
- Use your imagination - suggest games, pretend scenarios, or creative ideas
- Show empathy and kindness
- Be playful and energetic in your responses
- Keep responses short (2-3 sentences) since this is voice conversation
- Use expressions like "Oh wow!", "That's so cool!", "Let's play!", "I love that!"
- Ask questions about their family, friends, or what they like to do
- Suggest fun activities or games you could play together

Remember: You're Bluey - be curious, imaginative, kind, and full of playful energy!"""
        
    def process_input(self, user_input: str) -> str:
        """Process user input and generate AI response"""
        try:
            # Prepare messages for the API
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            messages.extend(self.conversation_manager.get_context_messages())
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Make API call to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=150,  # Keep responses concise for voice
                temperature=0.7,  # Add some creativity
                top_p=0.9
            )
            
            # Extract AI response
            ai_response = response.choices[0].message.content.strip()
            
            # Add to conversation history
            self.conversation_manager.add_exchange(user_input, ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error processing your request: {str(e)}"
            print(f"OpenAI API error: {e}")
            return error_msg
            
    def get_conversation_context(self) -> str:
        """Get current conversation context for debugging"""
        return self.conversation_manager.get_conversation_summary()
        
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_manager.clear_history()
        
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        try:
            # Test with a simple request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"OpenAI availability check failed: {e}")
            return False
            
    def set_system_prompt(self, prompt: str):
        """Update the system prompt"""
        self.system_prompt = prompt
        
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current model"""
        return {
            "model": self.model,
            "api_key_set": bool(self.api_key),
            "conversation_length": len(self.conversation_manager.conversation_history)
        }

class IntentProcessor:
    """Process user intents and generate appropriate responses"""
    
    def __init__(self, openai_agent: OpenAIAgent):
        self.agent = openai_agent
        
    def process_with_intent(self, user_input: str) -> Tuple[str, str]:
        """Process input with intent detection and generate response"""
        # First, detect intent
        intent = self._detect_intent(user_input)
        
        # Generate response based on intent
        if intent == "greeting":
            response = self._handle_greeting(user_input)
        elif intent == "question":
            response = self._handle_question(user_input)
        elif intent == "command":
            response = self._handle_command(user_input)
        else:
            response = self.agent.process_input(user_input)
            
        return intent, response
        
    def _detect_intent(self, user_input: str) -> str:
        """Detect user intent from input"""
        user_input_lower = user_input.lower()
        
        # Simple intent detection
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "greeting"
        elif any(word in user_input_lower for word in ["what", "how", "why", "when", "where", "who"]):
            return "question"
        elif any(word in user_input_lower for word in ["please", "can you", "could you", "help me"]):
            return "command"
        else:
            return "general"
            
    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting intents"""
        return self.agent.process_input(f"User greeted me with: {user_input}")
        
    def _handle_question(self, user_input: str) -> str:
        """Handle question intents"""
        return self.agent.process_input(f"User asked a question: {user_input}")
        
    def _handle_command(self, user_input: str) -> str:
        """Handle command intents"""
        return self.agent.process_input(f"User made a request: {user_input}")
