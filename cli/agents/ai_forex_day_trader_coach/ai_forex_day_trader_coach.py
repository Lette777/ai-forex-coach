import sys
import os
import asyncio
from typing import Annotated

# Add the src directory to Python path (based on your project structure)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

print(f"Current directory: {current_dir}")
print(f"Adding to Python path: {src_dir}")
print(f"Src directory exists: {os.path.exists(src_dir)}")

# Import the genai_session modules
try:
    from genai_session.session import GenAISession
    from genai_session.utils.context import GenAIContext
    print("✅ Successfully imported genai_session modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    
    # Show what's in the src directory
    if os.path.exists(src_dir):
        print(f"Contents of src directory: {os.listdir(src_dir)}")
        
        # Check if genai_session exists in src
        genai_session_path = os.path.join(src_dir, 'genai_session')
        if os.path.exists(genai_session_path):
            print(f"GenAI session directory exists: {genai_session_path}")
            print(f"Contents: {os.listdir(genai_session_path)}")
        else:
            print("❌ genai_session directory not found in src")
    
    sys.exit(1)

# Load environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AGENT_JWT = os.getenv('AGENT_JWT')

# For testing, you can temporarily hardcode values here (remove in production)
if not OPENAI_API_KEY:
    print("⚠️  OPENAI_API_KEY not found in environment variables")
    # Uncomment and replace with your actual API key for testing:
    # OPENAI_API_KEY = "sk-your-openai-api-key-here"

if not AGENT_JWT:
    print("⚠️  AGENT_JWT not found in environment variables")
    # Uncomment and replace with your actual JWT token for testing:
    # AGENT_JWT = "your-jwt-token-here"

if not OPENAI_API_KEY or not AGENT_JWT:
    print("\n❌ Missing required credentials. Please either:")
    print("1. Set environment variables:")
    print("   $env:OPENAI_API_KEY=\"your-api-key\"")
    print("   $env:AGENT_JWT=\"your-jwt-token\"")
    print("2. Or uncomment and fill in the hardcoded values above for testing")
    sys.exit(1)

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Initialize the GenAI session
try:
    session = GenAISession(
        jwt_token=AGENT_JWT,
        model="gpt-4",
        provider="openai"
    )
    print("✅ GenAI session initialized successfully")
except Exception as e:
    print(f"❌ Error initializing GenAI session: {e}")
    sys.exit(1)


@session.bind(
    name="ai_forex_day_trader_coach",
    description="Your coach for profitable Forex trend trading",
    model="gpt-4",
    provider="openai"
)
async def ai_forex_day_trader_coach(
    agent_context: GenAIContext,
    trading_question: Annotated[
        str,
        "The user's forex trading question or scenario they need coaching on",
    ],
):
    """
    AI Forex Day Trading Coach
    
    Provides expert guidance on forex day trading strategies, risk management,
    technical analysis, and trading psychology.
    """
    
    prompt = f"""
    You are an expert Forex day trading coach with years of experience in profitable trading.
    
    User's Question/Scenario: {trading_question}
    
    Please provide comprehensive coaching that covers:
    
    1. MARKET ANALYSIS:
       - Current market conditions assessment
       - Key technical indicators to watch
       - Support/resistance levels
       - Trend identification
    
    2. RISK MANAGEMENT:
       - Position sizing recommendations
       - Stop-loss placement strategies
       - Risk-to-reward ratios
       - Maximum daily/weekly risk limits
    
    3. TRADING STRATEGY:
       - Entry and exit criteria
       - Timeframe recommendations
       - Currency pair selection
       - Trade timing considerations
    
    4. PSYCHOLOGY & DISCIPLINE:
       - Emotional management techniques
       - Maintaining trading discipline
       - Handling losses and wins
       - Building confidence
    
    5. PRACTICAL TIPS:
       - Pre-market preparation
       - Trade journaling importance
       - Continuous learning resources
       - Common mistakes to avoid
    
    Keep your advice practical, actionable, and focused on long-term profitability.
    Use specific examples where helpful, but avoid giving financial advice.
    """
    
    try:
        response = await session.generate_response(prompt)
        return response
    except Exception as e:
        error_message = f"Error generating trading advice: {str(e)}"
        print(error_message)
        return error_message


async def main():
    """Main function to start the forex trading coach agent"""
    try:
        print("🚀 Starting AI Forex Day Trading Coach Agent...")
        print(f"📊 Using model: gpt-4")
        print("💡 Ready to provide forex trading coaching!")
        print("=" * 50)
        
        await session.process_events()
        
    except KeyboardInterrupt:
        print("\n👋 Agent stopped by user")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
    finally:
        print("🔚 Agent session ended")


if __name__ == "__main__":
    asyncio.run(main())