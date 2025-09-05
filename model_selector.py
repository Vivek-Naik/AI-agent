from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

def get_available_models():
    """Get list of available AI models based on API keys"""
    models = []
    
    # Check for Google Gemini
    if os.getenv("GOOGLE_API_KEY"):
        models.append({
            "name": "Google Gemini 1.5 Flash",
            "id": "gemini-1.5-flash",
            "provider": "Google",
            "description": "Fast and efficient model"
        })
        models.append({
            "name": "Google Gemini 1.5 Pro",
            "id": "gemini-1.5-pro",
            "provider": "Google", 
            "description": "Most capable model"
        })
    
    # Check for OpenAI
    if os.getenv("OPENAI_API_KEY"):
        models.append({
            "name": "OpenAI GPT-3.5 Turbo",
            "id": "gpt-3.5-turbo",
            "provider": "OpenAI",
            "description": "Fast and cost-effective"
        })
        models.append({
            "name": "OpenAI GPT-4",
            "id": "gpt-4",
            "provider": "OpenAI",
            "description": "Most advanced model"
        })
    
    # Check for Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        models.append({
            "name": "Anthropic Claude 3.5 Sonnet",
            "id": "claude-3-5-sonnet-20241022",
            "provider": "Anthropic",
            "description": "Balanced performance and capability"
        })
    
    return models

def select_model():
    """Display available models and let user select one"""
    models = get_available_models()
    
    if not models:
        print("❌ No AI models available. Please check your API keys in the .env file.")
        print("Required API keys:")
        print("- GOOGLE_API_KEY for Gemini")
        print("- OPENAI_API_KEY for GPT models")
        print("- ANTHROPIC_API_KEY for Claude")
        return None
    
    print("🤖 Available AI Models:")
    print("=" * 50)
    
    for i, model in enumerate(models, 1):
        print(f"{i}. {model['name']} ({model['provider']})")
        print(f"   {model['description']}")
        print()
    
    while True:
        try:
            choice = int(input(f"Select a model (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                return models[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(models)}")
        except ValueError:
            print("Please enter a valid number")

def chat_with_model(selected_model):
    """Start a chat session with the selected model"""
    print(f"\n🤖 Chatting with {selected_model['name']}")
    print("Type 'quit' to exit.\n")
    
    if selected_model['provider'] == 'Google':
        # Configure Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(selected_model['id'])
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            try:
                response = model.generate_content(user_input)
                print(f"Gemini: {response.text}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    elif selected_model['provider'] == 'OpenAI':
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model=selected_model['id'])
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            try:
                response = llm.invoke(user_input)
                print(f"GPT: {response.content}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    elif selected_model['provider'] == 'Anthropic':
        from langchain_anthropic import ChatAnthropic
        
        llm = ChatAnthropic(model=selected_model['id'])
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            try:
                response = llm.invoke(user_input)
                print(f"Claude: {response.content}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")

def main():
    print("🚀 AI Model Selector")
    print("=" * 30)
    
    selected_model = select_model()
    
    if selected_model:
        chat_with_model(selected_model)

if __name__ == "__main__":
    main()
